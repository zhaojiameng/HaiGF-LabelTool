

from PySide2.QtCore import QSize, Slot, QPoint
from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QDockWidget)
import damei as dm
import numpy as np

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

        self.shadow_tabbar = None  # 影子

        self.paint_flag = 0

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


    def moving_tab(self, ev, shadow_tabbar):
        """移动tab"""
        # logger.info(f"moving_tab")
        st = shadow_tabbar

        # 移动和显示影子tab bar
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))  # 获取鼠标在tab widget中的位置
        st.setParent(self)
        x = ev_posw.x() - st.width() / 2
        y = ev_posw.y() - st.height() / 2
        st.move(x, y)
        st.show()

        # 根据鼠标位置绘制page的一半的背景
        cw = self.currentWidget()
        lurbc = self.pos2lurbc(ev)  # 鼠标位置对应的左上右下中心
        # cw.update(lurbc=lurbc)
        if self.paint_flag == 0:
            self.paint_flag = 1
            cw.paint_lurbc(lurbc=lurbc)

    def pos2lurbc(self, ev):
        """pos to left, up, right, bottom, center"""
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))
        x, y = ev_posw.x(), ev_posw.y()
        w, h = self.size().width(), self.size().height()
        # print(f'ev_posw={ev_posw}, self_size={w} {h}')
        
        """
        以宽和高的1/4和3/4为界限，分为5个区域
        """
        control_points = ((w/4, h/4), (w*3/4, h*3/4))
        cps = control_points
        if x < cps[0][0]:  # 0~1/4
            if y < cps[0][1]:
                # 判断左上
                line = (0, 0), (w / 3, h / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                return 'left' if cross >= 0 else 'up'
            elif y < cps[1][1]:
                return 'left'
            else:
                # 判断左下
                line = (0, h), (w / 3, h * 2 / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                # return 'left' if cross >= 0 else 'bottom'
                return 'bottom' if cross >= 0 else 'left'
        elif x < cps[1][0]:  # [1/3, 2/3]
            if y < cps[0][1]:
                return 'up'
            elif y < cps[1][1]:
                return 'center'
            else:
                return 'bottom'
        else:  # [2/3, 1]
            if y < cps[0][1]:
                # 判断右上
                line = (w, 0), (w * 2 / 3, h / 3)
                cross = self.point_vs_line(p=(x, y), line=line)
                return 'up' if cross >= 0 else 'right'
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

        




    




    