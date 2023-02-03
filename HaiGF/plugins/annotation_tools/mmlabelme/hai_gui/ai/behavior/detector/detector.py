import os,sys
import yaml
import random
import cv2
import time
import numpy as np
import damei as dm
from copy import deepcopy
# import torch

from .YOLOv5.utils.general import non_max_suppression, scale_coords, plot_one_box


class Detector(object):
	def __init__(self, detector_type='SEYOLOv5', cfg_file=None):
		self.detecotr_type = detector_type
		self.cfg_file = cfg_file if cfg_file is not None else f'{os.getcwd()}/detector/config_files/{detector_type}_config_file.yaml'
		self.model, self.device, self.cfg, self.half = self.init_detector(detector_type)
		self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
		self.filt_classes = [int(x) for x in self.cfg['filt_classes'].split(',')] if self.cfg['filt_classes'] != '' else None
		self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(100)]  # 最大100种颜色，超过的重新取
		self.multi_source = False

	def init_detector(self, dettype):
		"""load model, load weights"""
		print(f'Detector type: {dettype}')
		if dettype == 'SEYOLOv5':
			return self.assemble_yolov5()
		else:
			raise NameError(f'unsupported detector type: {dettype}')

	def assemble_yolov5(self):
		sys.path.append(f"{os.getcwd()}/detector/YOLOv5")
		# from models.experimental import attempt_load
		# from utils.torch_utils import select_device
		from .YOLOv5.models.experimental import attempt_load
		from .YOLOv5.utils.torch_utils import select_device

		# read cfg_file
		with open(self.cfg_file, 'r') as f:
			cfg = yaml.load(f, Loader=yaml.FullLoader)
		device = select_device(cfg['device'])
		cfg['weights'] = cfg['weights'].replace('~', os.environ['HOME']) if '~' in cfg['weights'] else cfg['weights']
		model = attempt_load(cfg['weights'], map_location=device)
		# model = torch.hub.load('ultralytics/yolov5', cfg['weights'], pretrained=True)
		sys.path.remove(f"{os.getcwd()}/detector/YOLOv5")

		half = cfg['half'] and device.type != 'cpu'
		if half:
			model.half()

		return model, device, cfg, half

	def run_through_once(self, imgsz):
		# import torch
		img = torch.zeros((1, 3, imgsz, imgsz), device=self.device)  # init img
		_ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once

	def load_single_and_detect(self, file_path, img_sz=640):
		if not os.path.exists(file_path):
			return
		im0 = cv2.imread(file_path)
		img, ratio, (dw, dh) = dm.general.letterbox(deepcopy(im0), new_shape=img_sz)
		img = img[:, :, ::-1].transpose(2, 0, 1)
		img = np.ascontiguousarray(img)
		return self.detect(file_path, img, im0)

	def detect(self, paths, img, im0s):
		# print(type(paths), paths)
		# print(type(img), img.shape)  # (2, 3, 384, 640)
		# print(type(im0s), len(im0s), im0s[0].shape)
		# exit()
		device = self.device
		model = self.model
		half = self.half
		cfg = self.cfg

		paths = [paths] if isinstance(paths, str) else paths
		if img.ndim == 3:
			# LoadImages函数会只加载一张图
			# paths是一个str
			# img是ndarray [3, 384, 640]
			# im0s是一个ndarray [720, 1280, 3]
			self.multi_source = False
			imgs = img[np.newaxis, :]
			im0s = [im0s]

		else:
			imgs = img
			self.multi_source = True

		assert type(im0s) == list
		assert type(paths) == list
		imgs = torch.from_numpy(imgs).to(device)
		imgs = imgs.half() if half else imgs.float()
		imgs /= 255.0

		# inference
		model.eval()
		# t0 = time.time()
		pred = model(imgs, augment=cfg['augment'])[0]
		# NMS
		# t1 = time.time()
		pred = non_max_suppression(
			pred, cfg['conf_thres'], cfg['iou_thres'], classes=0, agnostic=cfg['agnostic_nms'])
		# pred是一个list, 元素个数的batch_size，每个元素是ndarray(num_obj, 6), 6: x1y1x2x2, conf, cls
		# 处理结果： 转为nparray
		# t2 = time.time()
		# print(f'inference time: {(t1-t0)*1000:.2f}ms {(t2-t1)*1000:.2f}ms')

		ret = []
		for i, det in enumerate(pred):  # 第i个bs
			p, im0 = paths[i], im0s[i]
			if det is not None and len(det):
				# print(det.shape, img.shape)
				det[:, :4] = scale_coords(imgs.shape[2:], det[:, :4], im0.shape).round()  # 有时候会返回None
				det = det.cpu().numpy()
				ret.append(det)
			else:
				ret.append(None)

		# ret = np.array(ret)  # [batch_size, num_obj, 6], None, 每个num_object数目可能不同
		# print(ret[0], ret[0].shape, ret[1].shape)
		# print(f'paths: {paths}')
		"""筛选感兴趣种类的目标"""
		if self.filt_classes is not None and len(ret) > 0:  # filter class
			valid_ret = []
			for bs_ret in ret:  # batch_size ret  [nun_obj, 6]
				if bs_ret is None:
					valid_ret.append(None)
					continue
				bs_valid = []
				cfg_filt_classes = cfg['filt_classes'].split(',')
				# print(f'ret: {ret} bs_ret: {bs_ret}')
				for valid_cls in cfg_filt_classes:
					tmp = bs_ret[bs_ret[:, -1] == int(valid_cls)]  # [valid_num_obj, 6] 或 [0, 6]
					if len(tmp) != 0:
						# bs_valid.append(tmp) if len(bs_valid) == 0 else bs_valid.extend(tmp)
						bs_valid.extend(tmp)
					else:
						pass
				bs_valid = np.array(bs_valid)
				# print('bs', bs_valid, bs_valid.shape)
				valid_ret.append(bs_valid)
			ret = valid_ret
			# ret = ret[np.newaxis, :, :]
		# print('xx', ret[0].shape, ret[1].shape)  # (4, 6) (22, 6), bs0有4个人，bs1有22个人
		# if self.multi_source:
		ret = ret if len(ret) > 0 else None
		# else:
		# 	ret = ret[0, :, :] if len(ret) > 0 else None

		return ret  # list, [bs, num_obj, 6] num_obj 在不同的图像中不一样, 6: xyxy,conf,cls

	def imshow(self, im0s, rets):
		# print(len(rets), type(rets))  # 长度是bs, 类型的list
		ret = rets[0]
		simg = deepcopy(im0s[0])
		h, w, c = simg.shape

		# print(f'ret: {ret.shape}')  # (n, 6)

		for i in range(len(ret)):
			bbox = ret[i, :4]
			conf = ret[i, 4]
			cls = ret[i, 5]
			label = f'{self.names[int(cls)]} {conf:.2f}'
			simg = dm.general.plot_one_box_trace_pose_status(
				x=bbox, img=simg, label=label, color=self.colors[int(cls)], line_thickness=3
			)
		simg = cv2.resize(simg, (int(w*0.5), int(h*0.5)))
		cv2.imshow('xx.png', simg)
		# if cv2.waitKey(0) == ord('q'):
		# 	exit()
