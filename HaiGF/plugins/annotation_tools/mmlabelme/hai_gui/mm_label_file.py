import os, sys
import base64
import contextlib
import io
import json
import os.path as osp
from pathlib import Path

import PIL.Image
import cv2
import numpy as np
from collections import OrderedDict
import damei as dm
from copy import deepcopy

from hai_gui import __version__
from hai_gui.logger import logger
from hai_gui import PY2
from hai_gui import QT4
from hai_gui import utils

from .mm import mm_quadrant_decide

PIL.Image.MAX_IMAGE_PIXELS = None


@contextlib.contextmanager
def open(name, mode):
    assert mode in ["r", "w"]
    if PY2:
        mode += "b"
        encoding = None
    else:
        encoding = "utf-8"
    yield io.open(name, mode, encoding=encoding)
    return


class MMLabelFileError(Exception):
    pass


class MMLabelFile(object):
    mm = True
    suffix = ".json"
    mm_names = ['vis', 'ir']
    cls_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                 'frisbee',
                 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                 'surfboard',
                 'tennis racket', 'bottle',
                 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
                 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
                 'oven',
                 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                 'hair drier', 'toothbrush']

    def __init__(self, filename=None, modals_new=None, mm_files=None):
        """filename是标注文件.json"""
        self.shapes = []
        self.shapes_show = []
        self.imagePath = None
        self.imageData = None
        self.current_imgs = None
        self.mm_files = mm_files
        self.modals_new = modals_new
        self.modals = ['vis'] if mm_files is None else list(mm_files.keys())
        self.img_layout = [[0, 0]]  # 图像的多模态布局，长度的模态数目，每个元素是该模态的左上角贴图位置。
        self.modals_list = []
        self.scale_percent = []
        self.modals_size = []

        if filename is not None:
            self.load(filename)
        self.filename = filename

    @staticmethod
    def read_mm_data2img(file_path):
        """读取多模态路径，全部转为图像格式"""
        if True:  # 本来就是图像格式
            return cv2.imread(file_path)
        else:  # TODO: 其他模态转图像
            raise NotImplementedError

    @staticmethod
    def cv2_load_mm(filename, mm_files=None, modals_new=None):
        """加载多模态数据，合并成一张图像，返回布局"""

        current_modals = [k for k, v in mm_files.items() if v] if mm_files else ['vis']
        current_files = [v for k, v in mm_files.items() if v] if mm_files else [filename]

        # assert filename in current_files
        assert len(current_modals) == len(current_files)

        valid_files = [x for x in current_files if os.path.exists(x)]
        assert len(valid_files) == len(current_files)  # 主程序负责保证都是存在的路径

        # 获取布局
        imgs = [MMLabelFile.read_mm_data2img(x) for x in valid_files]

        img_x_max = max([img.shape[0] for img in imgs])
        img_y_max = max([img.shape[1] for img in imgs])
        # percent of original size
        scale_percent = []
        for i in range(len(imgs)):
            img_test = imgs[i]
            if img_test.shape[0] < 0.8 * img_x_max and img_test.shape[1] < 0.8 * img_y_max:
                scale_percent.append(img_x_max/img_test.shape[0])
                width = int(img_test.shape[1] * scale_percent[i])
                height = int(img_test.shape[0] * scale_percent[i])
                dim = (width, height)
                imgs[i] = cv2.resize(img_test, dim, interpolation=cv2.INTER_AREA)
            else:
                scale_percent.append(1)

        hws = np.array([x.shape[:2] for x in imgs])  # [n, 3]  h和w的

        if modals_new is not None:
            id = []
            imgs_new = []
            scale_percent_new = []
            for mm_modal in modals_new:
                current_id = current_modals.index(mm_modal)
                id.append(current_id)
                imgs_new.append(imgs[current_id])
                scale_percent_new.append(scale_percent[current_id])
            scale_percent = scale_percent_new
        else:
            id = [0, 1, 2, 3]
            imgs_new = imgs

        gap_len = 10
        if len(imgs_new) == 1:
            h, w = hws[id[0]]  # 1080, 1920
            img_layout = [[0, 0]]

        elif len(imgs_new) == 2:
            img_layout = [[0, 0]]  # [n, 2]
            img_layout.append([hws[id[0]][1]+gap_len, 0])
            h, w = [np.max([hws[id[0]][0], hws[id[1]][0]]), np.sum([hws[id[0]][1], hws[id[1]][1]])]
            w = w+gap_len

        elif len(imgs_new) == 3:
            img_layout = [[0, 0]]  # [n, 2]
            img_layout.append([hws[id[0]][1]+gap_len, 0])
            img_layout.append([0, hws[id[0]][0]+gap_len])
            h, w = [np.max([hws[id[0]][0] + hws[id[2]][0], hws[id[1]][0]]),
                    np.max([hws[id[0]][1] + hws[id[1]][1], hws[id[2]][1]])]
            h, w = [h+gap_len, w+gap_len]

        elif len(imgs_new) == 4:
            img_layout = [[0, 0]]  # [n, 2]
            img_layout.append([hws[id[0]][1]+gap_len, 0])
            img_layout.append([0, hws[id[0]][0]+gap_len])
            img_layout.append([hws[id[0]][1]+gap_len, hws[id[0]][0]+gap_len])
            h, w = [np.max([hws[id[0]][0] + hws[id[2]][0], hws[id[1]][0] + hws[id[3]][0]]),
                    np.max([hws[id[0]][1] + hws[id[1]][1], hws[id[2]][1] + hws[id[3]][1]])]
            h, w = [h+gap_len, w+gap_len]
        # TODO: 3个或者更多模态
        else:
            raise NotImplementedError(f'{len(mm_files)} modals dataload not implemented')
        # 画图
        img = np.ones((h, w, 3), dtype=np.uint8) * 240  # 合成图
        for i, layout in enumerate(img_layout):
            img = dm.general.imgAdd(imgs_new[i], img, x=layout[1], y=layout[0], alpha=1)

        return img, imgs, current_modals, img_layout, scale_percent

    @staticmethod
    def load_image_file(filename, mm_files=None, modals_new=None):
        """从图像路径load"""
        if MMLabelFile.mm:
            img, imgs, modals, layout, scale_percent_list = MMLabelFile.cv2_load_mm(filename, mm_files=mm_files, modals_new=modals_new)
        else:
            img, modals, layout = cv2.imread(filename), ['vis'], [[0, 0]]
            imgs = [deepcopy(img)]
            scale_percent_list = [1]

        # print(img.shape, layout)
        # 获取模态的尺寸
        modals_size = []
        for i in imgs:
            modals_size.append(np.array(i).shape)

        if img is None:
            logger.error("Failed opening image file: {}".format(filename))
            return None, None, None
        ext = osp.splitext(filename)[1].lower()  # 扩展名
        img = MMLabelFile.numpy_img2bytes(img, ext=ext)
        # 转成正方形,
        # imgs = [cv2.cvtColor(dm.general.letterbox(x, color=(255, 255, 255))[0], cv2.COLOR_BGR2BGRA) for x in imgs]
        # print([x.shape for x in imgs])

        imgs = [MMLabelFile.numpy_img2bytes(x, ext=ext) for x in imgs]
        return img, imgs, modals, layout, modals_size, scale_percent_list

    @staticmethod
    def numpy_img2bytes(img, ext):
        image_pil = PIL.Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        with io.BytesIO() as f:  # 内存中创建一个二进制文件
            if PY2 and QT4:
                format = "PNG"
            elif ext in [".jpg", ".jpeg"]:
                format = "JPEG"
            else:
                format = "PNG"
            image_pil.save(f, format=format)  # 保存格式
            f.seek(0)  # 一定文件读写指针的位置
            return f.read()

    def load(self, filename):
        """这个是从json文件load"""
        keys = [
            "version",
            "modals_list",
            "modals_size",
            "imagePath",
            "shapes",  # polygonal annotations
            "flags",  # image level flags
            "imageHeight",
            "imageWidth",
        ]
        shape_keys = [
            "modal",
            "label",
            "points",
            "group_id",
            "shape_type",
            "flags",
            "tid",
            "status",
            "status_group_id",
        ]
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            version = data.get("version")
            if version is None:
                logger.warn(
                    "Loading JSON file ({}) of unknown version".format(
                        filename
                    )
                )
            elif version.split(".")[0] != __version__.split(".")[0]:
                logger.warn(
                    "This JSON file ({}) may be incompatible with "
                    "current labelme. version in file: {}, "
                    "current version: {}".format(
                        filename, version, __version__
                    )
                )

            if data["imageData"] is not None:
                imageData = base64.b64decode(data["imageData"])  # 不管了，标注文件不存
                modals = None
                layout = None
                if PY2 and QT4:
                    imageData = utils.img_data_to_png_data(imageData)
            else:
                # relative path from label file to relative path from cwd
                imagePath = osp.join(osp.dirname(filename), data["imagePath"])

                imageData, imgs, modals, layout, self.modals_size, self.scale_percent = self.load_image_file(imagePath, self.mm_files,
                                                                                        self.modals_new)

            self.modals_list = data.get("modals_list")
            flags = data.get("flags") or {}
            imagePath = data["imagePath"]
            # self._check_image_height_and_width(
            #     base64.b64encode(imageData).decode("utf-8"),
            #     data.get("imageHeight"),
            #     data.get("imageWidth"),
            # )
            shapes = [
                dict(
                    modal=s["modal"],
                    label=s["label"],
                    points=s["points"],
                    shape_type=s.get("shape_type", "polygon"),
                    flags=s.get("flags", {}),
                    group_id=s.get("group_id"),
                    other_data={k: v for k, v in s.items() if k not in shape_keys},
                    tid=s.get("tid"),
                    status=s.get("status"),
                    status_group_id=s.get("status_group_id")
                )
                for s in data["shapes"]
            ]
        except Exception as e:
            raise MMLabelFileError(e)

        otherData = {}
        for key, value in data.items():
            if key not in keys:
                otherData[key] = value

        # 载入时改为绝对坐标
        for shape in shapes:
            if self.modals_new is None:
                modal_list = modals
            else:
                modal_list = self.modals_new
            if shape['modal'] in modal_list:
                quad = modal_list.index(shape['modal'])
            else:
                continue

            for p in shape['points']:
                p[0] = (p[0]*self.scale_percent[quad] + layout[quad][0])
                p[1] = (p[1]*self.scale_percent[quad] + layout[quad][1])

        self.shapes = shapes
        # Only replace data after everything is loaded.
        self.flags = flags
        self.imagePath = imagePath
        self.imageData = imageData
        self.filename = filename
        self.otherData = otherData
        self.current_imgs = imgs
        self.modals = modals
        self.img_layout = layout

    @staticmethod
    def _check_image_height_and_width(imageData, imageHeight, imageWidth):
        img_arr = utils.img_b64_to_arr(imageData)
        if imageHeight is not None and img_arr.shape[0] != imageHeight:
            logger.error(
                "imageHeight does not match with imageData or imagePath, "
                "so getting imageHeight from actual image."
            )
            imageHeight = img_arr.shape[0]
        if imageWidth is not None and img_arr.shape[1] != imageWidth:
            logger.error(
                "imageWidth does not match with imageData or imagePath, "
                "so getting imageWidth from actual image."
            )
            imageWidth = img_arr.shape[1]
        return imageHeight, imageWidth

    def save(
            self,
            filename,
            modals_list,
            modals_size,
            shapes,
            imagePath,
            imageHeight,
            imageWidth,
            imageData=None,
            otherData=None,
            flags=None,
            modals_new=None,
            layout=[],
            scale_percent_list=[1],
            ):
        """

        :param filename:
        :param modals_list:
        :param modals_size:
        :param shapes:
        :param imagePath:
        :param imageHeight:
        :param imageWidth:
        :param imageData:
        :param otherData:
        :param flags:
        :param modals_new: list, ['vis', 'ir', ...]
        :param layout:
        :param scale_percent_list: list [float 1~xn] 长度对应模态数目，小图放大倍数
        :return:
        """

        if imageData is not None:
            imageData = base64.b64encode(imageData).decode("utf-8")
            imageHeight, imageWidth = self._check_image_height_and_width(
                imageData, imageHeight, imageWidth
            )
        if otherData is None:
            otherData = {}
        if flags is None:
            flags = {}

        shapes_new = shapes
        decide_point = [layout[1][0], layout[2][1]] if len(layout) == 3 else layout[-1]
        # 象限，单模态下是[0, 0]
        for shape in shapes_new:
            p_x = []
            p_y = []
            p_new = []
            # shape_type == 'rectangle'  # polygon
            for p in shape['points']:
                p_x.append(p[0])
                p_y.append(p[1])
            quad = mm_quadrant_decide.quad_decide(decide_point, p_x, p_y)  # 象限

            if modals_new is None:
                for p in shape['points']:
                    p_new.append((p[0] - layout[quad][0], p[1] - layout[quad][1]))
            else:
                if len(modals_new) == 1:
                    continue
                elif len(modals_new) == 2:
                    if max(p_x) < decide_point[0]:
                        continue
                    else:
                        for p in shape['points']:
                            p_new.append((p[0] - decide_point[0], p[1]))
                else:
                    for p in shape['points']:
                        p_new.append((p[0] - layout[quad][0], p[1] - layout[quad][1]))
            for i in range(len(p_new)):
                p_new[i] = (p_new[i][0]/scale_percent_list[quad], p_new[i][1]/scale_percent_list[quad])
            shape['points'] = p_new

        data = dict(
            version=__version__,
            flags=flags,
            shapes=shapes_new,
            imagePath=imagePath,
            imageData=imageData,
            imageHeight=imageHeight,
            imageWidth=imageWidth,
            modals_list=modals_list,
            modals_size=modals_size,
        )
        for key, value in otherData.items():
            assert key not in data
            data[key] = value
        try:
            with open(filename, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.filename = filename
        except Exception as e:
            raise MMLabelFileError(e)

    @staticmethod
    def is_label_file(filename):
        return osp.splitext(filename)[1].lower() == MMLabelFile.suffix

    def merge_shapes(self, ai_ret, iou_thresh=0.6):
        """合并本身存在的文件内容和ai更新的内容"""
        if ai_ret is None:
            return
        shapes = self.shapes
        s_bboxes = [dm.general.pts2bbox(s['points']) for s in shapes]

        new_shapes = []
        for i, target in enumerate(ai_ret):
            if target is None:
                continue
            bbox_xyxy = np.array(target[:4], dtype=np.float32)
            target_cls = target[4]
            tid = target[5]
            trace = target[6]
            keypoints = target[7]
            kp_score = target[8]
            pro_socre = target[9]

            status_idx = target[10]
            status_name = target[11]  # 这是一个ndarray，包含所有可能的状态
            status_score = target[12]
            duration = target[13]

            # 转成可以序列化的格式
            most_status = str(status_name[0]) if status_name is not None else None
            det_pts = [[int(bbox_xyxy[0]), int(bbox_xyxy[1])], [int(bbox_xyxy[2]), int(bbox_xyxy[3])]]

            # 根据iou找到最匹配的那个目标
            ious = [dm.general.bbox_iou(bbox_xyxy, s_bbox, return_np=True) for s_bbox in s_bboxes]
            # print(f'ious: {ious}')
            if len(ious) == 0 or np.max(ious) < iou_thresh:  # 没有或者最大的iou都小于0.9，新建
                new_shape = dict(
                    modal='vis',
                    label=self.cls_names[target_cls],
                    points=det_pts,
                    shape_type="rectangle",
                    flags={},
                    group_id=None,
                    other_data=None,
                    tid=int(tid),
                    status=most_status,
                    status_group_id=None,
                )
                new_shapes.append(new_shape)
            elif np.max(ious) >= iou_thresh:  # 覆盖更新，已有的就删除了
                idx = ious.index(np.max(ious))
                s_bboxes.pop(idx)
                shape = shapes.pop(idx)  # pop就是已经取出来了，有可能还有剩下的
                shape['modal'] = 'vis'
                shape['label'] = self.cls_names[target_cls]
                shape['points'] = det_pts
                shape['tid'] = int(tid)
                shape['status'] = most_status
                shape['shape_type'] = 'rectangle'
                new_shapes.append(shape)
                # flags, group_id, other_data, status_group_id,  不变
            else:
                raise NameError(f'label file.py merge unkown error. bbox: {bbox_xyxy}')

        self.shapes = shapes + new_shapes

        # print(f'all_shapes: {len(self.shapes)} {self.shapes}')
        # print('merge')
