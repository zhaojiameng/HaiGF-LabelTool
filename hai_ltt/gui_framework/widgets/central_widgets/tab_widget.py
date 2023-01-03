

from PySide2.QtCore import QSize, Slot
from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QDockWidget)
import damei as dm

from ... import utils
from ..core_func_bar.tool_bar import get_toolbar, ToolBar
from .start_page import HStartPage, HExamplesPage
from .hai_tab_bar import HTabBar

logger = dm.get_logger('tab_widget')



def get_start_tab_widget(parent=None, **kwargs):
    """tab widget包含n个tab和n个page，每个tab对应一个page"""
    tab_widget = HTabWidget(parent=parent, **kwargs)  # 空界面
    page1_start = HStartPage(parent=tab_widget, **kwargs)
    page2_examples = HExamplesPage(parent=tab_widget, **kwargs)

    pages = [page1_start, page2_examples]
    # pages = [page1_start]
    tab_widget.setPages(pages)

    return tab_widget


class HTabWidget(QTabWidget):
    """
    包含TabBar、ToolBar和Page的组合控件
    先写一个默认的控件Table
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.parent = parent
        # self.mw = parent
        self.tab_bar = HTabBar(self)  # 空的tab bar

        self.setWindowTitle(f"TabWidget")
        self.setObjectName(f"TabWidget")

        # self.layout().setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.setTabShape(QTabWidget.Rounded)
        self.setTabsClosable(True)
        self.usesScrollButtons()
        self.setMovable(True)

        self.shadow_tabbar = QTabBar(self)  # 影子

        # self.tab_bar.addTab(utils.newIcon("start"), self.tr("Start"))
        # self.tabBarClicked.connect(self.tabBarClicked)

    def setPages(self, pages):
        """添加pages"""
        # new_idx = len(self.tab_widgets)
        # logger.info(f'Create new TabWidget, idx={new_idx}')
        # tab_widget.setObjectName(f"TabWidget{new_idx}")
        # tab_widget.tabBarClicked.connect(self.on_tabBarClicked)
        # tab_widget.tabBarDoubleClicked.connect(self.on_tabBarDoubleClicked)
        # tab_widget.tabBar().tabMoved.connect(self.on_tabMoved)
        
        # 移除tab bar里的所有tab
        for i in range(self.tab_bar.count()):
            self.tab_bar.removeTab(0)
        # 移除tab widget里的所有tab
        for i in range(self.count()):
            self.removeTab(0)

        for page in pages:
            # print('xx', page.parent)
            self.addTab(page, 'test title')  # 添加一个page
            if page.icon and page.title:
                self.tab_bar.addTab(page.icon, page.title)
            elif not page.icon and page.title:
                self.tab_bar.addTab(page.title)
            else:
                raise ValueError("page.icon and page.title can't be None at the same time")
        
        self.setTabBar(self.tab_bar)

    # def mousePressEvent(self, ev):
    #     logger.info(f"mousePressEvent {ev}")

    # def mouseMoveEvent(self, ev):
    #     logger.info(f"mouseMoveEvent {ev}")


    def moving_tab(self, ev, shadow_tabbar):
        """移动tab"""
        logger.info(f"moving_tab")
        self.shadow_tabbar = shadow_tabbar
        # self.shadow_tabbar.setTabText('xxx')

        c_page = self.currentWidget()  # 当前page
        # self.shadow_tabbar.setParent(c_page)
        self.shadow_tabbar.setParent(self)

        # self.shadow_tabbar.addTab('xx')
        self.shadow_tabbar.show()
        self.shadow_tabbar.move(ev.x(), ev.y())



    




    