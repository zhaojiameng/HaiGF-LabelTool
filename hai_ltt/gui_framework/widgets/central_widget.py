
from PySide2.QtCore import QRect, Qt, QByteArray, Slot
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton, QSpacerItem, QSplitter, QFrame,
    QGridLayout)

import damei as dm

from hai_ltt.apis import HGF
from .tab_widget import TabWidget, get_tab_widget, Page
from .pages.start_page import StartPage
from .. import utils

logger = dm.get_logger('central_widget')


def get_central_widget(parent=None):
    return CentralWidget(parent=parent)

class CentralWidget(QWidget):
    """
    自定义Widget控件，网格布局
    布局内有1个控件
    Qsplitter切分，内容是TabWidget
    继承关系(父到子)：CentralWidget -> Splitter -> QObject
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mw = parent

        self._spliters = []  # 分屏器列表
        self._tab_widgets = []  # TabWidget列表

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # state = parent.settings.value("splitter/state", QByteArray())
        # splitter.restoreState(state)

        self._init()
        # w = self._spliters[0].widget(0)
        # print(w, f'parent={w.parent()}')
        # print(self.current_tab_widget)
        self.setStyleSheet(f'background-color: {HGF.COLORS.WhiteSmoke};border-corlor: {HGF.COLORS.Black}; \
            border-width: 0px; margin: 0px; padding: 0px;')

        
    def _init(self, **kwargs):
        """
        初始化，添加分屏器、TabWidget、Page
        """
        mw = self.mw

        splitter = self.get_splitter()  # 添加分屏器
        self._spliters.append(splitter)
        tab_widget = self.get_tab_widget()  # 添加TabWidget
        self._tab_widgets.append(tab_widget)
        splitter.addWidget(tab_widget)  # 添加TabWidget到分屏器
        self.load()

    @property
    def current_tab_widget(self):
        tabws = self.tab_widgets
        if tabws == [] or tabws is None:
            return None
        elif len(tabws) == 1:
            return tabws[0]
        else:
            for i, tabw in enumerate(tabws):
                is_visible = tabw.isVisible()

                print(f'is_visible={is_visible}')
                # TODO: return tabw
            # raise NotImplementedError('多个TabWidget时，需要实现')

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

    @property
    def spliters(self):
        return self._spliters

    @property
    def tab_widgets(self):
        return self._tab_widgets

    def get_splitter(self, orientation=Qt.Horizontal, parent=None):
        """添加分屏器"""
        current_spl = self.current_splitter
        current_spl_idx = self.spliters.index(current_spl) if current_spl else -1
        new_spl_idx = current_spl_idx + 1
        splitter = QSplitter(orientation, parent=parent)
        splitter.setObjectName(f"Splitter{new_spl_idx}")  # i.e. Splitter0, Splitter1, ...
        splitter.setHandleWidth(1)
        return splitter

    def get_tab_widget(self, parent=None, **kwargs):
        start_page = StartPage(parent=self, **kwargs)
        examples_page = Page(parent=self, **kwargs)
        tab_widget = TabWidget(parent=parent)
        new_idx = len(self.tab_widgets)
        logger.info(f'Create new TabWidget, idx={new_idx}')
        tab_widget.setObjectName(f"TabWidget{new_idx}")
        tab_widget.tabBarClicked.connect(self.on_tabBarClicked)
        tab_widget.tabBarDoubleClicked.connect(self.on_tabBarDoubleClicked)
        tab_widget.tabBar().tabMoved.connect(self.on_tabMoved)
        
        tab_widget.addTab(
            start_page, 
            utils.newIcon("start"), 
            self.tr("Start")) 
        tab_widget.addTab(
            examples_page, 
            self.tr("Examples"))
        return tab_widget

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
        

    def split_screen(self, index):
        """
        实现分屏，实现左右和上下分屏即可
        """
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
            # current_spl.deleteLater()
        # print(f'current_spl={current_spl}')
        # current_tabw = 
    
    def on_tabMoved(self, from_index, to_index):
        logger.info(f'tabMoved. from_index: {from_index}, to_index: {to_index}')

    

    

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





        


