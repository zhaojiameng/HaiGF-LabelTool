
from PySide2 import QtCore
from PySide2 import QtWidgets

from ..title_bar import TitilBarWithAction

def get_main_side_bar(parent=None, **kwargs):
    main_side_bar = MainSideBar(parent=parent, **kwargs)
    return main_side_bar

class MainSideBar(QtWidgets.QDockWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        self.setWindowTitle('Main Side Bar Title')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 添加一个带Action的标题栏
        self.title_bar = TitilBarWithAction()
        self.setTitleBarWidget(self.title_bar)
        # 添加一个树形控件
        # self.tree_widget = QtWidgets.QTreeWidget(parent=self)
    
        # self.layout.addWidget(self.title_bar)
        # self.layout.addWidget(self.tree_widget)

        self.setFixedWidth(200)



