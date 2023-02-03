import random
import cv2
import numpy as np
import torch
import math
import damei as dm


def letterbox(
		img, new_shape=640, color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, roi=None):
	"""
	resize image to new_shape with multiple of 32
	:param img: np.array [w, h, 3]
	:param new_shape: int or tuple, 640, [640, 320]
	:param color: background color
	:param auto: auto minimum rectangle if true
	:param scaleFill: stretch, only when auto is False
	:param scaleup: scale up and scale down if Ture else only scale down
	:param roi: use roi or not
	:return: img, ratio, (dw, dh), recover
	"""
	# Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
	shape = img.shape[:2]  # current shape [height, width]  720, 1280

	if isinstance(new_shape, int):
		new_shape = (new_shape, new_shape)

	# print(new_shape, shape)
	# Scale ratio (new / old)
	r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
	if not scaleup:  # only scale down, do not scale up (for better test mAP)
		r = min(r, 1.0)

	# Compute padding
	ratio = r, r  # width, height ratios
	new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
	dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
	# print(dw, dh, ratio)
	if auto:  # minimum rectangle
		dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
	elif scaleFill:  # stretch
		dw, dh = 0.0, 0.0
		new_unpad = (new_shape[1], new_shape[0])
		ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

	# print(dw, dh)
	dw /= 2  # divide padding into 2 sides
	dh /= 2
	# print(new_unpad)

	if shape[::-1] != new_unpad:  # resize
		img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

	# roi
	if roi is not None:
		x1, x2 = roi[0] / shape[1] * new_unpad[0], roi[2] / shape[1] * new_unpad[0]  # convert from pixel to percet
		y1, y2 = roi[1] / shape[0] * new_unpad[1], roi[3] / shape[0] * new_unpad[1]
		img = img[int(y1):int(y2), int(x1):int(x2)]
		rest_h = img.shape[0] % 32
		rest_w = img.shape[1] % 32
		dh = 0 if rest_h == 0 else (32 - rest_h) / 2
		dw = 0 if rest_w == 0 else (32 - rest_w) / 2
		recover = [new_shape[0], new_unpad[1], int(x1) - dw, int(y1) - dh]
	else:
		recover = None

	top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
	left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
	img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
	return img, ratio, (dw, dh), recover


