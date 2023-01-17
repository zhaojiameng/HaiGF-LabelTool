"""
Main side bar of HAI Tools
"""
import os, sys
from pathlib import Path
from PySide2.QtWidgets import *
from HaiGF.apis import HMainSideBarWidget

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import numpy as np
import cv2
from HaiGF import utils


here = Path(__file__).parent

class HaiWidget(HMainSideBarWidget):
    
    itemDoubleClicked = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemCheckStateChanged = QtCore.Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        self.parent = parent
        self.num_mm = 1

        self.iconlist = QtWidgets.QListWidget(self)
        self.iconlist.setViewMode(QtWidgets.QListView.IconMode)
        self.iconlist.setSpacing(10)
        self.iconlist.setIconSize(QtCore.QSize(200, 200))
        # self.iconlist.setMovement(True)
        self.iconlist.setMovement(QtWidgets.QListView.Static)
        self.iconlist.setResizeMode(QtWidgets.QListView.Adjust)
        self.items = []  # 项目列表
        self.modals = []  # 
        self._default_img_data = None
        # self.try_init()
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.iconlist)
        self.setLayout(hlayout)

    @property
    def default_img_data(self):
        # img_np = np.zeros((200, 200, 3), dtype=np.uint8)
        if self._default_img_data is None:
            icon_path = f"{here.parent}/resources/default_algorithm.png"
            img = cv2.imread(icon_path)
            img = cv2.resize(img, (100, 100))
            self._default_img_data = utils.numpy_img2bytes(img, suffix='png')
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
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
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
