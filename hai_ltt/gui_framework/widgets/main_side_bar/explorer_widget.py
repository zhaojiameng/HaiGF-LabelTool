
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from pathlib import Path

import damei as dm

logger = dm.get_logger('explorer_widget')

class ExplorerWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.dir = kwargs.pop('dir', Path.home())
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 文件系统
        self.model = QFileSystemModel()
        self.model.setRootPath(f"/")

        # 树
        self.tree = QTreeView()
        self.tree.setWindowTitle('title')
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(f'{self.dir}'))
        # self.tree.setHeaderHidden(True)
        self.tree.setColumnWidth(0, 250)


        self.layout.addWidget(self.tree)

    def mouseDoubleClickEvent(self, ev):
        logger.debug(f'mouseDoubleClickEvent, ev={ev}')
