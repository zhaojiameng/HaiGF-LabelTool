

from PySide2.QtCore import QSize, Slot
from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QDockWidget)
import damei as dm

from .. import utils
from .tool_bar import get_toolbar, ToolBar

logger = dm.get_logger('tab_widget')


def get_tab_widget(parent=None, **kwargs):
    tab_widget = TabWidget(parent=parent, **kwargs)
    return tab_widget


class TabWidget(QTabWidget):
    """
    包含TabBar、ToolBar和Page的组合控件
    先写一个默认的控件Table
    """
    def __init__(self, parent=None, pages=None, **kwargs):
        super().__init__(parent)
        self.mw = parent

        self.setWindowTitle(f"TabWidget")
        self.setObjectName(f"TabWidget")

        # self.layout().setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.setTabShape(QTabWidget.Rounded)
        self.setTabsClosable(True)
        self.usesScrollButtons()
        self.setMovable(True)
        

        # self.tabBarClicked.connect(self.tabBarClicked)

    # def mousePressEvent(self, ev):
    #     logger.info(f"mousePressEvent {ev}")

    # def mouseMoveEvent(self, ev):
    #     logger.info(f"mouseMoveEvent {ev}")
    

class Page(QWidget):
    """单个页面，包含ToolBar和Page"""
    def __init__(self, parent=None, **kwargs):
        # print(parent, 'parent')
        super().__init__(parent)
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


    




    