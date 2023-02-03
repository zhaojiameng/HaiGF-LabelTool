"""
根据文件名加载文件，把原来的功能一块一块拆开
"""
import os
import os.path as osp
from pathlib import Path
# from qtpy import QtCore
# from qtpy import QtGui

from PySide2 import QtCore, QtWidgets, QtGui

from ..mm_label_file import MMLabelFile as LabelFile
from ..mm_label_file import MMLabelFileError as LabelFileError


def check_file_exists(mw, files):
    """检查文件是否存在"""

    def check_single(file):
        if QtCore.QFile.exists(file):
            return True
        else:
            mw.errorMessage(
                mw.tr("Error opening file"),
                mw.tr("No such file: <b>%s</b>") % file,
            )
            return False

    if isinstance(files, str):
        files = [files]
    elif isinstance(files, dict):
        files = [x for x in files.values() if x is not None]
    exists = [check_single(x) for x in files]
    # print(f'files: {files} exists: {exists}')
    if len([x for x in exists if x]) == len(files):  # 全部都是True
        return True
    else:
        return False


def load_json(mw, files, mm_modals_new=None):
    """files可能是str， 可能是dict，是dict时就是mm_files"""
    if isinstance(files, str):
        filenames = [files]
        mm_files = None
    elif isinstance(files, dict):
        filenames = [x for x in files.values() if x is not None]
        mm_files = files
    else:
        raise NotImplementedError(f'files {files} {type(files)}')

    label_file = osp.splitext(filenames[0])[0] + ".json"  # 所有模态共用一个json文件
    # print(self.output_dir)
    if mw.output_dir:  # 如果ouput_dir不是None，就改下前缀
        label_file_without_path = osp.basename(label_file)
        label_file = osp.join(mw.output_dir, label_file_without_path)

    # LabelFile读取文件，有imageData, imagePath, otherData labelFile对象
    if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):  # 判断有文件且是标注文件
        try:
            labelFile = LabelFile(label_file, mm_modals_new, mm_files=mm_files)  # 创建一个labelfile对象
        except LabelFileError as e:
            mw.errorMessage(
                mw.tr("Error opening file"),
                mw.tr(
                    "<p><b>%s</b></p>"
                    "<p>Make sure <i>%s</i> is a valid label file."
                )
                % (e, label_file),
            )
            mw.status(mw.tr("Error reading %s") % label_file)
            return False
        img_data = labelFile.imageData
        img_path = osp.join(osp.dirname(label_file), labelFile.imagePath, )
        other_data = labelFile.otherData
        label_file = labelFile

        modals = labelFile.modals
        imgs_data = labelFile.current_imgs
        layout = labelFile.img_layout
        scale_percent = labelFile.scale_percent
        modals_size = labelFile.modals_size

        # self.imageData = self.labelFile.imageData  # 加载到的图像数据
        # self.imagePath = osp.join(osp.dirname(label_file), self.labelFile.imagePath, )  # 图像路径，其他数据
        # self.otherData = self.labelFile.otherData
    else:
        # lf = LabelFile(filename=None, mm_files=mm_files)
        img_data, imgs_data, modals, layout, modals_size, scale_percent = LabelFile.load_image_file(
            filename=filenames[0], mm_files=mm_files, modals_new=mm_modals_new)  # 加载所有模态，imgdata是合成图，imgs_data是每个模态的数据
        # print(modals, layout)
        if img_data:
            img_path = filenames[0]
        label_file = None

    return img_data, img_path, label_file, modals, imgs_data, layout, modals_size, scale_percent
