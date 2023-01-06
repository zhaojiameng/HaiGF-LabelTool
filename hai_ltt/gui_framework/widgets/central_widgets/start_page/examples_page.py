from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from .hai_page import HPage

class HExamplesPage(HPage):
    """单个页面，包含ToolBar和Page"""
    def __init__(self, parent=None, **kwargs):
        # print(parent, 'parent')
        icon = kwargs.pop('icon', None)
        title = kwargs.pop('title', 'Examples')
        super().__init__(parent, icon=icon, title=title, **kwargs)
        self.mw = parent
        tool_bar = kwargs.pop("tool_bar", None)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 设置Frameless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
        # 设置工具栏
        self.setupToolBar(tool_bar=tool_bar)

    def default_tool_bar(self):
        # tool_bar = get_toolbar(title='PageToolBar', parent=self.parent)
        # mw = self.mw
        # actions = [mw.actions.explorer_action]
        # tool_bar.addActions(actions)
        tool_bar = QWidget()
        tool_bar.setLayout(QHBoxLayout())
        tool_bar.layout().addWidget(QLabel("PageToolBar"))
        return tool_bar

    def setupToolBar(self, tool_bar=None):
        tool_bar = tool_bar if tool_bar else self.default_tool_bar()
        self.layout.addWidget(tool_bar)