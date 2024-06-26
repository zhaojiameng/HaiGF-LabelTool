import os, sys
import yaml
from easydict import EasyDict
import torch
import numpy as np
import cv2
import random
from pathlib import Path
from copy import deepcopy
import damei as dm

from ..butils import general
# from detector.YOLOv5.utils.torch_utils import select_device
# from poser.utils import test_transform
# from poser.AlphaPose.utils.pPose_nms import pose_nms
# from poser.AlphaPose.utils.transforms import get_func_heatmap_to_coord

from ..detector.YOLOv5.utils.torch_utils import select_device
from .utils import test_transform
from .AlphaPose.utils.pPose_nms import pose_nms
from .AlphaPose.utils.transforms import get_func_heatmap_to_coord

# from poser.AlphaPose.models import builder
# print(sys.path)
# from alphapose.models import builder
from .AlphaPose.models import builder


class Poser(object):
	def __init__(self, poser_type='AlphaPose', cfg_file=None):
		self.poser_type = poser_type
		self.cfg_file = cfg_file if cfg_file is not None else f'{os.getcwd()}/poser/config_files/{poser_type}_config_file.yaml'
		self.model, self.cfg, self.device = self.init_poser(poser_type)
		self.heatmap_to_coord = get_func_heatmap_to_coord(self.cfg)
		self.eval_joints = [*range(0, self.cfg.DATA_PRESET.NUM_JOINTS)]
		self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(100)]  # 最大100种颜色，超过的重新取
		self.old_hmi = None

	def init_poser(self, postype):
		print(f'Poser type: {postype}')
		if postype == 'AlphaPose':
			return self.assemble_AlphaPose()
		else:
			raise NameError(f'unsupported poser type: {postype}')

	def assemble_AlphaPose(self):
		# from alphapose.models import builder
		# from .AlphaPose.models import builder

		with open(self.cfg_file, 'r') as f:
			cfg = EasyDict(yaml.load(f, Loader=yaml.FullLoader))
		device = select_device(cfg['device'])
		model = builder.build_sppe(cfg.MODEL, preset_cfg=cfg.DATA_PRESET)
		cfg['weights'] = cfg['weights'].replace('~', os.environ['HOME']) if '~' in cfg['weights'] else cfg['weights']
		print(f'Loading weights from {cfg["weights"]}')
		model.load_state_dict(torch.load(cfg['weights'], map_location=device))
		# print(cfg.device, device)
		if len(cfg['device'].split(',')) >= 2:
			model.to(device)
			model = torch.nn.DataParallel(model, device_ids=cfg['device']).to(device)
		else:
			model.to(device)

		return model, cfg, device

	def detect_pose(self, track_ret, raw_imgs, img_names, return_type='AlphaPose'):
		"""
		多重姿态检测
		:param track_ret: list, [bs] (num_obj, 7), x1 y1 x2 y2, cls, tid, trace
		:param raw_imgs: ndarray, (bs, h, w, c)
		:param img_names: list, [bs]
		:param return_type: AlphaPose or zzd
		:return: list [bs] (num_ojb, 10), xyxy, cls, tid, trace, keypoints kp_score proposal_score
		"""
		if track_ret is None:
			return None
		raw_imgs = raw_imgs if isinstance(raw_imgs, list) else [raw_imgs]
		img_names = img_names if isinstance(img_names, list) else [img_names]
		assert len(track_ret) == len(raw_imgs), f'{len(track_ret)} != {len(raw_imgs)}'
		assert len(track_ret) == len(img_names), f'{len(track_ret)} != {len(img_names)}'
		multi_pose_ret = [None] * len(track_ret)
		name_person_idx = 0  # 分类模型人的索引的是0
		for i, ret in enumerate(track_ret):
			if ret is None:
				multi_pose_ret[i] = None
				continue
			# 处理非人目标，保留检测和跟踪结果，不进行关键点检测，非人目标可能有，也可能没有
			non_person_idxes = [idx for idx, x in enumerate(ret) if x[4] != name_person_idx]
			non_person_ret = ret[non_person_idxes]  # 非人目标
			np_poser_ret = np.zeros((len(non_person_ret), 3), dtype=object)
			np_poser_ret[...] = None
			np_ret10 = np.concatenate((non_person_ret, np_poser_ret), axis=1)

			person_idxes = [idx for idx, x in enumerate(ret) if x[4] == name_person_idx]
			person_ret7 = ret[person_idxes]  # 人的目标
			person_ret10 = self.single_detect_pose(
				track_ret=person_ret7, raw_img=raw_imgs[i], img_name=img_names[i], return_type=return_type)
			if person_ret10 is None:
				p_poser_ret = np.zeros((len(person_ret7), 3), dtype=object)
				p_poser_ret[...] = None
				person_ret10 = np.concatenate((person_ret7, p_poser_ret), axis=1)

			# print(np_ret10.shape, person_ret10.shape)
			multi_pose_ret[i] = np.concatenate((person_ret10, np_ret10), axis=0)
			# print('pose none', [x[7] is None for x in multi_pose_ret[i]])
		return multi_pose_ret

	def single_detect_pose(self, track_ret, raw_img, img_name, return_type='AlphaPose'):
		"""

		:param track_ret: np.array(object): [num_obj, 7]，7: xyxy cls tid trace
		:param raw_img: np.array [h, w, 3]
		:param img_name: abs path to the image
		:param return_type:
				AlphaPose: list, 长度num_obj, 每个元素是字典，里面有img_name, result: keypoints, kp_score, proposcal_score, id, box, box是x1y1wh格式
				zzd: np.array(object): [num_obj, 10]，10: xyxy cls tid trace keypoints kp_score proposal_score
		:return: list or np.array(object)
		"""
		if track_ret is None or len(track_ret) == 0:
			return None

		model = self.model
		cfg = self.cfg
		device = self.device

		features = np.zeros((len(track_ret), 3, *cfg.DATA_PRESET.IMAGE_SIZE), dtype=np.float32)  # [5, 3, 256, 192]
		cropped_bboxes = np.zeros((len(track_ret), 4), dtype=np.float32)
		bboxes = np.array(track_ret[:, :4], dtype=np.int32)
		for i in range(len(track_ret)):
			features[i], cropped_bbox = test_transform.test_transform(raw_img, bboxes[i], cfg.DATA_PRESET.IMAGE_SIZE)
			cropped_bboxes[i] = torch.FloatTensor(cropped_bbox)
		# print(features[0].shape)  # [3, 256, 192]
		batch_size = cfg['feature_batch_size']
		leftover = 1 if len(features) % batch_size else 0
		num_batches = len(features)//batch_size + leftover
		# features.dtype = np.float16
		features = torch.from_numpy(features)

		features = features.to(device)
		# print(f'xx {type(features)}')
		half = False
		if half:
			model.half()
			features = features.half()
		model.eval()
		human_pose = []
		for i in range(num_batches):
			feature = features[i * batch_size:min((i+1)*batch_size, len(features))]

			# feature = feature.to(device)
			try:
				hm_i = model(feature)  # [4, 136, 64, 48]
				self.old_hmi = hm_i
			except Exception as e:
				print(f'poser error: {e}')
				hm_i = self.old_hmi
			# print(f'hm_i: {hm_i.shape}')
			try:
				human_pose.append(hm_i)
			except Exception as e:
				print(f'humanpose append error: {e}')
				# TODO: 使用rtsp是偶尔报错
				exit()
		# print(type(feature))
		# print(len(human_pose), num_batches, len(features), len(track_ret))
		# exit()
		human_pose = torch.cat(human_pose)  # [num_person, 136, 64, 48]
		human_pose = human_pose.detach().cpu()

		# postprocess
		# scores = track_ret[:, 4:5]
		pose_coords = []
		pose_scores = []
		assert len(human_pose) == len(track_ret)
		for i in range(len(human_pose)):  # every person
			crop_bbox = cropped_bboxes[i].tolist()
			pose_coord, pose_score = self.heatmap_to_coord(
				human_pose[i][self.eval_joints], crop_bbox,
				hm_shape=cfg.DATA_PRESET.HEATMAP_SIZE, norm_type=cfg.LOSS.NORM_TYPE)
			# print(pose_coord.shape, pose_score.shape)  # ndarray [136, 2], ndarray [136, 1]
			pose_coords.append(torch.from_numpy(pose_coord).unsqueeze(0))
			pose_scores.append(torch.from_numpy(pose_score).unsqueeze(0))
		preds_coords = torch.cat(pose_coords)
		preds_scores = torch.cat(pose_scores)

		scores = np.ones((len(track_ret), 1))  # 其实应该传入目标检测的score才对
		ids = np.array(track_ret[:, 5:6], dtype=np.int32)
		boxes, scores, ids, preds_img, preds_scores, pick_ids = pose_nms(
			torch.from_numpy(bboxes), torch.from_numpy(scores), torch.from_numpy(ids),
			preds_coords, preds_scores, cfg['min_box_area'])
		# print(type(ret), len(ret))  # list, len:6, 每个元素也是list, len：4 4是目标个数，里面是每个目标的bbox
		if return_type == 'AlphaPose':
			_result = []
			for k in range(len(scores)):
				_result.append(
					{
					'keypoints': preds_img[k],
					'kp_score': preds_scores[k],
					'proposal_score': torch.mean(preds_scores[k]) + scores[k] + 1.25 * max(preds_scores[k]),
					'idx': ids[k],
					'box': [boxes[k][0], boxes[k][1], boxes[k][2] - boxes[k][0], boxes[k][3] - boxes[k][1]]
					}
				)
			result = {
				'imgname': img_name,
				'result': _result
			}
			return result
		elif return_type == 'zzd':
			# print(track_ret)

			align_idxs = {}  # pose的结果和track根据bbox的iou对齐，键：track的idx，值：poser的idx
			for k in range(len(scores)):
				pose_box = np.array(boxes[k], dtype=np.int32)
				ious = [dm.general.bbox_iou(pose_box, np.array(x[:4], dtype=np.int32), return_np=True) for x in track_ret]
				ious = np.array(ious)
				idx = np.argmax(ious)
				assert ious[idx] > cfg['iou_thresh_for_track_pose_align']
				assert idx not in align_idxs.keys()
				align_idxs[idx] = k

			# print(align_idxs)
			poser_ret = [None] * len(track_ret)
			for z in range(len(track_ret)):
				if z not in align_idxs.keys():
					keypoints, kp_score, proposal_score = None, None, None
				else:
					poser_idx = align_idxs[z]
					keypoints = preds_img[poser_idx]
					kp_score = preds_scores[poser_idx]
					proposal_score = torch.mean(preds_scores[poser_idx] + scores[poser_idx] + 1.25 * max(preds_scores[poser_idx]))
					keypoints = keypoints.numpy().tolist()
					kp_score = kp_score.numpy().tolist()
					proposal_score = float(proposal_score.numpy())
				poser_ret[z] = [keypoints, kp_score, proposal_score]
			poser_ret = np.array(poser_ret, dtype=object)
			final_poser_ret = np.concatenate((track_ret, poser_ret), axis=1)
			# print(final_poser_ret)

			return final_poser_ret

		else:
			raise NameError(f'not supported return type: {return_type}')

	def imshow_composite(self, orig_imgs, results, show_name='xxx', scale=1):
		assert len(orig_imgs) == len(results)  # list

		out_imgs = np.zeros_like(orig_imgs)
		for i in range(len(orig_imgs)):
			orig_img = orig_imgs[i, ...]
			ret = results[i]
			out_imgs[i] = self.single_plot(orig_img=orig_img, result=ret)
		out_img = general.composite_imgs(out_imgs, scale=scale, gap=None)

		show_name = 'xx'
		print(type(show_name), type(out_img))
		cv2.imshow(show_name, out_img)
		if cv2.waitKey(0) == ord('q'):  # q to quit
			raise StopIteration

	def imshow(self, im0s, rets, show_name='xx'):
		# im0s: list
		im0s = im0s if isinstance(im0s, list) else [im0s]
		simg = deepcopy(im0s[0])
		h, w, c = simg.shape
		ret = rets[0]
		simg = self.single_plot(simg, ret)
		simg = cv2.resize(simg, (int(w*0.5), int(h*0.5)))
		cv2.imshow(show_name, simg)
		# if cv2.waitKey(0) == ord('q'):  # q to quit
			# cv2.destroyAllWindows()
		#	raise StopIteration
		# cv2.destroyAllWindows()
		return simg

	def single_plot(self, orig_img, result):
		# result  [num_obj, 10]，10: xyxy cls tid trace keypoints kp_score proposal_score
		out_img = np.copy(orig_img)
		if result is None:
			pass
		else:
			for i, person in enumerate(result):
				bbox_xyxy = person[:4]
				tid = person[5]
				trace = person[6]
				status = ''
				keypoints = person[7]
				kp_score = person[8]
				# print(type(keypoints), keypoints)  # list
				# print(type(kp_score), kp_score)  # list
				label = f"person {tid:<2}"
				out_img = general.plot_one_box_trace_pose_status(
					bbox_xyxy, out_img,
					label=label, color=self.colors[tid % len(self.colors)], trace=trace, status=status,
					keypoints=keypoints, kp_score=kp_score, skeleton_thickness=3, kp_radius=8,
					other_kp_radius=4)
		return out_img
