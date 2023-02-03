"""
支持多模态的组件
"""
from ast import Not
import os, sys
from pathlib import Path
from tkinter import N
# from qtpy import QtCore
# from qtpy.QtCore import Qt
# from qtpy import QtGui
# from qtpy import QtWidgets
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
import numpy as np
import cv2

from hai_gui.mm_label_file import MMLabelFile

from . import utils

pydir = Path(os.path.abspath(__file__)).parent


def load_MMDock(parent, cfg, dock_name='MM List'):
    print(f'cfg: {cfg}')
    mmdock = MMDockBuilder(parent, cfg, dock_name=dock_name)
    mmdock.build_context()

    return mmdock.mm_dock


class MMDockBuilder(object):
    def __init__(self, parent, mmcfg, dock_name='MM List'):
        self.mmcfg = mmcfg
        self.mm_names = mmcfg['names']
        self.num_mm = len(self.mm_names)  # 几个模态

        self.mm_dock = QtWidgets.QDockWidget(parent.tr(dock_name), parent)

    def build_context(self):
        """组装内部控件"""
        self.mm_list = QtWidgets.QListWidget()
        self.mm_dock.setWidget(self.mm_list)
        # print(f'zzd mmdock')


class MMListWidget(QtWidgets.QWidget):

    itemDoubleClicked = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemCheckStateChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(MMListWidget, self).__init__()
        # self.resize(1024, 768)
        self.parent = parent
        self.num_mm = 1
        # MMListWidget.itemddCheckStateChanged.connect(self.slot_checkstate_changed)

        self.iconlist = QtWidgets.QListWidget()
        self.iconlist.setViewMode(QtWidgets.QListView.IconMode)
        self.iconlist.setSpacing(10)
        self.iconlist.setIconSize(QtCore.QSize(200, 200))
        self.iconlist.setMovement(True)
        self.iconlist.setResizeMode(QtWidgets.QListView.Adjust)
        self.items = []
        self.modals = []
        self._default_img_data = None
        # self.try_init()
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.iconlist)
        self.setLayout(hlayout)

    @property
    def default_img_data(self):
        # img_np = np.zeros((200, 200, 3), dtype=np.uint8)
        if self._default_img_data is None:
            icon_path = f"{pydir.parent}/icons/default_algorithm.png"
            img = cv2.imread(icon_path)
            img = cv2.resize(img, (100, 100))
            self._default_img_data = MMLabelFile.numpy_img2bytes(img, ext='png')
        return self._default_img_data

    def try_init(self):
        # print('try')
        # img = '../icons/eye.png'
        img = "/home/zzd/PycharmProject/xsensing/mmlabelme/mmlabelme/icons/eye.png"
        # print(os.path.exists(img))
        for i in range(2):
            item = QtWidgets.QListWidgetItem()
            item.setCheckable = True
            item.setEnabled = False
            # item.setChecked = True
            item.setText(f'{i} xxx!!!#@#@')
            item.setIcon(QtGui.QIcon(QtGui.QPixmap(img)))
            # item.setSizeHint(QtCore.QSize(200, 200))
            # item.setBackground(QtGui.QBrush(QtGui.QPixmap(img)))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Checked)
            self.setStyleSheet(f'background-color: #EE3B3B')
            self.iconlist.addItem(item)

    def updateModals(self, modals, modal_imgs=None, modals_new=None, mw=None):
        mw = mw if mw is not None else self.parent

        if modal_imgs is not None:
            assert len(modal_imgs) == len(modals), 'modal_imgs and modals must have the same length'
        self.iconlist.clear()
        self.items = []
        self.modals = modals
        # print(f'modals: {modals} modal_images: {type(modal_imgs)} {type(modal_imgs[0])}')
        for i, modal in enumerate(modals):
            img_data = modal_imgs[i] if modal_imgs is not None else None
            img_data = img_data if img_data is not None else self.default_img_data

            img_byte = utils.imgdata2qt(mw, img_data, filename=f'multi modal: {modal}')
            img_pixmap = QtGui.QPixmap.fromImage(img_byte)

            item = QtWidgets.QListWidgetItem()  # Item in the list
            item.setText(modal)
            # item.setSizeHint(QtCore.QSize(200, 200))
            item.setIcon(QtGui.QIcon(img_pixmap))
            if modals_new is not None:
                if modal in modals_new:
                    item.setCheckState(2)
                else:
                    item.setCheckState(0)
            else:
                item.setCheckState(2)
            # item.setBackground(QtGui.QBrush(img_pixmap))
            self.iconlist.addItem(item)
            self.items.append(item)
        # print(len(self.iconlist))
        self.update()

    def slot_checkstate_changed(self, state_list):
        # xTODO
        modal_list = np.array(self.modals)
        modal_list_new = list(modal_list[np.nonzero(np.array(state_list))[0]])
        # 多模态修改 信号传递
        return modal_list_new

    def clean(self):
        self.updateModals(modals=[])














