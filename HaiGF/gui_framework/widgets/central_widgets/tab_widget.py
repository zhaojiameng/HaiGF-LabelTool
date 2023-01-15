

from PySide2.QtCore import QSize, Slot, QPoint
from PySide2.QtGui import QIcon, Qt, QPainter, QColor
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QDockWidget)
import damei as dm
import numpy as np

from HaiGF.gui_framework import utils
from ..core_func_bar.tool_bar import get_toolbar, ToolBar
from .start_page import HStartPage, HExamplesPage, ExamplePage
from .hai_tab_bar import HTabBar

logger = dm.get_logger('tab_widget')



def get_start_tab_widget(parent=None, **kwargs):
    """tab widget包含n个tab和n个page，每个tab对应一个page"""
    tab_widget = HTabWidget(parent=parent, **kwargs)  # 空界面
    page1_start = HStartPage(parent=tab_widget, **kwargs)
    page2_examples = ExamplePage(parent=tab_widget, title='Examples', **kwargs)
    # page2_examples = HExamplesPage(parent=tab_widget, title='Examples', **kwargs)

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
        self.p = parent
        self.setWindowTitle(f"HTabWidget")

        self.setContentsMargins(0, 0, 0, 0)

        self.setTabShape(QTabWidget.Rounded)
        self.setTabsClosable(True)
        self.usesScrollButtons()
        self.setMovable(True)

        self._pages = []

        # self.tab_bar.addTab(utils.newIcon("start"), self.tr("Start"))
        # self.tabBarClicked.connect(self.tabBarClicked)

    @property
    def c_idx(self):
        return self.tabBar().c_idx
    
    @property
    def pages(self):
        return self._pages

    def removeTab(self, index):
        self._pages.pop(index)
        return super().removeTab(index)
        

    def setPages(self, pages):
        """设置pages"""
        self._pages = pages
        self.load_pages()

    def addPage(self, page, load=True):
        """添加page"""
        if page not in self._pages:
            self._pages.append(page)
        if load:
            self.load_pages()

    def addPages(self, pages):
        """添加pages"""
        for page in pages:
            self.addPage(page, load=False)
        self.load_pages()
    
    def insertPage(self, index, page):
        """插入page"""
        if page not in self._pages:
            self._pages.insert(index, page)
        self.load_pages()

    def load_pages(self):
        """加载pages"""
        # 移除tab bar里的所有tab
        # if self.tab_bar is not None:
            # self.tab_bar.setParent(None)
        tab_bar = HTabBar(self)
        tab_bar.show()
        
        for i, page in enumerate(self._pages):
            # print(f'[{i+1}/{len(self._pages)}] page: {page.title}')
            # print('xx', page.parent)
            self.addTab(page, 'test title')  # 添加一个page
            # 设置tab bar的tab
            if page.icon and page.title:
                tab_bar.addTab(page.icon, page.title)
            elif not page.icon and page.title:
                tab_bar.addTab(page.title)
            else:
                raise ValueError("page.icon and page.title can't be None at the same time")
        
        # tab_bar设置stretch
        # tab_bar.setStretchLastSection(True)
        self.setTabBar(tab_bar)
        

    def mask_page(self, ev):
        """遮罩当前page"""
        cw = self.currentWidget()  # 这个是指哪个的page
        mr = self.pos2mask_region(ev)  # 获取鼠标位置对应左上右下中心的哪一个
        cw.mask_region(mr)

    def clear_mask(self):
        # cw = self.currentWidget()
        # print('clear mask, cw:', cw)
        # self.currentWidget().clear_mask()
        self._pages[self.c_idx].clear_mask()


    def pos2mask_region(self, ev, control_points=None):
        """
        以宽和高的1/4和3/4为控制点，把self分为5个区域left, top, right, bottom, center
        返回当前鼠标位置对应的区域
        return: 'left', 'top', 'right', 'bottom', 'center'
        """
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))  # 获取鼠标在tab widget中的位置
        x, y = ev_posw.x(), ev_posw.y()
        w, h = self.size().width(), self.size().height()  # self的宽和高
        control_points = ((w/4, h/4), (w*3/4, h*3/4)) if control_points is None else control_points
        
        cps = control_points
        if x < cps[0][0]:  # 0~1/4
            if y < cps[0][1]:
                # 判断左上
                line = (0, 0), (w / 3, h / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                return 'left' if cross >= 0 else 'top'
            elif y < cps[1][1]:
                return 'left'
            else:
                # 判断左下
                line = (0, h), (w / 3, h * 2 / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                return 'bottom' if cross >= 0 else 'left'
        elif x < cps[1][0]:  # [1/3, 2/3]
            if y < cps[0][1]:
                return 'top'
            elif y < cps[1][1]:
                return 'center'
            else:
                return 'bottom'
        else:  # [2/3, 1]
            if y < cps[0][1]:
                # 判断右上
                line = (w, 0), (w * 2 / 3, h / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                return 'top' if cross >= 0 else 'right'
            elif y < cps[1][1]:
                return 'right'
            else:
                # 判断右下
                line = (w, h), (w * 2 / 3, h * 2 / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                # return 'bottom' if cross >= 0 else 'right'
                return 'right' if cross >= 0 else 'bottom'
        

    @staticmethod
    def point_vs_line(p, line):
        """
        判断点p在直线line的哪一侧
        计算AB和AC的叉积，如果大于0，说明点p在直线line的左侧，否则在右侧
        返回在线的左侧还是右侧
        """
        x1, y1 = line[0]
        x2, y2 = line[1]
        x, y = p
        AB = np.array([x2 - x1, y2 - y1])
        AC = np.array([x - x1, y - y1])
        ret = np.cross(AB, AC)
        return ret

    def remove_current_page(self):
        """移除当前page"""
        c_idx = self.tabBar().c_idx
        cpage = self._pages[c_idx]
        pages = [x for x in self._pages if x != cpage]
        self.setPages(pages)
        # self.print_pages_name()

    def print_pages_name(self):
        for page in self._pages:
            print('page_title', page.title)
        print('tabbar count: ', self.tabBar().count())

    def add_tab_from_another_tabw(self, tabw2):
        """把tabw2当前tab的page添加到self中"""
        page = tabw2.currentWidget()
        pages = self._pages + [page]
        self.setPages(pages)
        # tabw.setPages([page])



        




    




    