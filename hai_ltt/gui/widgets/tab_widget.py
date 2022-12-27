

from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QDockWidget)

from .. import utils


def get_tab_widget(parent=None, **kwargs):
    return TabWidget(parent=parent, **kwargs)

# class TabWidget(QDockWidget):
# class TabWidget(QWidget):
class TabWidget(QTabWidget):
    """包含TabBar、ToolBar和Page的组合控件"""
    def __init__(self, parent=None, id=0):
        super().__init__(parent)

        self.setWindowTitle(f"TabWidget {id}")

        # self.layout = QVBoxLayout(self)
        # self.layout.setSpacing(0)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.setIcon(utils.newIcon("anno"))
        self.setMovable(True)  # TabBar可移动
        # self.setIconSize(QSize(16, 16))  # 设置图标大小，默认16x16
        
        tab_bar = TabBar()
        label = QLabel(f"TabWidget {id}")
        label2 = QLabel(f"TabWidget2 {id}")
        
        # self.layout.addWidget(tab_bar)
        # self.layout.addWidget(label)
        # self.layout.addWidget(label2)
        self.addTab(tab_bar, utils.newIcon("ai"), "TabBar")
        self.addTab(label, "Label")
        # self.setTabIcon(0, utils.newIcon("ai"))
        self.setTabShape(QTabWidget.Rounded)
        self.setTabsClosable(True)
        self.usesScrollButtons()

        # 设置可调整控件大小

        # self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        
        # 设置边框颜色
        # self.setStyleSheet("border-right: 1px solid rgb(0, 255, 255);")



class TabBar(QWidget):
    """选项卡，包含多个Tab, 每个Tab包含图标、标题、关闭按钮"""
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

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


    




    