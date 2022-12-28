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

        # 1.标题文本
        self.title_label = QtWidgets.QLabel(f'Title')
        font = QtGui.QFont()
        font.setFamily(HGF.FONT_FAMILY)
        font.setPointSize(HGF.FONT_SIZE)
        self.title_label.setFont(font)
        # self.title_label.setStyleSheet("color: rgb(100, 100, 100);")

        # 2.占位符
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # 3.标题右侧的工具按钮
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(HGF.FONT_SIZE, HGF.FONT_SIZE))
        action = utils.newAction(
                parent=self,
                text='Title Bar Action',
                icon='more',)
        default_actions = [action]
        self.addActions(default_actions)
        # 设置action的样式
        # self.toolbar.setStyleSheet("QToolBar {border: 0px;background-color: rgb(122, 0, 255);}")
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(spacer)
        self.layout.addWidget(self.toolbar)

        # 设置控件前后景色， #DCDCDC亮灰色，#808080灰色
        self.setStyleSheet(
            f"background-color: {HGF.COLORS.Gainsboro}; \
            color: {HGF.COLORS.LightBlack};")
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
    def addAction(self, action):
        # self.layout.addAction(action)
        # 设置act
        self.toolbar.addAction(action)

    def addActions(self, actions):
        for action in actions:
            self.addAction(action)



         
