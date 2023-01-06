
from PySide2.QtCore import QRect, Qt, QByteArray, Slot, QPoint
from PySide2.QtGui import QCursor, QKeySequence, QMouseEvent
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QSpacerItem, QSplitter, QFrame,
    QGridLayout)

import damei as dm

from hai_ltt.apis import HGF
from .tab_widget import HTabWidget, get_start_tab_widget
from .hai_tab_bar import HTabBar
from .start_page import HExamplesPage
from ... import utils

logger = dm.get_logger('central_widget')


def get_central_widget(parent=None):
    central_widget = CentralWidget(parent=parent)
    # splitter是自动的，不需要手动添加
    start_tab_widget = get_start_tab_widget(parent=central_widget)
    start_tab_widget.setObjectName('StartTabW')
    empty_tabw = HTabWidget(parent=parent)
    page = HExamplesPage(title='ex')
    page.setObjectName('EmptyPage')
    empty_tabw.setPages([page])
    empty_tabw.setObjectName('EmptyTabW')
    # central_widget.addTabWidget(empty_tabw)
    central_widget.addTabWidget(start_tab_widget)
    central_widget.addTabWidget(empty_tabw)
    return central_widget

class CentralWidget(QWidget):
    """
    自定义Widget控件，网格布局
    布局内有1个控件
    Qsplitter切分，内容是TabWidget
    继承关系(父到子)：CentralWidget -> Splitter -> QTabWidget -> Tab和Page
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mw = parent
        self.setWindowFlags(Qt.FramelessWindowHint)

        self._spliters = []  # 分屏器列表
        self._tab_widgets = []  # TabWidget列表

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(f'background-color: {HGF.COLORS.White}; ')
            # border-width: 3px; margin: 0px; padding: 3px;')
        
        # 初始化1个默认分屏器
        self.addSplitter()

    @property
    def spliters(self):
        return self._spliters

    @property
    def tab_widgets(self):
        return self._tab_widgets

    def current_tab_widget(self, pos=None):
        """获取当前TabWidget"""
        tabws = self.tab_widgets
        if tabws is None:
            return
        vis_tabws = [tabw for tabw in tabws if tabw.isVisible()]
        if vis_tabws == []:
            return None
        elif len(vis_tabws) == 1:
            return vis_tabws[0]
        else:
            assert pos is not None, '多个TabWidget时，需要传入pos参数'
            ctabw = []
            for tabw in vis_tabws:
                geom = tabw.geometry()  # x, y, w, h
                if geom.contains(pos):
                    ctabw.append(tabw)
                # print(f'geom={geom}, pos={pos}')
                # if tabw.geometry().contains(pos):
                    # ctabw.append(tabw)
            if ctabw == []:
                return None
            assert len(ctabw) == 1, f'多个TabWidget时，需要传入pos参数, {ctabw}'
            return ctabw[0]

    @property
    def current_splitter(self):
        spls = self.spliters
        if spls == [] or spls is None:
            return None
        elif len(spls) == 1:
            return spls[0]
        else:
            raise NotImplementedError('多个分屏器时，需要实现')
        return self.splitters

    # def get_splitter(self, orientation=Qt.Horizontal, parent=None):
    #     """添加分屏器"""
    #     pass
        # return splitter

    def addSplitter(self, orientation=Qt.Horizontal, parent=None):
        """添加分屏器"""
        current_spl = self.current_splitter
        current_spl_idx = self.spliters.index(current_spl) if current_spl else -1
        new_spl_idx = current_spl_idx + 1
        splitter = QSplitter(orientation, parent=parent)
        splitter.setObjectName(f"Splitter{new_spl_idx}")  # i.e. Splitter0, Splitter1, ...
        splitter.setHandleWidth(1)
        self._spliters.append(splitter)
        return splitter

    def addTabWidget(self, tab_widget):
        """添加TabWidget, 只会在当前分屏器中添加"""
        splitter = self.current_splitter
        self._tab_widgets.append(tab_widget)
        splitter.addWidget(tab_widget)  # 添加TabWidget到分屏器
        self.load()

    def on_tabBarClicked(self, index):
        logger.info(f'tabBarClicked. tabw: {self.current_tab_widget}, tab idx: {index}')
        current_tab = self.current_tab_widget.tabBar()
        print(f'current_tab={current_tab} {current_tab.tabText(index)}')
        # current_tab =

    def on_tabBarDoubleClicked(self, index):
        logger.info(f'tabBarDoubleClicked. index: {index}')
        # current_tab = self.current_tab_widget.tabBar()
        # print(f'current_tab={current_tab}')
        self.split_screen(index)
        

    def split_screen(self, current_tabw, mask_region=None):
        """
        实现分屏，实现左右和上下分屏即可
        """
        if mask_region is None:
            return
        current_spl = self.current_splitter
        current_tabw = self.current_tab_widget
        cpage = current_tabw.currentWidget()  # current page
        ctext = current_tabw.tabBar().tabText(index)  # current text
        cicon = current_tabw.tabBar().tabIcon(index)  # current icon
        # print(f'ctext={ctext}, cicon={cicon}')

        attempt_tabw = current_tabw  # 当前tabw或其他tabw，尝试
        attempt_area = 'right'

        attempt_spl = attempt_tabw.parent()  # 
        orent = attempt_spl.orientation()
        print(f'orent={orent}')
        
        # TODO: 判断当前tabw的位置，决定新建tabw的位置
        if attempt_tabw == current_tabw:
            if attempt_area == 'center':
                pass
            elif attempt_area == 'left':
                # 尝试把tab添加到tabw的左侧，新建tabw, 添加Tab到新建tabw
                new_tabw = TabWidget()
                new_tabw.addTab(cpage, cicon, ctext)
                # current_tabw.removeTab(index)  # 移除旧Tabw中的当前Tab  # Note: 不能移除，new_tabw添加tab后，会自动移除
                if attempt_spl.orientation() == Qt.Horizontal:
                    new_spl = attempt_spl
                else:
                    new_spl = self.get_splitter(orientation=Qt.Horizontal)
                # insert的索引是attempt tabw在父spl中的索引
                idx = attempt_spl.indexOf(attempt_tabw)
                new_spl.insertWidget(idx, new_tabw)
            elif attempt_area == 'right':
                # 尝试把tab添加到当前tabw的右侧，新建tabw，添加Tab到新建tabw
                new_tabw = TabWidget()
                new_tabw.addTab(cpage, cicon, ctext)
                if attempt_spl.orientation() == Qt.Horizontal:
                    new_spl = attempt_spl
                else:
                    new_spl = self.get_splitter(orientation=Qt.Horizontal)
                idx = attempt_spl.indexOf(attempt_tabw)
                new_spl.insertWidget(idx+1, new_tabw)
                # current_spl.addWidget(target_tabw)
            else:
                raise NotImplementedError('尝试拖动其他区域时，需要实现')
        else:
            raise NotImplementedError('尝试拖动到其他tabw时，需要实现')

        if current_tabw.count() == 0:
            current_tabw.deleteLater()


    def closeEvent(self, event):
        self.parent.settings.setValue("splitter/state", self.splitter.saveState())
        
    def load(self):
        """加载TabWidget"""

        # 加载分屏器
        for spl in self.spliters:
            self.layout.addWidget(spl)
        # 清除所有的子控件
        # for i in reversed(range(self.layout.count())):
            # self.layout.itemAt(i).widget().setParent(None)
        # for tab_widget in tab_widgets:
            # spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            # self.layout.addWidget(tab_widget)
            # self.splitter.addWidget(tab_widget)

    def mousePressEvent(self, ev):
        logger.info(f'mousePressEvent. ev: {ev}')

    def mouseMoveEvent(self, ev):
        logger.info(f'mouseMoveEvent. ev: {ev}')

    def moving_tab(self, ev, shadow_tabbar):
        """
        鼠标拖动Tab中
        """
        # logger.info(f'moving_tab. ev: {ev}')
        st = shadow_tabbar

        # 移动和显示影子tab bar
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))  # 获取鼠标在tab widget中的位置
        st.setParent(self)
        x = ev_posw.x() - st.width() / 2
        y = ev_posw.y() - st.height() / 2
        st.move(x, y)
        st.show()

        # 判断鼠标在哪个控件里
        ctabw = self.current_tab_widget(pos=ev_posw)
        for tabw in self.tab_widgets:  # 清除其他tabw的mask
            if tabw != ctabw:
                tabw.clear_mask()
        if ctabw is None:  # 在多个tabw的接缝处，不做处理
            return
        ctabw.mask_page(ev)  # 在当前tabw上显示mask

    def moved_tab(self, ev):
        """鼠标拖动Tab结束"""
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))  # 获取鼠标在tab widget中的位置
        
        ctabw = self.current_tab_widget(pos=ev_posw)
        if ctabw is None:
            return
        mr = ctabw.currentWidget().mask_region  # 蒙版位置, left, right, top, bottom, center
        ctabw.clear_mask()  # 清除蒙版
        logger.info(f'ctabw={ctabw}, mr={mr}')
        self.split_screen(ctabw, mr)









        


