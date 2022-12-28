"""
带有按钮的标题栏
"""

from PySide2 import QtCore
from PySide2 import QtWidgets

from .. import utils

class TitilBarWithAction(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.layout = QtWidgets.QHBoxLayout(self)

        self.title_label = QtWidgets.QLabel('Title Bar')

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        spacer.setStyleSheet("background-color: rgb(0, 0, 100);")
        
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(8, 8))
        # 设置action的样式
        self.toolbar.setStyleSheet("QToolBar {border: 0px;}")
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(spacer)
        self.layout.addWidget(self.toolbar)

        default_actions = [
            utils.newAction(
                parent=self,
                text='Title Bar Action',
                icon='more',
            )
        ]
        self.addActions(default_actions)

        # 固定高度
        # self.setFixedHeig

        # 设置控件前后景色
        # self.parent.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        self.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        
    def addAction(self, action):
        # self.layout.addAction(action)
        # 设置act
        self.toolbar.addAction(action)

    def addActions(self, actions):
        for action in actions:
            self.addAction(action)



         
