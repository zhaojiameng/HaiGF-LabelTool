"""
status classifier
"""
import os
from pathlib import Path
from easydict import EasyDict
import yaml
import torch
import torch.nn.functional as F
import numpy as np
import damei as dm
from copy import deepcopy
import cv2
import random
import warnings
from ..butils import general
# from classifier.feature_builder import FeatureBuilder
# from classifier.fallen_detection import AuxiliaryDetection, SmoothAndDuration

from .feature_builder import FeatureBuilder
from .fallen_detection import AuxiliaryDetection, SmoothAndDuration


class Classifier(object):
	def __init__(self, classifier_type='ResNet50', cfg_file=None, multi_classifier=1):
		self.classifier_type = classifier_type
		self.cfg_file = cfg_file if cfg_file is not None else f'{os.getcwd()}/classifier/config_files/{classifier_type}_config_file.yaml'
		self.num_featuer_builder = multi_classifier
		self.model, self.cfg, self.device = self.init_classifier(classifier_type)
		self.names = self.model.classes
		self.names = self.names if 'fallen' in self.names else self.names+['fallen']
		self.names = self.names if 'getup' in self.names else self.names+['getup']
		self.feature_builders = self.init_feature_builders()
		self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(100)]  # 最大100种颜色，超过的重新取

		# 读取目标检测器的类别
		self.tgt_names = self.read_target_names()

		# 初始化跌倒检测器
		self.aux_det = AuxiliaryDetection(self.cfg)
		self.smooth_duration_model = SmoothAndDuration(names=self.names, bs=1)
		print(f'classifier cfg: {self.cfg}')
		# TODO: smooth duration model的batch_size应该与检测的图像一致

	def init_classifier(self, clsitype):
		print(f'Classifier type: {clsitype}')
		if clsitype == 'Resnet50':
			return self.assemble_Resnet50()
		else:
			raise NameError(f'unsupported classifier type: {clsitype}')

	def read_target_names(self):
		fp = f'{os.getcwd()}/detector/config_files/SEYOLOv5_config_file.yaml'
		with open(fp, 'r') as f:
			data = EasyDict(yaml.load(f, Loader=yaml.FullLoader))
		return data.names

	def assemble_Resnet50(self):
		from classifier.ResNet50.utils import general as resnet_general
		from classifier.ResNet50.models import resnet_zoo_behavior
		with open(self.cfg_file, 'r') as f:
			cfg = EasyDict(yaml.load(f, Loader=yaml.FullLoader))
		device = dm.torch_utils.select_device(cfg['device'])
		print(cfg, self.cfg_file)
		model = resnet_zoo_behavior.attempt_load(
			model_name='resnet50', pretrained=False, num_classes=cfg['num_classes'])
		cfg['weights'] = cfg['weights'].replace('~', os.environ['HOME']) if '~' in cfg['weights'] else cfg['weights']
		model = resnet_general.load_weights(
			weights_path=cfg['weights'], model=model, need_ckpt=False, device=device)

		print(model.classes)
		if len(cfg['device'].split(',')) >= 2:
			model.to(device)
			model = torch.nn.DataParallel(model, device_ids=cfg['device']).to(device)
		else:
			model.to(device)

		return model, cfg, device

	def init_feature_builders(self):
		num = self.num_featuer_builder
		return [FeatureBuilder(cfg_file=self.cfg_file)] * num

	def build_features(self, poser_ret, img_name, **kwargs):
		"""
		传入多重poser ret结果，构建多重特征
		:param poser_ret: results from poser
		:param img_name: image_paths
		:param kwargs: arguments
		:return: metas, features. metas: list bs*num_object个元素, 每个元素是6个值：img_name, xxyxy, tid,
		features: ndarray (num_obj_with_keypoints, 192, 640, 3)， 不同的bs全部合在一起了
		"""
		feature_builders = self.feature_builders
		assert len(feature_builders) == len(poser_ret)
		metas = []
		features = []
		bs_split = [0]  # 用于记录每个batch_size构建的有效特征数目
		for i, ret in enumerate(poser_ret):
			# print(f'ret, {ret}')
			p = img_name[i]
			# print(f'{i} {p} {ret.shape}')
			# print(ret[:, 4])
			feature_builder = feature_builders[i]
			meta, feature = feature_builder.build_feature(ret, p, kwargs)
			# print('meta', len(meta), feature.shape)
			# meta: list len=4, feature: ndarray (num_obj_with_keypoints, 192, 640, 3)
			metas.extend(meta) if meta is not None else None
			features.extend(feature) if feature is not None else None
			bs_split.append(len(features)) if feature is not None else None
		features = np.array(features)
		return metas, features, bs_split

	def build_and_save_feature(self, poser_ret, path, save_dir=''):
		"""
		:param meta: [num_obj, 3], 3: img_name, bbox, tid
		:param features: [num_obj, h, c*w, 3]
		:return:
		"""
		metas, features, bs_split = self.build_features(poser_ret, path)

		num_person = len(features) if features is not None else 0
		print(f"num_person: {num_person} {path}")
		# self.feature_builder.save_feature(meta, features, save_dir=save_dir)

	def detect_status(self, poser_rets, paths, **kwargs):
		"""
		多重状态检测
		:param poser_rets: list, [bs] (num_obj, 10)
		:param paths: list, 路径
		:param kwargs: xx
		:return: list, [bs]个元素，每个元素是(num_obj, 13), 13=10+3, 2: status_idx, status_name, status_score.
		status_ret: list 长度bs，每个元素是一个ndarray，单张图的检测结果single_ret。
		single_ret: [num_obj, 13]  长度是该图的目标数目，13列分别是不同的信息：
		0-3: bbox, x1y1x2y2格式，在原始图像上的像素坐标。
		4: target cls: 目标检测的分类的索引，共80类，目标全部类别见后，重要类别：0: person, 13: bench, 56: chair, 57: couch, 58: potted plant 59: bed, 60: dining table 62: tv 73: book 74: clock。
		目标全部类别：：['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
		5: tid: 跟踪赋予id
		6: trace: 跟踪的轨迹，list, 由多个二元组组成的列表，每个二元组是该目标在所有帧的bbox的中心位置。
		7: keypoints: 关键点，list, [136, 2]
		8: kp_score: 每个关键点的分数, list, [136, 1]
		9: pro_socre: 提议分数: list, [136, 1]
		10: status_idx: 状态类别索引，列表，可能的前n个状态，按分数高低排序。全部状态类别：['walking', 'standing', 'sitting', 'jumping', 'lying', 'squating', 'fighting']
		11: status_name: 状态类别名称, 列表，可能的前n个状态。
		12: status_score: 状态类别分数, 列表，对应n个状态的分数。
		"""
		paths = paths if isinstance(paths, list) else [paths]
		assert len(poser_rets) == len(paths)
		metas, features, bs_split = self.build_features(poser_rets, paths, **kwargs)

		# metas
		# print('detect_status metas feaures split', len(metas), features.shape, bs_split)

		outputs = self.single_detect_status(features)  # [num_obj, num_status], 10个目标，7个类别，[10, 7]
		# 状态是7个类别中值最大的那个。

		# 后处理，补全outputs, 原因是可能会出现跟踪到了，但是没有关节点的问题，导致也无法检测状态
		multi_clssify_ret = []
		for i, poser_ret in enumerate(poser_rets):  # 这个i是bs循环
			if poser_ret is None:  # 处理bs中某些图没有任何目标的情况。
				multi_clssify_ret.append(None)
				continue

			clser_ret = np.zeros((len(poser_ret), 3), dtype=object)  # [num_obj, 3]
			clser_ret[...] = None

			if len(bs_split) == 1:  # 某些图片检测到目标，跟踪到了，但没有姿态的情况
				concated_ret = np.concatenate((poser_ret, clser_ret), axis=1)
				multi_clssify_ret.append(concated_ret)
				continue

			meta = metas[bs_split[i]:bs_split[i+1]]
			out = outputs[bs_split[i]:bs_split[i+1]]
			outputs_dict = dict(zip([x[5] for x in meta], out))  # x[5]是tid

			for j in range(len(clser_ret)):
				tid = poser_ret[j][5]  # 这个是poser的tid
				if tid in outputs_dict.keys():  # 判断分类器里有没有这个tid
					cls = outputs_dict[tid]
					cls_score = np.sort(cls)[::-1]  # 对分数排序，当作置信度，从大到小
					cls_idx = np.argsort(cls)[::-1]  # 对索引取排序，从大到小
					cls_name = np.array([self.model.classes[x] for x in cls_idx])
					# print('cls score', cls_score)
					# print('cls idx  ', cls_idx, cls.shape)
					# print('cls name ', cls_name)
					clser_ret[j, 0] = cls_idx
					clser_ret[j, 1] = cls_name
					clser_ret[j, 2] = cls_score
				else:
					clser_ret[j, :] = None

			concated_ret = np.concatenate((poser_ret, clser_ret), axis=1)
			multi_clssify_ret.append(concated_ret)
		# print(len(multi_clssify_ret), multi_clssify_ret[0].shape, multi_clssify_ret[1].shape)
		multi_clssify_ret = self.post_process(multi_clssify_ret)
		multi_clssify_ret = self.smooth_duration_model(multi_clssify_ret)  # [xx, xx] bs, xx: ndarray: num_obj, 16

		return multi_clssify_ret

	def post_process(self, rets):
		"""后处理，去掉打架，添加后面的"""
		names = self.names
		fight_idx = names.index('fighting')
		fallen_idx = names.index('fallen')
		lying_idx = names.index('lying')

		self.aux_det.push(rets)

		for i, ret in enumerate(rets):  # i: bs
			if ret is None:
				continue
			for j, target in enumerate(ret):
				bbox_xyxy = target[:4]
				target_cls = target[4]
				if target_cls != 0:
					continue

				tid = target[5]
				trace = target[6]
				keypoints = target[7]
				kp_score = target[8]
				pro_socre = target[9]

				status_idx = target[10]
				status_name = target[11]
				status_score = target[12]
				# print(f'tid: {tid} s_idx: {status_idx} s_name: {status_name} s_score: {status_score}')

				if status_idx is None:
					continue
				"""1. 去除打架状态"""
				valid_idx = status_idx != fight_idx
				status_idx = status_idx[valid_idx]
				status_name = status_name[valid_idx]
				status_score = status_score[valid_idx]
				# print(f'xxx tid: {tid} s_idx: {status_idx} s_name: {status_name} s_score: {status_score}')

				"""2.二次判断，sitting，如果坐着，判断是不是假的"""
				if status_name[0] == 'sitting':
					# print('\nxxx sitting@@@')
					is_sitting, sitting_meta = self.aux_det.sitting_det(i, target, way='sitting2sitting')
					# is_sitting = self.second_judge_sitting(bbox_xyxy, keypoints, kp_score)
					if is_sitting is None:  # 不清楚，维持原状
						pass
						# print('sitting None')
					elif is_sitting:
						# print(f'sitting yes')
						pass
					else:
						print(f'修正：tid: {tid}：sitting 修成下一个状态, is sitting: {is_sitting} meta: {sitting_meta}')
						status_idx = status_idx[1::]
						status_name = status_name[1::]
						status_score = status_score[1::]
				# print(f'yyy tid: {tid} s_idx: {status_idx} s_name: {status_name} s_score: {status_score}')

				"""3.判断跌倒"""
				is_fallen, meta = self.aux_det.fallen_det(i, bbox_xyxy, tid, trace, keypoints, kp_score)
				if meta == 'might be lying':
					# 要继续判断是否是lying
					is_lying, lying_meta = self.aux_det.lying_det(i, target, is_fallen)
					is_fallen = not is_lying  # 是躺着，就不是跌倒了，是跌倒就不是躺着了
					if is_lying:
						# 进一步判断是否是起床
						is_getup, getup_meta = self.aux_det.getup_det(i, target, is_lying, lying_meta)
						status_need_update = 'getup' if is_getup else 'lying'
						# 更新
						status_idx, status_name, status_score = self.update_single_target_status(
							status_idx, status_name, status_score,
							status_need_update=status_need_update)
				if is_fallen:  # 更新
					status_idx, status_name, status_score = self.update_single_target_status(
						status_idx, status_name, status_score, status_need_update='fallen', new_score=0.95)
					# status_idx = np.insert(status_idx, 0, fallen_idx)
					# status_name = np.insert(status_name, 0, 'fallen')
					# status_score = np.insert(status_score, 0, 1)

				"""3.jumping2sitting"""
				if status_name[0] == 'jumping' or status_name[0] == 'fallen':
					is_sitting, sitting_meta = self.aux_det.sitting_det(i, target, way='jumping2sitting')
					print(f'\n jumping2siiting {is_sitting} {sitting_meta}')
					if is_sitting is None:
						pass
					if is_sitting:
						status_idx, status_name, status_score = self.update_single_target_status(
							status_idx, status_name, status_score,
							status_need_update='sitting')
					else:
						pass

				# 判断起床
				ret[j, 10] = status_idx
				ret[j, 11] = status_name
				ret[j, 12] = status_score
		return rets

	def update_single_target_status(self, idx, name, score, status_need_update, new_score=1):
		"""更新单个目标的状态，对已经存在的类别，重排序啊"""
		if status_need_update in name:
			status_need_update_in_old_idx = int(np.argwhere(name == status_need_update))
			idx = np.delete(idx, status_need_update_in_old_idx)
			name = np.delete(name, status_need_update_in_old_idx)
			score = np.delete(score, status_need_update_in_old_idx)
		status_need_update_in_names_idx = self.names.index(status_need_update)
		idx = np.insert(idx, 0, status_need_update_in_names_idx)
		name = np.insert(name, 0, status_need_update)
		score = np.insert(score, 0, new_score)
		return idx, name, score

	def single_detect_status(self, features):
		"""
		:param poser_ret: [num_obj, 10]
		:param path: img path
		:return: [num_obj, 12]
		"""
		# print(poser_ret.shape, path)

		# meta, features = self.build_feature(poser_ret, path, **kwargs)  # [num_obj, h, w*c, 3],

		if features is None or len(features) == 0:
			return None
		model = self.model
		cfg = self.cfg
		device = self.device
		batch_size = cfg['batch_size']

		features = np.array(features, dtype=np.float32)
		features = features/255.0
		features = features.transpose(0, 3, 1, 2)

		# print(features.shape, type(features), features.dtype)  # [num_cls, 192, 640, 3] n, h, w, 3, ndarray
		# 补全
		fs = features.shape  # features shape
		# remainder = fs[0] % batch_size  # 3, or 0, 1, 2, 3, 4, 5, 6, 7
		# if remainder != 0:
		# 	addend = np.zeros((batch_size-remainder, fs[1], fs[2], fs[3]), dtype=np.uint8)
		# 	features = np.concatenate((features, addend), axis=0)
		leftover = 1 if fs[0] % batch_size else 0
		num_batches = fs[0] // batch_size + leftover

		model.eval()
		features = torch.from_numpy(deepcopy(features)).contiguous()
		# features = features.permute(0, 3, 1, 2)
		# outputs = []
		outputs = np.zeros((0, len(model.classes)), dtype=np.float32)
		for i in range(num_batches):
			features = features.to(device)
			bfeature = features[i*batch_size:min((i+1)*batch_size, len(features)), ...]
			try:
				output = model(bfeature)  # [batch_size, 7]
			except Exception as e:
				warnings.warn(f'classfier error {e}')
				output = torch.randint((batch_size, 7))
			output = F.softmax(output, dim=1).detach().cpu().numpy()  # 变成0到1.
			# output = torch.argmax(output, dim=1).cpu().numpy().tolist()  # [batch_size, ]
			# outputs.extend(output)
			outputs = np.concatenate((outputs, output), axis=0)

		return outputs  # ndarray, [num_obj, 7]

	def imshow(self, rets, im0s, show_name='xxx', scale='auto', wait_time=0):
		im0s = im0s if isinstance(im0s, list) else [im0s]
		assert len(rets) == len(im0s), f'{len(rets)} != {len(im0s)}'

		simg = deepcopy(im0s[0])
		ret = rets[0]
		h, w, c = simg.shape
		# print(f'hwc: {h} {w} {c}')
		if scale == 'auto':  # 自动读取scale
			th, tw = 720, 1280  # target h target w
			scale = np.min([th/h, tw/w])
		# print(f'scale: {scale}')

		simg = self.single_plot(simg, ret)
		simg = cv2.resize(simg, (int(w * scale), int(h * scale)))
		cv2.imshow(show_name, simg)
		if cv2.waitKey(wait_time) == ord('q'):  # q to quit
			raise StopIteration

		# cv2.destroyAllWindows()
		# out_img = general.composite_imgs(out_imgs, scale=scale, gap=None)
		return simg

	def single_plot(self, orig_img, result, show_name='xxx', resize=None, save=None):

		out_img = np.copy(orig_img)
		# print(result.shape, result)
		if result is None:
			pass
		else:
			# result  [num_obj, 10]，10: xyxy cls tid trace keypoints kp_score proposal_score
			print('')
			for i, target in enumerate(result):
				bbox_xyxy = target[:4]
				target_cls = target[4]
				tid = target[5]
				trace = target[6]
				keypoints = target[7]
				kp_score = target[8]
				pro_socre = target[9]

				status_idx = target[10]
				status_name = target[11]
				status_score = target[12]

				status_topx = 2
				if status_idx is None:
					status = None
				else:
					status = [f'{status_score[k]:.2f} {x}' for k, x in enumerate(status_name[:status_topx:])]
				# print(f'status: {status}')
				# 非人目标
				target_name = self.tgt_names[target_cls]
				status = status if target_name == 'person' else None

				# print(
				# 	f'\nobj_idx: {i} target: {target_name} tracking_id: {tid}\nidx  : {status_idx} '
				# 	f'\nname : {status_name} \nscore: {status_score}')

				first_status = status_name[0] if status_name is not None else ''
				label = f"{tid:<2} {target_name} {first_status}"
				# exit()
				# status = person[11] if person[11] is not None else 'unk'
				out_img = general.plot_one_box_trace_pose_status(
					bbox_xyxy, out_img,
					label=label, color=self.colors[tid % len(self.colors)], trace=trace, status=status,
					line_thickness=4, keypoints=keypoints, kp_score=kp_score, skeleton_thickness=3, kp_radius=8, other_kp_radius=4)
		return out_img

	def analyse_ret(self, ret):
		"""
		ret: list, [bs]个元素，每个元素是(num_obj, 13), 13=10+3, 2: status_idx, status_name, status_score
		"""
		print(f'analyse bs: {len(ret)}')
		for i in range(len(ret)):
			print(f'{"-":-<30} bs index: {i} {"-":-<30}')
			single_ret = ret[i]  # 单图像的
			if single_ret is None:
				print(f'该图没有检测到任何目标')
				continue
			sp = single_ret.shape
			print(f'目标数目: {sp[0]}')
			for j, target in enumerate(single_ret):
				bbox_xyxy = target[:4]
				target_cls = target[4]
				tid = target[5]
				trace = target[6]
				keypoints = target[7]  # 也可能是None
				keypoints = keypoints if keypoints else []
				kp_score = target[8]
				pro_socre = target[9]

				status_idx = target[10]
				status_name = target[11]
				status_score = target[12]
				duration = target[13]
				"""
				print(
					f'第{j}个目标：tid: {tid} tcls: {target_cls} bbox: {bbox_xyxy} trace: {len(trace)} '
					f'kepoints: {len(keypoints)} {status_idx} name: {status_name[0:2]} score: {status_score[0:2]} '
					f'duration: {duration[0:2]}')
				"""
				if target_cls == 0:
					print(
						f'第{j}个目标：tid: {tid} tcls: {target_cls} '
						f'\nstatus  : {status_name} '
						f'\nscore   : {status_score}'
						f'\nduration: {duration}'
					)
				else:
					print(f'第{j}个目标: tid: {tid} tcls: {target_cls}')