def plot_one_box_trace_pose_status(
		x, img, color=None, label=None, line_thickness=None, focus=False, trace=None, status=None,
		keypoints=None, kp_score=None, **kwargs):
	"""
	draw box in img, support bbox, trace, pose and status, and focus
	:param x: bbox in xyxy format
	:param img: raw_img
	:param color: color in (R, G, B)
	:param label: label for target detection, i.e. cls or tid
	:param line_thickness: rt
	:param focus: is fill the inner bbox area
	:param trace: trace
	:param status: target status
	:param keypoints: tuple, [num_kps, 2], keypoints in pixel, support num_kps: 17 26 136
	:param kp_score: tuple, [num_kps, 1], score of every keypoint
	:return:
	"""
	# Plots one bounding box on image img
	tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
	color = color or [random.randint(0, 255) for _ in range(3)]
	c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
	cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
	# print('plot', img.shape, c1, c2, color, tl)
	if focus:  # 把框內的部分也填入
		focus_area = np.zeros((c2[1] - c1[1], c2[0] - c1[0], 3), dtype=np.uint8)
		focus_area[:, :, 0::] = color
		img = imgAdd(focus_area, img, x=c1[1], y=c1[0], alpha=0.75)

	if trace is not None:  # 如果传入了轨迹，就绘制轨迹，传入的轨迹是nparray (N, 2) N>=2，后面的2的xy
		# print('trace', trace)
		for i in range(len(trace) - 1):
			pt1 = tuple(trace[i])
			# pt2 = tuple(trace[i] + 1)  # 之前写的用在AILabelImage上的，没有报错啊
			pt2 = tuple(trace[i + 1])
			cv2.arrowedLine(img, pt1, pt2, color, int(2 * tl), cv2.LINE_8, 0, 0.3)

	if keypoints is not None:
		kp_preds = np.array(keypoints)
		kp_scores = np.array(kp_score)
		img = draw_keypoints_and_skeleton(img, kp_preds, kp_scores, **kwargs)

	if label:
		tf = max(tl - 1, 1)  # font thickness
		t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]

		# c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
		# cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
		# print(c1, c2)
		new_c1 = (c1[0], np.max([c1[1] - t_size[1] - 5, 0]))
		new_c2 = (np.max([c1[0] + t_size[0], c2[0]]), c1[1])  # 填充满框头，透明一半
		mh = np.min([new_c2[1], img.shape[0]]) - new_c1[1]  # mask可能会超过边界导致报错，修正
		mw = np.min([new_c2[0], img.shape[1]]) - new_c1[0]
		mask = np.zeros((mh, mw, 3), dtype=np.uint8)

		mask[...] = color
		# print(f'mask, {mask.shape} img: {img.shape} xy: {new_c1} bbox: {x}')
		img = imgAdd(mask, img, x=new_c1[1], y=new_c1[0], alpha=0.3, crop=True)
		cv2.putText(img, label, (c1[0], c1[1] - 4), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

		# 多个状态
		if status is not None:  # 绘制状态，字体稍微小一点
			status = [status] if isinstance(status, str) else status
			# print(status)
			# assert len(status) <= 2  # 最多两个状态类型，也可以是1个
			# print('s')
			l = len(status)
			spt1 = (int(x[0]), int(x[1]))  # status point 1, 左上角的点
			# spt1 = (int(x[2]), int(x[1]))  # status point 1

			max_status = status[int(np.argmax([len(mm) for mm in status]))]  # 所有字符串中最长的那个
			s_size = cv2.getTextSize(max_status, 0, fontScale=tl / 4, thickness=tf)[0]  # 它的像素尺寸,分别是w和h

			ctl = tl / 4  # current tl
			spt2 = [np.max([spt1[0] + s_size[0], int(x[2])]), spt1[1] + l * s_size[1] + 5 * l + 5]
			# spt2 = [spt1[0] + s_size[0], spt1[1] + l * s_size[1] + 5 * l + 5]
			"""
			# 填充个鬼，填充了字体太小，看不清
			# x方向填充满bbox，小于就填充，大于就缩小字体
			if spt2[0] <= int(x[2]):
				pass
			else:
				while True:
					ctl -= (tl/4)*0.02  # 每次减少1/10
					if ctl < 0:
						raise NameError(f'ctl < 0 , {ctl}')
					csize = cv2.getTextSize(max_status, 0, fontScale=ctl, thickness=tf)[0]
					if (spt1[0] + csize[0]) <= int(x[2]):
						break
			spt2[0] = int(x[2])
			"""

			mask = np.zeros((spt2[1]-spt1[1], spt2[0]-spt1[0], 3), dtype=np.uint8)
			mask[...] = color
			# 会出现在镜头mask在镜头亲可
			# print(f'x1y1: {spt1} maskshape: {mask.shape} imgshape: {img.shape}')
			# cv2.rectangle(img, spt1, spt2, color, -1, cv2.LINE_AA)
			img = imgAdd(small_img=mask, big_image=img, x=spt1[1], y=spt1[0], alpha=0.3, crop=True)

			for i, s in enumerate(status):
				cv2.putText(
					img, s, (spt1[0]+5, spt1[1]+(i+1)*s_size[1]+(i+1)*5), 0, ctl, [255, 255, 255], thickness=tf,
					lineType=cv2.LINE_AA)
	# print(status, t_size, s_size, spt1, spt2, tl)


	return img


def draw_keypoints_and_skeleton(
		img, keypoints, kp_score, kp_radius=3, other_kp_radius=1, skeleton_thickness=None,
		other_skeleton_thickness=1, prev_keypoints=None, prev_kp_score=None):
	"""
	draw keypoinys and skeleton
	:param img: raw img, [h, w, c]
	:param keypoints: ndarray, [num_kps, 2]
	:param kp_score: ndarray, [num_kps, 1]
	:param kp_radius: circle radius of keypoints, 3
	:param other_kp_radius: circle radius of keypoints exceed 26, i.e. 1,
	:param skeleton_thickness: thickness of skeleton line
	:param other_skeleton_thickness: thickness of skeleton line exceed 26, i.e. 1
	:return: img
	"""
	kp_preds = np.array(keypoints) if isinstance(keypoints, list) else keypoints
	kp_scores = np.array(kp_score) if isinstance(kp_score, list) else kp_score
	if prev_keypoints is not None:
		prev_kp_preds = np.array(prev_keypoints) if isinstance(prev_keypoints, list) else prev_keypoints
		prev_kp_scores = np.array(prev_kp_score) if isinstance(prev_kp_score, list) else prev_kp_score
	kp_num = len(kp_preds)
	if kp_num == 17:
		kp_preds = np.concatenate((kp_preds, torch.unsqueeze((kp_preds[5, :] + kp_preds[6, :]) / 2, 0)))
		kp_scores = np.concatenate((kp_scores, torch.unsqueeze((kp_scores[5, :] + kp_scores[6, :]) / 2, 0)))
	if kp_num == 17:
		kpformat = 'coco'
		if kpformat == 'coco':
			l_pair = [
				(0, 1), (0, 2), (1, 3), (2, 4),  # Head
				(5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
				(17, 11), (17, 12),  # Body
				(11, 13), (12, 14), (13, 15), (14, 16)
			]
			p_color = [
				(0, 255, 255), (0, 191, 255), (0, 255, 102), (0, 77, 255), (0, 255, 0),
				# Nose, LEye, REye, LEar, REar
				(77, 255, 255), (77, 255, 204), (77, 204, 255), (191, 255, 77), (77, 191, 255),
				(191, 255, 77),  # LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
				(204, 77, 255), (77, 255, 204), (191, 77, 255), (77, 255, 191), (127, 77, 255),
				(77, 255, 127), (0, 255, 255)]  # LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
			line_color = [
				(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50),
				(77, 255, 222), (77, 196, 255), (77, 135, 255), (191, 255, 77), (77, 255, 77),
				(77, 222, 255), (255, 156, 127),
				(0, 127, 255), (255, 127, 77), (0, 77, 255), (255, 77, 36)]
		else:
			raise NotImplementedError
	elif kp_num == 136:
		l_pair = [
			(0, 1), (0, 2), (1, 3), (2, 4),  # Head
			(5, 18), (6, 18), (5, 7), (7, 9), (6, 8), (8, 10),  # Body
			(17, 18), (18, 19), (19, 11), (19, 12),
			(11, 13), (12, 14), (13, 15), (14, 16),
			(20, 24), (21, 25), (23, 25), (22, 24), (15, 24), (16, 25),  # Foot
			(26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 33), (33, 34), (34, 35), (35, 36),
			(36, 37), (37, 38),  # Face
			(38, 39), (39, 40), (40, 41), (41, 42), (43, 44), (44, 45), (45, 46), (46, 47), (48, 49), (49, 50),
			(50, 51), (51, 52),  # Face
			(53, 54), (54, 55), (55, 56), (57, 58), (58, 59), (59, 60), (60, 61), (62, 63), (63, 64), (64, 65),
			(65, 66), (66, 67),  # Face
			(68, 69), (69, 70), (70, 71), (71, 72), (72, 73), (74, 75), (75, 76), (76, 77), (77, 78), (78, 79),
			(79, 80), (80, 81),  # Face
			(81, 82), (82, 83), (83, 84), (84, 85), (85, 86), (86, 87), (87, 88), (88, 89), (89, 90), (90, 91),
			(91, 92), (92, 93),  # Face
			(94, 95), (95, 96), (96, 97), (97, 98), (94, 99), (99, 100), (100, 101), (101, 102), (94, 103),
			(103, 104), (104, 105),  # LeftHand
			(105, 106), (94, 107), (107, 108), (108, 109), (109, 110), (94, 111), (111, 112), (112, 113),
			(113, 114),  # LeftHand
			(115, 116), (116, 117), (117, 118), (118, 119), (115, 120), (120, 121), (121, 122), (122, 123),
			(115, 124), (124, 125),  # RightHand
			(125, 126), (126, 127), (115, 128), (128, 129), (129, 130), (130, 131), (115, 132), (132, 133),
			(133, 134), (134, 135)  # RightHand
		]
		p_color = [
			(0, 255, 255), (0, 191, 255), (0, 255, 102), (0, 77, 255), (0, 255, 0),  # Nose, LEye, REye, LEar, REar
			(77, 255, 255), (77, 255, 204), (77, 204, 255), (191, 255, 77), (77, 191, 255),
			(191, 255, 77),  # 5:LShoulder, 6:RShoulder, 7:LElbow, 8:RElbow, 9:LWrist, 10:RWrist
			(204, 77, 255), (77, 255, 204), (191, 77, 255), (77, 255, 191), (127, 77, 255),
			(77, 255, 127),  # 11:LHip, 12:RHip, 13:LKnee, 14:Rknee, 15:LAnkle, 16:RAnkle
			(77, 255, 255), (0, 255, 255), (77, 204, 255),   # 17:Head, 18:Neck, 19:MidHip
			(0, 255, 255), (0, 191, 255), (0, 255, 102), (0, 77, 255), (0, 255, 0),
			(77, 255, 255)]  # foot， 25 colors

		line_color = [
			(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50),
			(0, 255, 102), (77, 255, 222), (77, 196, 255), (77, 135, 255), (191, 255, 77),
			(77, 255, 77),
			(77, 191, 255), (204, 77, 255), (77, 222, 255), (255, 156, 127),
			(0, 127, 255), (255, 127, 77), (0, 77, 255), (255, 77, 36),
			(0, 77, 255), (0, 77, 255), (0, 77, 255), (0, 77, 255), (255, 156, 127), (255, 156, 127)]
	elif kp_num == 26:
		l_pair = [
			(0, 1), (0, 2), (1, 3), (2, 4),  # Head
			(5, 18), (6, 18), (5, 7), (7, 9), (6, 8), (8, 10),  # Body
			(17, 18), (18, 19), (19, 11), (19, 12),
			(11, 13), (12, 14), (13, 15), (14, 16),
			(20, 24), (21, 25), (23, 25), (22, 24), (15, 24), (16, 25),  # Foot
		]
		p_color = [
			(0, 255, 255), (0, 191, 255), (0, 255, 102), (0, 77, 255), (0, 255, 0),  # Nose, LEye, REye, LEar, REar
			(77, 255, 255), (77, 255, 204), (77, 204, 255), (191, 255, 77), (77, 191, 255),
			(191, 255, 77),  # LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
			(204, 77, 255), (77, 255, 204), (191, 77, 255), (77, 255, 191), (127, 77, 255),
			(77, 255, 127),  # LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
			(77, 255, 255), (0, 255, 255), (77, 204, 255),  # head, neck, shoulder
			(0, 255, 255), (0, 191, 255), (0, 255, 102), (0, 77, 255), (0, 255, 0),
			(77, 255, 255)]  # foot

		line_color = [
			(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50),
			(0, 255, 102), (77, 255, 222), (77, 196, 255), (77, 135, 255), (191, 255, 77),
			(77, 255, 77),
			(77, 191, 255), (204, 77, 255), (77, 222, 255), (255, 156, 127),
			(0, 127, 255), (255, 127, 77), (0, 77, 255), (255, 77, 36),
			(0, 77, 255), (0, 77, 255), (0, 77, 255), (0, 77, 255), (255, 156, 127), (255, 156, 127)]
	else:
		raise NotImplementedError

	# draw keypoints
	vis_thres = 0.05 if kp_num == 136 else 0.4
	part_line = {}
	for n in range(kp_scores.shape[0]):
		if kp_scores[n] <= vis_thres:
			continue
		cor_x, cor_y = int(kp_preds[n, 0]), int(kp_preds[n, 1])
		part_line[n] = (cor_x, cor_y)
		# print(n, len(p_color), cor_x, cor_y)
		if n < len(p_color):
			cv2.circle(img, (cor_x, cor_y), kp_radius, p_color[n], -1)
		else:
			cv2.circle(img, (cor_x, cor_y), 1, (255, 255, 255), other_kp_radius)  # 白色
		# draw movement
		if prev_keypoints is not None:
			if prev_kp_scores[n] <= vis_thres:  # 分数太低不要
				continue
			if n >= 25:  # 只画前人体的移动，不算face和hand
				continue
			pt2 = (cor_x, cor_y)
			pt1 = (int(prev_kp_preds[n, 0]), int(prev_kp_preds[n, 1]))
			mol = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1]-pt2[1])**2)
			if mol <= 1.0:  # 太短不要
				continue
			liplenth = 0.3 if mol > 10 else 0.8  # 终端箭头缩放系数
			mol = 10 if mol > 10 else mol
			mol = (np.sqrt(10*mol) * 10)
			jit = [random.randint(0, 20) for _ in range(3)]
			color = (120-mol-jit[0], 120-mol-jit[0], 120-mol-jit[0])# 颜色随着距离增大而加深
			# print(f'{mol:.2f} {color}')
			cv2.arrowedLine(img, pt1, pt2, color, 2, cv2.LINE_8, 0, liplenth)
		# cv2.putText(img, str(n), (cor_x, cor_y), 0, 0.5, [0, 0, 0], thickness=1, lineType=cv2.LINE_AA)
	# Draw limbs
	for i, (start_p, end_p) in enumerate(l_pair):
		if start_p in part_line and end_p in part_line:
			start_xy = part_line[start_p]
			end_xy = part_line[end_p]
			if i < len(line_color):
				slt = skeleton_thickness if skeleton_thickness is not None else (2 * int(kp_scores[start_p] + kp_scores[end_p]) + 1)
				cv2.line(img, start_xy, end_xy, line_color[i], slt)
			else:
				cv2.line(img, start_xy, end_xy, (255, 255, 255), other_skeleton_thickness)

	return img


