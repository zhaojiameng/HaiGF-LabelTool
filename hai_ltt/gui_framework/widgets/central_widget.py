
from PySide2.QtCore import QRect, Qt, QByteArray
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QSpacerItem, QSplitter, QFrame,
    QGridLayout)

from .tab_widget import TabWidget, get_tab_widget, Page
from .. import utils

def get_central_widget(parent=None):
    return CentralWidget(parent=parent)

class CentralWidget(QWidget):
    """Qsplitter切分，内容是TabWidget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mw = parent
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.splitter)
        state = parent.settings.value("splitter/state", QByteArray())
        self.splitter.restoreState(state)

        self._start_page()
        
    def _start_page(self, **kwargs):
        mw = self.mw
        from .pages.start_page import StartPage
        # 先创建页面
        # page = Page(parent=mw, **kwargs)  # 是一个QWidget
        start_page = StartPage(parent=self, **kwargs)
        page2 = Page(parent=self, **kwargs)
        tab_widget = get_tab_widget(parent=self.mw)

        tab_widget.addTab(
            start_page, 
            utils.newIcon("start"), 
            mw.tr("Start")) 
        tab_widget.addTab(
            page2, 
            mw.tr("Page2"))

        self.load([tab_widget])

    def closeEvent(self, event):
        self.parent.settings.setValue("splitter/state", self.splitter.saveState())
        
    def load(self, tab_widgets):
        """加载TabWidget"""
        # 清除所有的子控件
        # for i in reversed(range(self.layout.count())):
            # self.layout.itemAt(i).widget().setParent(None)
        for tab_widget in tab_widgets:
            # spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            # self.layout.addWidget(tab_widget)
            self.splitter.addWidget(tab_widget)




        


