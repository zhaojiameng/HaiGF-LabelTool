from PySide2.QtWidgets import *
from PySide2.QtGui import *
import numpy as np
from hai_ltt.utils import general
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
        self.mask_region = None  # 遮罩区域
        self.mask = QWidget(self)
        
    def mask_lurbc(self, lurbc):
        """遮罩left up right bottom corner"""
        if self.mask_region == lurbc:
            return
        self.mask_region = lurbc
        # 切换时，先清除原来的遮罩
        self.mask.hide()
        print(f'mask, lurbc: {lurbc}')
        self.mask = QWidget(self)
        # mask.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        region = self.lurbc2region(lurbc)
        self.mask.setGeometry(region[0], region[1], region[2], region[3])
        # mask.resize(self.size())
        self.mask.setStyleSheet(f'background-color: {self.mask_color};')
        self.mask.show()
        self.mask.raise_()

    def clear_mask(self):
        self.mask_region = None
        self.mask.hide()

    # def paintEvent(self, ev):
    #     logger.info(f'paintEvent ev: {ev}')
    #     if self.mask_region:
    #         p = QPainter(self)
    #         print(f'paint device: {p.device()}')
    #         p.setOpacity(0.5)
    #         img = np.zeros((self.size().height(), self.size().width(), 3), dtype=np.uint8)
    #         img[...] = (100, 149, 237)  # 矢车菊蓝
    #         pixmap = general.img2pixmap(img)
    #         region = self.lurbc2region(self.mask_region)
    #         p.drawRect(region[0], region[1], region[2], region[3])
    #         p.fillRect(region[0], region[1], region[2], region[3], Qt.red)
    #         # p.drawPixmap(region[0], region[1], region[2], region[3], pixmap)
    #         p.end()
        
    def lurbc2region(self, lurbc):
        """left up right bottom corner to region"""
        if lurbc == 'left':
            region = (0, 0, self.width()/2, self.height())
        elif lurbc == 'right':
            region = (self.width()/2, 0, self.width(), self.height())
        elif lurbc == 'up':
            region = (0, 0, self.width(), self.height()/2)
        elif lurbc == 'bottom':
            region = (0, self.height()/2, self.width(), self.height())
        elif lurbc == 'center':
            region = (0, 0, self.width(), self.height())
        else:
            raise ValueError(f'Invalid lurbc: {lurbc}')
        return region

    @property
    def icon(self):
        return self._icon

    @property
    def title(self):
        return self._title

