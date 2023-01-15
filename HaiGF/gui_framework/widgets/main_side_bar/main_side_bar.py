
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from pathlib import Path
import damei as dm

from HaiGF.apis import HGF, root_path, __appname__
from ..common.title_bar_with_action import TitleBarWithAction
from ..common.blue_button import BlueButton
from ..common.hai_msb_widget import HMainSideBarWidget
from .explorer_widget import ExplorerWidget

logger = dm.get_logger('main_side_bar')

def get_main_side_bar(parent=None, **kwargs):
    return MainSideBar(parent=parent, **kwargs)

class MainSideBar(QtWidgets.QDockWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.mw = parent
        title = kwargs.pop('title', 'Main Side Bar Title')
        self.setWindowTitle(title)
        self.setObjectName('MainSideBar')

        self._aw_dict = {}  # action: widget
        self.c_widget = None  # current widget

        # 1.标题栏，带有按钮
        self.title_bar = TitleBarWithAction()  # QFrame()
        self.setTitleBarWidget(self.title_bar)
        # 2.默认界面
        self.default_widget = self.get_example_widget()
        self.setWidget(self.default_widget)
        self.setupProperty()

    def add_widget(self, widget, action):
        """添加一个widget, 对应一个action"""
        # self._widgets.append(widget)
        assert action not in self._aw_dict.keys(), f'action {action} already exists'
        self._aw_dict[action] = widget
        self.load_widget_by_action(action)

    def load(self, widget, title=None, title_actions=None):
        """重新加载"""
        self.c_widget = widget
        if widget:
            self.setWidget(widget)
        title = title if title not in [None, 'Title'] else widget.title
        title_actions = title_actions if title_actions else widget.title_actions
        
        self.title_bar.set_title(title)
        self.title_bar.set_title_actions(title_actions)
        self.title_bar.load()
        self.c_widget.load()

    def get_example_widget(self):
        """一个示例页面"""
        return ExampleWidget(parent=self)

    def setupProperty(self):
        self.setMinimumSize(QtCore.QSize(50, 0))
        self.setFeatures(QDockWidget.DockWidgetMovable)
        # 设置边框
        self.setStyleSheet('border: 1px solid #d9d9d9;')

    def load_widget_by_action(self, action, *args, **kwargs):
        """根据action加载widget"""
        # print(f'load_widget_by_action: {action}')
        widget = self._aw_dict.get(action, self.default_widget)
        title = widget.windowTitle()
        title = 'Title' if title == '' else title
        if hasattr(widget, 'title_actions'):
            title_actions = widget.title_actions
        else:
            title_actions = None
        # print(f'load_widget_by_action: {title} {title_actions}')
        self.load(widget=widget, title=title, title_actions=title_actions, *args, **kwargs)
    
    def load_widget_by_name(self, name, *args, **kwargs):
        """根据widget的name加载widget"""
        dir = kwargs.pop('dir', None)
        # print(f'load_widget_by_name: {name} {dir}')
        flag = False
        for action, widget in self._aw_dict.items():
            if widget.objectName() == name:
                if dir:
                    widget.set_dir(dir)
                self.load_widget_by_action(action, *args, **kwargs)
                flag = True
                break
        if not flag:
            logger.warning(f'`load_widget_by_name` widget {name} not found')


class ExampleWidget(HMainSideBarWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        label = QLabel(self.tr(
            'Empty widget, use "msb.add_widget(w, a)" to bind widget with an action.'))
        label.setFont(HGF.FONT)
        label.setWordWrap(True)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(spacer)
        self.setLayout(self.layout)

        


