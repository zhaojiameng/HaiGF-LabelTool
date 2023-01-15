from PySide2.QtWidgets import *
from PySide2.QtGui import *
import numpy as np
from HaiGF.utils import general
import damei as dm
logger = dm.get_logger('hai_page')

class HPage(QWidget):
    """抽象页面，包含ToolBar和Page"""
    def __init__(self, parent=None, icon=None, title=None, **kwargs):
        super().__init__(parent, **kwargs)

        # 设置Tab bar
        self._icon = icon
        self._title = self.tr(title)

        self.mask_color = f'rgba(100, 149, 237, 0.5)'
        self._mask_region = None  # 遮罩区域
        self.maskw = QWidget(self)
        
    def mask_region(self, mask_region):
        """遮罩left up right bottom corner"""
        if self._mask_region == mask_region:
            return
        self._mask_region = mask_region
        # 切换时，先清除原来的遮罩
        self.maskw.hide()
        # print(f'mask, mask_region: {mask_region}')
        self.maskw = QWidget(self)
        # mask.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        geom = self.mask_region2geom(mask_region)
        self.maskw.setGeometry(geom[0], geom[1], geom[2], geom[3])
        # mask.resize(self.size())
        self.maskw.setStyleSheet(f'background-color: {self.mask_color};')
        self.maskw.show()
        self.maskw.raise_()

    def clear_mask(self):
        self._mask_region = None
        self.maskw.hide()
        
    def mask_region2geom(self, mask_region):
        """left up right bottom corner to geometry"""
        if mask_region == 'left':
            geom = (0, 0, self.width()/2, self.height())
        elif mask_region == 'right':
            geom = (self.width()/2, 0, self.width(), self.height())
        elif mask_region == 'top':
            geom = (0, 0, self.width(), self.height()/2)
        elif mask_region == 'bottom':
            geom = (0, self.height()/2, self.width(), self.height())
        elif mask_region == 'center':
            geom = (0, 0, self.width(), self.height())
        else:
            raise ValueError(f'Invalid mask_region: {mask_region}')
        return geom

    @property
    def icon(self):
        return self._icon

    @property
    def title(self):
        return self._title

