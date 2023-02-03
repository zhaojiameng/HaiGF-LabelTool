"""
多路摄像头并行目标检测，设置方法：在multi_camera.txt中添加stsp摄像头
"""
import os, sys
import shutil
from pathlib import Path
import argparse
from detector.detector import Detector
from dataloader.dataloader import Dataloader
from tracker.tracker import Tracker
from poser.poser import Poser
from classifier.classifier import Classifier
import cv2
import time
import numpy as np
import torch
import damei as dm


def run(opt):
	# output dir
	if os.path.exists(opt.save_dir):
		shutil.rmtree(opt.save_dir)
	os.makedirs(opt.save_dir)
	# load dataset
	dataset = Dataloader(source=opt.source, imgsz=opt.img_size).dataset

	# load object detection model, and weights
	detector = Detector(detector_type=opt.detector_type, cfg_file=opt.detector_cfg_file)
	detector.run_through_once(opt.img_size)  # 空跑一次
	tracker = Tracker(tracker_type=opt.tracker_type, cfg_file=opt.tracker_cfg_file, multi_tracker=1)
	poser = Poser(poser_type=opt.poser_type, cfg_file=opt.poser_cfg_file)
	classifier = Classifier(
		classifier_type=opt.classifier_type, cfg_file=opt.classifier_cfg_file,
		multi_classifier=1)

	filt_with_txt = False  # 先分析一下status标注文件.txt，存在的才进行检测，这样能加快速度
	if filt_with_txt:
		from classifier.data_analyse import anaylise_label
		label_ret = anaylise_label()
		label_stems = [x[0] for x in label_ret]

	for img_idx, (paths, img, im0s, vid_cap) in enumerate(dataset):
		if dataset.is_camera:
			paths = [f'{p}/{img_idx:0>6}.jpg' for p in paths]
		elif dataset.is_video:
			paths = f'{paths}/{img_idx:0>6}.jpg'
		# print(dataset.is_camera, dataset.is_video)
		print(f'\n{"":=<30} img_idx: {img_idx} img_name: {Path(paths).name} {"":=<30}')

		t0 = dm.torch_utils.time_synchronized()
		det_ret = detector.detect(paths, img, im0s)  # detect result: list, [bs, num_obj, 6] 6: xyxy,conf,cls
		# print(det_ret)
		# detector.imshow(im0s, det_ret)
		t1 = dm.torch_utils.time_synchronized()
		tra_ret = tracker.track(det_ret, im0s)  # track result: list, [bs, num_obj, 7], 7: xyxy, cls, tid, trace
		t2 = dm.torch_utils.time_synchronized()
		pose_ret = poser.detect_pose(tra_ret, im0s, paths, return_type='zzd')
		# show_img = poser.imshow(im0s, pose_ret)
		t3 = dm.torch_utils.time_synchronized()
		status_ret = classifier.detect_status(pose_ret, paths, is_camera=dataset.is_camera)  # [bs, num, 13]
		t4 = dm.torch_utils.time_synchronized()

		# 分析该batch的检测结果，输出在命令行
		classifier.analyse_ret(ret=status_ret)
		# 显示预想
		show_img = classifier.imshow(status_ret, im0s, wait_time=1)

		print(
			f'\rimgid: {img_idx:>4} detect time: {(t1-t0)*1000:>6.2f} ms '
			f'track time: {(t2-t1)*1000:>6.2f} ms '
			f'total time: {(t4-t1)*1000:>6.2f} ms ', end='')
		# 保存
		save = False
		if save:
			paths = paths if isinstance(paths, list) else [paths]
			stem = Path(paths[0]).stem
			save_dir = '/home/zzd/datasets/ceyu/raw_typical_images_detected'
			cv2.imwrite(f'{save_dir}/{stem}.jpg', show_img)
		# print(paths)
		if img_idx == 1000000:
			print(f'img_idx: {img_idx} exit')
			exit()
	print('end')


def arg_set():
	parser = argparse.ArgumentParser()
	parser.add_argument('--source', type=str, default='sources/fall6',
						help='source: file, folder, 0 for webcam')
	parser.add_argument('--save-dir', type=str, default='inference/output', help='directory to save results')
	parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels) for dataloader')

	parser.add_argument('--detector_type', type=str, default='SEYOLOv5', help='module for object detection')
	parser.add_argument('--detector_cfg_file', type=str, default=None,
						help='config file for assemble detection model, use DEFAULT cfg in detecotr/config_files if None')

	parser.add_argument('--tracker_type', type=str, default='Deepsort', help='module for object tracking')
	parser.add_argument('--tracker_cfg_file', type=str, default=None,
						help='config file for assemble tracking model, use DEFAULT cfg in tracker/config_files if None')

	parser.add_argument('--poser_type', type=str, default='AlphaPose', help='module for human pose detection')
	parser.add_argument('--poser_cfg_file', type=str, default=None,
						help='config file for assemble poser model, use DEFAULT cfg in poser/config_files if None')

	parser.add_argument('--classifier_type', type=str, default='Resnet50', help='module for human pose detection')
	parser.add_argument('--classifier_cfg_file', type=str, default=None,
						help='config file for assemble classifier model, use DEFAULT cfg in classifier/config_files if None')

	parser.add_argument('--build_classifier_feature', default=True,
						help='use detector tracker poser to build feature for status classifier')

	parser.add_argument('--feature_save_dir', default=None,
						help='dir to save feature, if not None, save feature only')

	parser.add_argument('--save_dir', type=str, default=None, help='save_dir, the saved name is {save_dir}/{stem}.jpg')
	parser.add_argument('--save-txt', type=bool, default=False, help='save results to *.txt')
	parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')

	parser.add_argument('--classfier_weights', type=str, default='', help='path to rtatus classfier weights of resnet')
	parser.add_argument('--continous', type=int, default=5, help='continous frames')
	parser.add_argument('--save-sc-txt', type=bool, default=True,
						help='save status classfication txt or not, sc_stem.txt')
	opt = parser.parse_args()
	return opt


if __name__ == '__main__':
	opt = arg_set()
	# opt.source = 'multi_camera.txt'
	# opt.source = f"/home/zzd/datasets/ceyu/raw_typical_images"
	# opt.source = f"/home/zzd/datasets/ceyu/raw_images/9floor"
	# opt.source = f"/home/zzd/datasets/ceyu/raw_fall_images/fall6"
	# opt.source = f"/home/zzd/datasets/ceyu/raw_fall_images/getup2_2"
	# opt.source = f"/home/zzd/datasets/ceyu/raw_fall_images/fallen01"
	# opt.source = '/home/zzd/datasets/xsensing/allfm_extracted/n00_m01_172205'
	opt.source = '/home/zzd/datasets/xsensing/extracted_20211217/n03_m01_172234.mp4'
	run(opt)


