from PySide2.QtWidgets import *
from PySide2.QtGui import *
import numpy as np
from HaiGF.utils import general
from HaiGF.apis import HGF
import damei as dm
logger = dm.get_logger('hai_page')

class HPage(QWidget):
    """
    This is the base class of HaiGF's page, inherited from QWidget, can be added to the central widget.
    One page contains a title bar and an empty widget.
    The title bar contains title icon, title text, close button, etc.

    :param optinal parent: Parent widget, usually `mw`.
    :param optional icon: Icon to be displayed in title bar.
    :param optional title: Title to be displayed in title bar.
    :param optional kwargs: Other keyword arguments to be passed to QWidget.
    """
    def __init__(self, parent=None, icon=None, title=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent

        self._icon = icon
        self._title = title if title else self.tr('HPage Title')

        self.mask_color = f'rgba(100, 149, 237, 0.5)'
        self._mask_region = None  # 遮罩区域
        self.maskw = QWidget(self)  # 遮罩控件

        self.setStyleSheet(HGF.PAGE_CSS)
        
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

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    @title.setter
    def title(self, title):
        self._title = title

    def set_icon(self, icon: QIcon):
        """
        设置页面标题的图标\n
        """
        self.icon = icon

    def set_title(self, title: str):
        """
        设置页面标题的文字
        """
        self.title = title

    def set_widget(self, widget: QWidget):
        """
        Set the widget of the page.
        """
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(widget)
        self.setLayout(self.layout)

    def hide(self):
        # print(f'hide page: {self.title}')
        # self._p = self.parent()
        # self.setParent(None)
        super().hide()
        
    def show(self):
        # if self._p:
            # self._p.setCurrentWidget(self)
            # self.setParent(self._p)
        super().show()

