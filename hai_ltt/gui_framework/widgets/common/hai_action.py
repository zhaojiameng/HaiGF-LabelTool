import os.path as osp
import os
from pathlib import Path

import cv2
import numpy as np
from PySide2.QtGui import *
from PySide2.QtWidgets import QAction
from PySide2.QtSvg import QSvgRenderer

from hai_ltt.utils import general


here = Path(__file__).parent


class HAction(QAction):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self._shortcut = None
        self._tip = None
        self._icon = None
        self._text = None
        self._slot = None

        self._hovered = False
        self._icon_stem = None

    def get_icon_path(self, icon, color=None):
        icons_dir = f'{here.parent.parent}/icons'
        icons = os.listdir(icons_dir)
        if f'{icon}.svg' in icons:
            icon_name = f'{icon}.svg'
        elif f'{icon}.png' in icons:
            icon_name = f'{icon}.png'
        else:
            icon_name = 'unknown.png'
        icon_path = osp.join(icons_dir, icon_name)
        return icon_path

    def newIcon(self, icon, color=None):
        icon_path = self.get_icon_path(icon, color=color)
        
        if color is not None:
            if len(color) == 3:
                color = (color[0], color[1], color[2])
                # color = np.array(color, dtype=np.uint8)
            img = cv2.imread(icon_path)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # shape: (h, w, 4)
            # img[img[:, :, 0] > 250] = color
            lower = np.array([220, 220, 220])
            upper = np.array([255, 255, 255])
            mask = cv2.inRange(img, lower, upper)  # 范围内的为255，范围外的为0
            mask = cv2.bitwise_not(mask)  # 取反，范围内的为0，范围外的为255
            color = np.array([0, 0, 255])
            img = cv2.bitwise_and(img, img, mask=mask)
            img = cv2.add(img, color)

            # cv2.imshow("img", img)
            # cv2.waitKey(0)
            image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(image)
            # print(img[:, :, 3])
            # img转pixmap            
            # pixmap = general.img2pixmap(img)
            icon = QIcon(pixmap)
            return icon
        else:
            icon = QIcon(icon_path)
        return icon

    def setIcon(self, icon, color=None):
        print(f"setIcon: {icon}")
        if isinstance(icon, str):
            self._icon_stem = icon
            icon = self.newIcon(icon, color=color)
        super().setIcon(icon)
        self._icon = icon

    # def repaint_icon(self, color=None):
    #     icon = self._icon_stem
    #     self.setIcon(icon, color=color)


