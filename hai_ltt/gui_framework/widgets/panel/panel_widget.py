from PySide2.QtWidgets import *

from .. import HTabWidget, HTabBar
from ..central_widgets.start_page import HStartPage
from hai_ltt.apis import HGF

def get_panel_widget(parent=None, **kwargs):
    panel_widget = PanelWidget(parent=parent, **kwargs)
    # page = HStartPage(parent=panel_widget, **kwargs)
    # panel_widget.setPages([page])
    return panel_widget


class PanelWidget(QDockWidget):
    """是dock，但有TabWidget的属性"""
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent

        tab_bar_widget = DockTitleBar(parent=self)
        self.setTitleBarWidget(tab_bar_widget)

        self._pages = []

        self.setup_ui()
        # self.titleBarWidget().setStyleSheet('background-color: rgb(120, 23, 10);')
        # 设置背景蓝色
        # self.setStyleSheet('background-color: rgb(120, 23, 120);')

    @property
    def c_idx(self):
        return self.tabBar().c_idx

    def setup_ui(self):
        # 不可移动
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        # dock添加一个widget
        page = QTextBrowser()
        page.setText('Outputs: ')
        page.setFrameShape(QFrame.NoFrame)
        page2 = QTextEdit()
        page2.setFrameShape(QFrame.NoFrame)
        page2.setText('>>Please input something: ')
        self.add_tab('Output', page, tip='Output (Command+Shift+U)')
        self.add_tab('Terminal', page2, tip='Terminal (Command+`)')

        self.load()

    def add_tab(self, title, page, tip=None):
        self._pages.append(page)
        # tab = QWidget()
        self.tabBar().add_tab(title)
        if tip:
            self.tabBar().setTabToolTip(self.tabBar().count() - 1, tip)

    def clear_tabs(self):
        self._pages = []
        self.tabBar().clear()

    def tabBar(self):
        return self.titleBarWidget().children()[0]

    def load(self):
        """根据c_idx加载page, 其他page隐藏"""
        self.setWidget(self._pages[self.c_idx])
        # for i, page in enumerate(self._pages):
            # if i == self.c_idx:
                # page.show()
                # 
            # else:
                # page.hide()


class DockTitleBar(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent

        tab_bar = DockTabBar(parent=self)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 添加一个stretch，使得tab_bar靠左
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(tab_bar)
        # layout.addStretch()
        layout.addWidget(spacer)
        
        self.setLayout(layout)

        # 标题栏的背景颜色
        self.setStyleSheet(
            f'background-color: {HGF.COLORS.WhiteSmoke};')
                # color: {HGF.COLORS.Blue};')  # 字体颜色

    
class DockTabBar(QTabBar):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        # self.addTab('Output')
        # self.addTab('Terminal')
        self.setExpanding(False)
        self.c_idx = 0

        # 设置tab无背景
        # self.setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(122, 112, 33);')

    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        self.c_idx = self.tabAt(ev.pos())
        self.p.p.load()

    def add_tab(self, title):
        self.addTab(title)
        
        

    
        

