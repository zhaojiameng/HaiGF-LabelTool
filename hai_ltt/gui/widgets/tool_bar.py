from PySide2 import QtCore
from PySide2 import QtWidgets
from .. import utils


def get_toolbar(title, actions=None):
    """
    创建一个工具栏
    """
    toolbar = ToolBar(title)
    toolbar.setObjectName(f"{title}ToolBar")
    # toolbar.setOrientation(Qt.Vertical)
    toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
    if actions:
        utils.addActions(toolbar, actions)
    return toolbar

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, title):
        super(ToolBar, self).__init__(title)
        layout = self.layout()
        m = (0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setContentsMargins(*m)  # 设置左顶右底的边距
        self.setContentsMargins(*m)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setMovable(False)
        # 设置背景颜色灰色
        # self.setStyleSheet("background-color: rgb(50, 50, 50);")
        
    def addAction(self, action):
        if isinstance(action, QtWidgets.QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = QtWidgets.QToolButton()
        btn.setDefaultAction(action)
        # btn.setToolButtonStyle(self.toolButtonStyle())  # 设置后会同时显示icon和text
        self.addWidget(btn)
        # Center align
        for i in range(self.layout().count()):
            is_tool_button = isinstance(self.layout().itemAt(i).widget(), QtWidgets.QToolButton)
            # print(i, is_tool_button, self.layout().itemAt(i))
            if is_tool_button:
                self.layout().itemAt(i).setAlignment(QtCore.Qt.AlignCenter)
                # QtCore.Qt.AlignBottom

    def addActions(self, actions):
        utils.addActions(self, actions)
