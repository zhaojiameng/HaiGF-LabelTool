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

        self.paint_region = None
        
    def paint_lurbc(self, lurbc):
        """绘制left up right bottom corner"""
        print(f'paint, lurbc: {lurbc}')
        self.paint_region = lurbc
        self.update()

    def paintEvent(self, ev):
        logger.info(f'paintEvent ev: {ev}')
        if self.paint_region:
            p = QPainter(self)
            p.setOpacity(0.5)
            img = np.zeros((self.size().height(), self.size().width(), 3), dtype=np.uint8)
            img[...] = (100, 149, 237)  # 矢车菊蓝
            pixmap = general.img2pixmap(img)
            p.drawPixmap(0, 0, self.width(), self.height(), pixmap)
        

    @property
    def icon(self):
        return self._icon

    @property
    def title(self):
        return self._title

