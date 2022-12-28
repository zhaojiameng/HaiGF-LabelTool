
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from pathlib import Path

from ..title_bar import TitleBarWithAction

def get_main_side_bar(parent=None, **kwargs):
    return MainSideBar(parent=parent, **kwargs)

class MainSideBar(QtWidgets.QDockWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        title = kwargs.pop('title', 'Main Side Bar Title')
        self.setWindowTitle(title)
        # 添加一个带Action的标题栏
        self.title_bar = TitleBarWithAction()  # QFrame()
        self.setTitleBarWidget(self.title_bar)
        # 添加一个默认的页面
        default_page = QtWidgets.QLabel()
        default_page.setText('Default Page')
        # self.layout.addWidget(default_page)

        # self.setFixedWidth(200)
        default_widget = self.get_example_widget()
    
        self.setWidget(default_widget)
        self.setupProperty()

    def get_example_widget(self):
        """一个示例页面"""
        return ExampleWidget(parent=self)

    def setupProperty(self):
        self.setMinimumSize(QtCore.QSize(50, 0))


class ExampleWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 文件系统
        self.model = QFileSystemModel()
        self.model.setRootPath(f"{Path.home()}")
        
        self.tree = QTreeView()
        self.tree.setWindowTitle('title')
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(f"{Path.home()}"))

        self.layout.addWidget(self.tree)



