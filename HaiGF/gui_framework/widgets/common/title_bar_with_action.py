"""
带有按钮的标题栏
"""

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from ... import utils
from HaiGF.apis import HGF

class TitleBarWithAction(QtWidgets.QWidget):
    """带有按钮的标题栏, 是QWidget的子类"""
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.p = parent

        self._title = kwargs.pop('title', 'Title')
        self._title_actions = kwargs.pop('title_actions', self.get_default_actions())

        # 1.标题文本
        self.title_bar = TitleTextBar(self)

        # 2.占位符
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # 设置绿色
        # spacer.setStyleSheet("background-color: green;")
        # 3.标题右侧的工具按钮
        self.toolbar = TitleToolBar(parent=self)
        self.toolbar.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)

        # x.总体布局
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title_bar)
        self.layout.addWidget(spacer)
        self.layout.addWidget(self.toolbar)

        # 设置控件前后景色， #DCDCDC亮灰色，#808080灰色
        # self.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.setStyleSheet(
            f"background-color: {HGF.COLORS.Gainsboro};")
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    
    @property
    def title(self):
        return self._title

    @property
    def title_actions(self):
        return self._title_actions
    
    def set_title(self, title):
        self._title = title

    def set_title_actions(self, actions):
        self._title_actions = actions

    def get_default_actions(self):
        action = utils.newAction(
                parent=self,
                text='Title Bar Action',
                icon='more',)
        default_actions = [action]
        return default_actions

    def load(self):
        # self.title_label.setFont(HGF.FONT)
        self.toolbar.setIconSize(QtCore.QSize(HGF.FONT_SIZE, HGF.FONT_SIZE))
        
        # print(self._title)
        # print(self._title_actions)
        actions = self._title_actions
        # 设置标题
        self.title_bar.setTabText(0, self._title)
        # 设置右侧的工具按钮
        # 清空
        self.toolbar.clear()
        if actions is None or len(actions) == 0:
            self.toolbar.hide()
        else:
            self.toolbar.add_actions(self._title_actions)
            self.toolbar.show()

class TitleTextBar(QtWidgets.QTabBar):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.p = parent
        # self.title_label = QtWidgets.QLabel(f'Title')
        self.addTab('title')
        self.setExpanding(False)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setFont(HGF.TAB_FONT)

    def paintEvent(self, ev):
        # super().paintEvent(ev)
        p = QtGui.QPainter(self)
        p.setPen(QtGui.QPen(HGF.COLORS.Black))
        # p.setFont(HGF.FONT)
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self.tabText(0))


class TitleToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.p = parent

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(QtCore.Qt.AlignRight)

        # self.setMinimumSize(20, 20)
        # self.setMaximumSize(100, 100)
        # print(self.sizeHint(), 'sizeHint')
        # self.setIconSize(QtCore.QSize(48, 48))

        self._tool_btns = []
       
    def add_action(self, action):
        if isinstance(action, QtWidgets.QWidgetAction):
            return super(TitleToolBar, self).addAction(action)
        # print(action, 'xxx')
        btn = QtWidgets.QToolButton()
        btn.setDefaultAction(action)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self._tool_btns.append(btn)
        self.addWidget(btn)
        # self.toolbar.addAction(action)
        # 中央对齐
        for i in range(self.layout().count()):
            btn_i = self.layout().itemAt(i)
            if isinstance(btn_i, QtWidgets.QToolButton):
                btn_i.setAlignment(QtCore.Qt.AlignCenter)

    def add_actions(self, actions):
        for action in actions:
            self.add_action(action)     
