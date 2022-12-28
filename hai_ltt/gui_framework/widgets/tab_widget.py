

from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QDockWidget)

from .. import utils
from .tool_bar import get_toolbar, ToolBar


def get_tab_widget(parent=None, **kwargs):
    tab_widget = TabWidget(parent=parent, **kwargs)
    return tab_widget


class TabWidget(QTabWidget):
    """
    包含TabBar、ToolBar和Page的组合控件
    # 先写一个默认的控件Table
    """
    def __init__(self, parent=None, pages=None, **kwargs):
        super().__init__(parent)
        self.mw = parent

        self.setWindowTitle(f"TabWidget")

        self.setTabShape(QTabWidget.Rounded)
        self.setTabsClosable(True)
        self.usesScrollButtons()

        # 设置可调整控件大小
        # self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        # 设置边框颜色
        # self.setStyleSheet("border-right: 1px solid rgb(0, 255, 255);")
    

class Page(QWidget):
    """单个页面，包含ToolBar和Page"""
    def __init__(self, parent=None, **kwargs):
        # print(parent, 'parent')
        super().__init__(parent)
        self.mw = parent
        tool_bar = kwargs.pop("tool_bar", None)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
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


    def a(self):

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.addWidget(QLabel("TabBar"))

        # 列表
        list_widget = QListWidget()
        list_widget.setFixedWidth(100)

        btn = QPushButton("TabBar")
        btn.setIcon(utils.newIcon("anno"))
        list_widget.addItem(QListWidgetItem(btn.icon(), "TabBar"))

        # self.layout.addWidget(btn)
        self.layout.addWidget(list_widget)
        
        # 设置图标
        self.setWindowIcon(utils.newIcon("anno"))

        # 设置高度
        self.setFixedHeight(30)

        # 设置背景色
        self.setStyleSheet("background-color: rgb(255, 0, 0);")


    




    