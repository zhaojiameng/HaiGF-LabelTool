"""
跟踪加载器，目前支持Deepsort
"""

import os
import numpy as np
import yaml
import cv2
import torch
import random
import damei as dm
import math
from ..butils import general
import matplotlib.pyplot as plt

# from detector.YOLOv5.utils.general import plot_one_box_track_status


class Tracker(object):
	def __init__(self, tracker_type='Deepsort', cfg_file=None, multi_tracker=1):
		self.detecotr_type = tracker_type
		self.cfg_file = cfg_file if cfg_file is not None else f'{os.getcwd()}/tracker/config_files/{tracker_type}_config_file.yaml'
		self.num_models = multi_tracker
		self.models, self.cfg = self.init_tracker(tracker_type)
		self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(100)]  # 最大100种颜色，超过的重新取

	def init_tracker(self, tratype):
		print(f'Tracker type: {tratype}. ')
		if tratype == 'Deepsort':
			return self.assemble_deepsort()
		else:
			raise NameError(f'unsupported tracker: {tratype}')

	def assemble_deepsort(self):

		from tracker.deep_sort import DeepSort

		with open(self.cfg_file, 'r') as f:
			cfg = yaml.load(f, Loader=yaml.FullLoader)
		cfg['weights'] = cfg['weights'].replace('~', os.environ['HOME']) if '~' in cfg['weights'] else cfg['weights']
		models = [None] * self.num_models
		for i in range(self.num_models):
			models[i] = DeepSort(cfg['weights'], use_cuda=cfg['use_cuda'])
		return models, cfg

	def track(self, det_ret, imgs):
		"""
		多重跟踪
		:param det_ret: list, 长度为batch_size， 每个元素是该路图像当前帧检测到的目标(num_obj, 6)
		:param img:
		:return:
		"""
		if det_ret is None:
			return None
		imgs = imgs if isinstance(imgs, list) else [imgs]
		models = self.models
		assert len(det_ret) == len(imgs), f'{len(det_ret)} != {len(imgs)}'
		assert len(det_ret) == len(models)
		multi_track_ret = [None] * self.num_models
		for i, data in enumerate(det_ret):
			img = imgs[i]
			model = models[i]
			multi_track_ret[i] = self.single_model_track(data, img, model=model)
		return multi_track_ret

	def single_model_track(self, det_ret, img, model=None):
		"""
		传入该图和这张图的目标检测结果，获取tid和轨迹
		:param det_ret: 单图目标检测结果(num_obj, 6), 6: xyxy, conf, cls
		:param img: 该图
		:param model: track模型，实例化对象
		:return: 单图跟踪结果(num_obj, 7), 7: xyxy, cls, tid, trace  注意，conf没有返回
		"""
		model = model if model is not None else self.models[0]
		# print(det_ret, len(det_ret), det_ret[0].shape)
		if det_ret is None or len(det_ret) == 0:  # 画面中没有检测到目标
			return
		# print(f'det_ret: {det_ret}')
		bbox_tracking = dm.general.xyxy2xywh(det_ret[:, :4])
		cls_conf = det_ret[:, 4]
		cls_ids_tracking = det_ret[:, 5]
		ret = model.update(bbox_tracking, cls_conf, cls_ids_tracking, img, return_xywh=False)  # 返回xyxy
		# 返回的ret是np.array, [18, 7], 18个目标，7: xyxy cls tid trace 少了conf
		if len(ret) == 0:  # no tracking result, use object detect result
			ret = np.array([np.array(x[:4], dtype=np.int32).tolist()+[int(x[5])]+[0]+[[[0, 0], [0, 0]]] for x in det_ret], dtype=object)
		return ret

	def imshow(self, raw_imgs, results, show_name='xxx', scale=1):
		# print(len(raw_imgs), len(results), raw_imgs[0].shape, results[0].shape)
		assert len(raw_imgs) == len(results)

		out_imgs = np.zeros_like(raw_imgs)
		for i, raw_img in enumerate(raw_imgs):
			ret = results[i]
			out_imgs[i, ...] = self.single_plot(raw_img=raw_img, ret=ret)
		out_img = general.composite_imgs(out_imgs, scale=scale, gap=None)

		show_name = 'xx'
		# print(type(show_name), type(out_img))
		cv2.imshow(show_name, out_img)
		if cv2.waitKey(5) == ord('q'):  # q to quit
			raise StopIteration

	def single_plot(self, raw_img, ret):
		"""单图，检测跟踪结果，绘图"""
		out_img = raw_img
		for x in ret:
			bbox_xyxy = x[:4]
			cls = x[4]
			tid = x[5]
			trace = x[6]
			out_img = plot_one_box_track_status(
				bbox_xyxy, out_img, label=f"{tid:<2}", color=self.colors[tid], trace=trace, status='0')
		return out_img