def imgAdd(small_img, big_image, x, y, alpha=0.5, crop=False):
	"""
	draw small image into big image
	:param small_img: small img
	:param big_image: big img
	:param x: left position for drawing in pixel
	:param y: top position for drawing in pixel
	:param alpha: transparency
	:return: big img draw with small img
	"""
	row, col = small_img.shape[:2]
	if small_img.shape[0] > big_image.shape[0] or small_img.shape[1] > big_image.shape[1]:
		raise NameError(f'imgAdd, the size of small img bigger than big img.')
	if crop:  # 当small_img在xy位置贴上去的时候可能会出现超过big_img边界的问题，如果crop为True，就自适应裁剪
		bigh, bigw = big_image.shape[:2]
		if x + row > bigh:
			small_img = small_img[:int(bigh-x), :, :]
		if y + col > bigw:
			small_img = small_img[:, :int(bigw-y), :]

	roi = big_image[x:x + row, y:y + col, :]
	# print('imgadd', roi.shape, small_img.shape)
	roi = cv2.addWeighted(small_img, alpha, roi, 1 - alpha, 0)
	big_image[x:x + row, y:y + col] = roi
	return big_image


def composite_imgs(imgs, titles=None, scale=1, gap=None):
	"""
	composite images to one image like monitoring
	:param imgs: ndarray, imags, (bs, h, w, 3)
	:param titles: list, str, title for plot
	:param scale: 1
	:param gap: gap pixel between different imgs
	:return: img (h*scale, w*scale, 3)
	"""
	# 设置画布, 根据目标数目设置
	# imgs = np.concatenate((imgs, imgs, imgs, imgs, imgs, imgs, imgs, imgs, imgs), axis=0)
	# titles = ['xxxxx'] * len(imgs)
	# imgs = imgs
	# print(imgs.shape)

	sp = imgs[0].shape
	h, w, c = (sp[0] * scale, sp[1] * scale, sp[2])  # convas shape

	convas = np.zeros((h, w, c), dtype=np.uint8)
	color = [193, 182, 255]  # 粉色背景, BGR
	convas[:, :, 0] = color[0]
	convas[:, :, 1] = color[1]
	convas[:, :, 2] = color[2]
	num_grid = math.ceil(np.sqrt(len(imgs)))  # 向上取整

	gap = gap if gap is not None else int(max([h/num_grid, w/num_grid]) * 0.015)
	ngap = num_grid - 1
	matrix = np.zeros((num_grid, num_grid, 2), dtype=np.int32)
	for i in range(num_grid):
		for j in range(num_grid):
			matrix[i, j, :] = np.array(
				[int((w+gap)/num_grid)*j,
				 int((h+gap)/num_grid)*i])
	matrix = matrix.reshape((-1, 2))
	# print(gap, ngap, matrix, matrix.shape)  # (m, 2), m可能取值为1, 4, 9, 16..., 2: x y

	new_size = (int((w+gap)/num_grid-gap), int((h+gap)/num_grid-gap))
	fill_img = np.zeros((new_size[1], new_size[0], 3), dtype=np.uint8)
	fill_color = (230, 230, 250)
	fill_img[..., 0] = fill_color[0]
	fill_img[..., 1] = fill_color[1]
	fill_img[..., 2] = fill_color[2]
	label = 'No Image'
	fsp = fill_img.shape
	tl = round(0.002 * (fsp[0] + fsp[1]) / 2) + 1  # line/font thickness
	cv2.putText(fill_img, label, (int(fsp[1]/5), int(fsp[0]/2)), 0, tl, [176, 196, 222],
				thickness=3, lineType=cv2.LINE_AA)

	for i in range(len(matrix)):
		yx = matrix[i]
		if i < len(imgs):
			img = imgs[i]
			img = cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)
			convas = imgAdd(img, convas, x=yx[1], y=yx[0], alpha=1)
			# title = f'{titles[i]}/{i}'
			# convas = cv2.putText(convas, title,
			# 					 (int(yx[0]+img.shape[1]/5), int(yx[1]+img.shape[0]/2)),
			# 					 0, tl/3, [0, 0, 0], thickness=3, lineType=cv2.LINE_AA)
		else:
			convas = imgAdd(fill_img, convas, x=yx[1], y=yx[0], alpha=1)

	return convas

