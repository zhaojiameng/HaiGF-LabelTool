from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class HSplitter(QSplitter):
    def __init__(self, parent=None, orientation=None, *args, **kwargs):
        super().__init__(parent=parent, orientation=orientation, *args, **kwargs)
        self.setHandleWidth(1)  # 设置分割线宽度
        self.setChildrenCollapsible(False)  # 设置子控件不可折叠
        # self.setStretchFactor(0, 1)  # 设置子控件的伸缩比例
        # self.setStretchFactor(1, 1)  # 设置子控件的伸缩比例
        # self.setCollapsible(0, False)  # 设置子控件是否可折叠
        # self.setCollapsible(1, False)  # 设置子控件是否可折叠
        self._widgets = []

    @property
    def widgets(self):
        return self._widgets

    def set_widget(self, widget):
        """设置一个子控件"""
        # 清除已有的子控件
        widgets = [widget]
        self.set_widgets(widgets)

    def set_widgets(self, widgets):
        """设置多个子控件"""
        # for i in range(self.count()):
            # self.widget(i).setParent(None)
        for i in range(len(self.widgets)):
            self.removeWidget(self.widgets[0])
        # print(widgets, len(widgets))
        for w in widgets:
            self.addWidget(w)
        
