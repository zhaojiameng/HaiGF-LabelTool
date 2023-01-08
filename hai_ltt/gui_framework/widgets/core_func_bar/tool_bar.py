from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from ... import utils
from hai_ltt.apis import HGF


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

    def paintEvent(self, ev):
        # 绘制背景为红色
        painter = QtWidgets.QStylePainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QColor(HGF.CORE_FUNC_BAR_BACKGOUND_COLOR))
        painter.drawRect(self.rect())
    
        # 设置背景颜色灰色
        self.setStyleSheet(F"background-color: {HGF.CORE_FUNC_BAR_BACKGOUND_COLOR};")
        painter.end()
        
    def addAction(self, action):
        if isinstance(action, QtWidgets.QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = QtWidgets.QToolButton()
        # btn.setStyleSheet("background-color: rgb(10, 10, 10);")
        # 设置btn的Action填充满整个btn
        btn.setDefaultAction(action)
        self.addWidget(btn)
        # Center align
        for i in range(self.layout.count()):
            is_tool_button = isinstance(self.layout.itemAt(i).widget(), QtWidgets.QToolButton)
            if is_tool_button:
                self.layout.itemAt(i).setAlignment(QtCore.Qt.AlignCenter)

    def addActions(self, actions):
        utils.addActions(self, actions)
