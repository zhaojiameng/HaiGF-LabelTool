import os, sys
from pathlib import Path
# from qtpy import QtGui

from PySide2 import QtCore, QtWidgets, QtGui

from collections import OrderedDict
import numpy as np


def scanMMImages(path, mm_names, extra_suffix=None):
    """
    扫描一个路径下的所有数据，返回的图像的第一个模态的数据，mm_data是一个列表，每个元素是一个字典，键是模态名，值是列表
    :param path:
    :param mm_names: vis, ir, radar76, radar24, 等
    :param extra_suffix: 额外支持的后缀
    :return:
    """
    extensions = [
        ".%s" % fmt.data().decode().lower()
        for fmt in QtGui.QImageReader.supportedImageFormats()]
    extensions = extensions if extra_suffix is None else extensions+extra_suffix

    mm_data_dict = OrderedDict()  # 有序字典，键内包含所有文件名
    for i, (root, dirs, files) in enumerate(os.walk(path)):
        valid_dir = [x for x in mm_names if x in dirs]  # 排序按mm_names来
        if len(valid_dir) == 0:  # 其他的不要
            continue
        else:
            for j, dirr in enumerate(valid_dir):
                files = os.listdir(f'{root}/{dirr}')
                files = sorted([f'{root}/{dirr}/{x}' for x in files if x.lower().endswith(tuple(extensions))])
                if dirr not in mm_data_dict.keys():
                    mm_data_dict[dirr] = files
                else:
                    mm_data_dict[dirr] += files

    # 重排序
    mm_data = []  # 全部的数据
    for i, modal in enumerate(mm_names):  # 遍历所有模态
        if modal not in mm_data_dict.keys():
            continue
        modal_files = mm_data_dict[modal]  # 该模态的所有文件
        for j, file in enumerate(modal_files):
            entry = {}
            for k, modalk in enumerate(mm_names):
                if modalk == modal:
                    # print(f'modal: {modal} modalk: {modalk} file: {file}')
                    entry[modalk] = file
                elif modalk not in mm_data_dict.keys():
                    entry[modalk] = None
                else:  # 索引其他模块, pop出来
                    corresponding_filename = f"{Path(file).parent.parent}/{modalk}/{Path(file).name}"
                    corresponding_idx = [i for i, x in enumerate(mm_data_dict[modalk]) if x == corresponding_filename]
                    if len(corresponding_idx) == 0:
                        entry[modalk] = None
                    elif len(corresponding_idx) == 1:
                        entry[modalk] = mm_data_dict[modalk].pop(corresponding_idx[0])
                    else:
                        raise NameError(f'找到的对应其他模态的索引长度大于2，可能存在重复文件。{file}')
            # print(entry)
            mm_data.append(entry)
    return mm_data


def get_mm_files_from_filename(mm_data, filename):
    """根据一个模态的文件名，取出对应的所有模态的数据，暴力搜索,
    返回：
    """
    for i, data in enumerate(mm_data):
        for j, key in enumerate(list(data.keys())):
            if data[key] == filename:
                return mm_data[i]
    return None


def imgdata2qt(mw, img_data, filename):
    image = QtGui.QImage.fromData(img_data)  # 读取图像，这个是QT的图像格式
    if image.isNull():
        formats = [
            "*.{}".format(fmt.data().decode())
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]
        mw.errorMessage(
            mw.tr("Error opening file"),
            mw.tr(
                "<p>Make sure <i>{0}</i> is a valid image file.<br/>"
                "Supported image formats: {1}</p>"
            ).format(filename, ",".join(formats)),
        )
        mw.status(mw.tr("Error reading %s") % filename)
        return False
    return image
