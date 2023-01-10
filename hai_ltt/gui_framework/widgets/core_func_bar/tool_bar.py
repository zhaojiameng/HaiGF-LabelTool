import numpy as np
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import damei as dm
from functools import partial

from ... import utils
from hai_ltt.apis import HGF

logger = dm.get_logger('tool_bar')

def get_toolbar(title, parent=None, actions=None):
    """
    创建一个工具栏
    """
    toolbar = ToolBar(title, parent=parent)
    toolbar.setObjectName(f"{title} ToolBar")
    # toolbar.setOrientation(QtCore.Qt.Vertical)
    toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
    if actions:
        utils.addActions(toolbar, actions)
    # print(toolbar.sizeHint())
    return toolbar

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, title, parent=None):
        super(ToolBar, self).__init__(title, parent=parent)
        self.layout = self.layout()

        m = (0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 设置左顶右底的边距
        self.setContentsMargins(0, 0, 0, 0)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setMovable(False)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        self.setIconSize(QtCore.QSize(np.ceil(48*HGF.SCALE_FACTOR), np.ceil(48*HGF.SCALE_FACTOR)))

    def paintEvent(self, ev):
        # 绘制背景
        painter = QtWidgets.QStylePainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QColor(HGF.CORE_FUNC_BAR_BACKGOUND_COLOR))
        painter.drawRect(self.rect())  # 绘制rect为LightGray
        # 绘制选中Checked的
        for i in range(self.layout.count()):  # 遍历所有的widget
            w = self.layout.itemAt(i).widget()
            w_geom = w.geometry()
            if not isinstance(w, QtWidgets.QToolButton):
                continue
            a = w.defaultAction()  # action
            if a.isChecked():
                painter.setPen(QColor(HGF.COLORS.White))
                # 在widget左侧画线条，粗细为10
                x1, y1 = w_geom.left(), w_geom.top()
                x2, y2 = w_geom.left(), w_geom.bottom()
                print(x1, y1, x2, y2)
                thickness = 3
                for j in range(thickness):
                    painter.drawLine(0+j, y1, 0+j, y2)


                # painter.drawLine(x1, y1, x2+thickness, y2)
                
                # painter.drawLine(w_geom.left(), w_geom.top(), w_geom.left(), w_geom.bottom())
    
        # 设置背景颜色灰色
        self.setStyleSheet(F"background-color: {HGF.CORE_FUNC_BAR_BACKGOUND_COLOR};")
        # self.setStyleSheet(F"background-color: {HGF.COLORS.RoyalBlue};")
        painter.end()

        
    def addAction(self, action):
        if isinstance(action, QtWidgets.QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = QtWidgets.QToolButton()
        btn.setDefaultAction(action)
        self.addWidget(btn)
        action.hovered.connect(partial(self.hover_event, action.text()))
        action.triggered.connect(self.action_triggered)
        # Center align
        for i in range(self.layout.count()):
            is_tool_button = isinstance(self.layout.itemAt(i).widget(), QtWidgets.QToolButton)
            if is_tool_button:
                self.layout.itemAt(i).setAlignment(QtCore.Qt.AlignCenter)

    def addActions(self, actions):
        utils.addActions(self, actions)

    def moveEvent(self, ev):
        print("moveEvent", ev)
    
    def toggleViewAction(self):
        logger.info("toggleViewAction")

    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        pass

    def action_triggered(self):
        logger.info('action triggered')
        for i in range(self.layout.count()):  # 遍历所有的widget
            w = self.layout.itemAt(i).widget()
            
            if not isinstance(w, QtWidgets.QToolButton):  # 如果不是QToolButton则不做任何操作
                continue
            a = w.defaultAction()  # action
            print(a.isChecked(), a.isEnabled(), a.isCheckable())
        self.repaint()
        

    def hover_event(self, current_text):
        return
        print("hoverEnterEvent", current_text)
        # print all widgets's state
        c_text = current_text
        for i in range(self.layout.count()):  # 遍历所有的widget
            w = self.layout.itemAt(i).widget()
            if not isinstance(w, QtWidgets.QToolButton):  # 如果不是QToolButton则不做任何操作
                continue
            a = w.defaultAction()  # action
            if a.text() == c_text:
                color = (255, 255, 255)
            else:
                color = (128, 128, 128)
            a.setIcon(a._icon_stem, color=color)
            


