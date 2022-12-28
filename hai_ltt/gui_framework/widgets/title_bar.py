"""
带有按钮的标题栏
"""

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from .. import utils
from hai_ltt.apis import HGF

class TitleBarWithAction(QtWidgets.QFrame):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 5, 10, 5)

        self.title_label = QtWidgets.QLabel(f'Title')
        # 设置字体尺寸
        font = QtGui.QFont()
        font.setFamily(HGF.FONT_FAMILY)
        font.setPointSize(10)
        self.title_label.setFont(font)
        # 设置文本颜色
        # self.title_label.setStyleSheet("color: rgb(100, 100, 100);")

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(10, 10))
        # 设置action的样式
        # self.toolbar.setStyleSheet("QToolBar {border: 0px;background-color: rgb(122, 0, 255);}")
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(spacer)
        self.layout.addWidget(self.toolbar)
        # self.addWidgets([self.title_label, spacer, self.toolbar])

        action = utils.newAction(
                parent=self,
                text='Title Bar Action',
                icon='more',)
        default_actions = [action]
        self.addActions(default_actions)

        # 设置显示边框
        # self.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        # 设置控件前后景色， #DCDCDC亮灰色，#808080灰色
        self.setStyleSheet("background-color: #DCDCDC; color: #808080;")
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
    def addAction(self, action):
        # self.layout.addAction(action)
        # 设置act
        self.toolbar.addAction(action)

    def addActions(self, actions):
        for action in actions:
            self.addAction(action)



         
