
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
from .start_page import ExamplePage

logger = dm.get_logger('central_widget')


def get_central_widget(parent=None):
    central_widget = CentralWidget(parent=parent)
    # splitter是自动的，不需要手动添加
    start_tab_widget = get_start_tab_widget(parent=central_widget)
    start_tab_widget.setObjectName('StartTabW')

    # empty_tabw = HTabWidget(parent=central_widget)
    empty_page = HExamplesPage(title='ex')
    empty_page.setObjectName('EmptyPage')
    # pages = start_tab_widget.pages + [empty_page]
    # start_tab_widget.setPages(pages)
    # empty_tabw.setPages([empty_page])
    # empty_tabw.setObjectName('EmptyTabW')

    # empty_tabw2 = HTabWidget(parent=central_widget)
    empty_page2 = HExamplesPage(title='ex2')
    empty_page2.setObjectName('EmptyPage2')
    # empty_tabw2.setPages([empty_page2])
    # empty_tabw2.setObjectName('EmptyTabW2')
    # central_widget.addTabWidget(empty_tabw)

    start_tab_widget.addPage(empty_page)
    start_tab_widget.insertPage(1, empty_page2)
    
    central_widget.addTabWidget(start_tab_widget)
    # central_widget.addTabWidget(empty_tabw)
    # central_widget.addTabWidget(empty_tabw2)
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

        self._splitters = []  # 分屏器列表
        self._tab_widgets = []  # TabWidget列表

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(f'background-color: {HGF.COLORS.White}; ')
            # border-width: 3px; margin: 0px; padding: 3px;')

    @property
    def splitters(self):
        return self._splitters

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
        spls = self.splitters
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

    def automatic_naming(self, tabw=None, spliiter=None):
        if spliiter is not None:
            if self.splitters == []:
                return 'Splitter0'
            else:
                maxidx = max([int(spl.objectName().replace('Splitter', '')) for spl in self.splitters])
                return f'Splitter{maxidx + 1}'
                
            cspl = self.current_splitter
            cspl_idx = self.splitters.index(cspl) if cspl else -1
            new_spl_idx = cspl_idx + 1
            name = f'Splitter{new_spl_idx}'
            return name
        if tabw is not None:
            # if self.tab_widgets == []:
            #     return 'TabWidget0'
            # else:
            #     names = [tabw.objectName() for tabw in self.tab_widgets]
            #     maxidx = max([int(tabw.objectName().replace('TabWidget', '')) for tabw in self.tab_widgets])
            #     return f'TabWidget{maxidx + 1}'
            ctabw = self.current_tab_widget()
            ctabw_idx = self.tab_widgets.index(ctabw) if ctabw else -1
            new_tabw_idx = ctabw_idx + 1
            name = f'TabWidget{new_tabw_idx}'
            return name


    def create_splitter(self, orientation=Qt.Horizontal, parent=None):
        """添加分屏器到_splitters列表"""
        parent = parent if parent else self
        splitter = QSplitter(orientation, parent=parent)
        name = self.automatic_naming(spliiter=splitter)
        splitter.setObjectName(name)  # i.e. Splitter0, Splitter1, ...
        splitter.setHandleWidth(1)
        return splitter

    def asign_spliter(self, tab_widget, *args):
        """分配分屏器"""
        # 什么时候创建分屏器？
        if self.splitters == []:
            splitter = self.create_splitter()
            self._splitters.append(splitter)
        elif len(self.splitters) == 1:
            splitter = self.splitters[0]
        else:
            raise NotImplementedError('多个分屏器时，需要实现')

        return splitter

    def addTabWidget(self, tab_widget, *args):
        """添加TabWidget到_tab_widgets列表，并设置其parrent为splitter中"""
        self._tab_widgets.append(tab_widget)
        # 分配spliter，分配方案：不知道
        splitter = self.asign_spliter(tab_widget, *args)
        splitter.addWidget(tab_widget)  # 添加TabWidget到分屏器
        self.load()

    def create_tab_widget_by_source_tabw(self, source_tabw):
        """
        根据源TabWidget及其index tab, 创建新的TabWidget
        """
        tabw = HTabWidget(self)
        name = self.automatic_naming(tabw=tabw)
        tabw.setObjectName(name)
        page = source_tabw.currentWidget()
        tabw.setPages([page])
        return tabw

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

    
    def get_current_splitter_by_tab_widget(self, tab_widget):
        """获取当前TabWidget所在的Splitter"""
        for splitter in self.splitters:
            if splitter.indexOf(tab_widget) != -1:
                return splitter
        return None
    
    def judge_need_create_new_splitter(self, mask_region, tspl):
        """判断是否需要创建新的Splitter和方向"""
        orent = tspl.orientation()
        if mask_region in ['left', 'right']:
            if orent == Qt.Horizontal:
                return False, Qt.Vertical
            else:
                return True, Qt.Vertical
        elif mask_region in ['top', 'bottom']:
            if orent == Qt.Vertical:
                return False, Qt.Horizontal
            else:
                return True, Qt.Horizontal
        else:  # center
            return False, None

    def split_screen(self, source_tabw, target_tabw, mask_region=None):
        """
        在moved_tab后调用，实现分屏，实现左右和上下分屏即可
        :param target_tabw: 当前鼠标所在TabWidget，即目标TabWidget
        :param mask_region: left, right, top, bottom, center or None
        """
        stabw = source_tabw
        ttabw = target_tabw
        mr = mask_region
        if mr is None:
            return
        tspl = self.get_current_splitter_by_tab_widget(ttabw)
        orent = tspl.orientation()

        


        return

        print(f'Stabw={stabw} \nTtabw={ttabw} \nTspl={tspl} \nMr={mr} \nOrent={orent}')
        need_create_new_tabw = True if mr in ['left', 'right', 'top', 'bottom'] else False
        need_create_new_spl, new_orent = self.judge_need_create_new_splitter(mr, tspl=tspl)
        print(f'need_create_new_tabw={need_create_new_tabw} \nneed_create_new_spl={need_create_new_spl} \nnew_orent={new_orent}')
        
        # 创建新TabWidget和Splitter
        if need_create_new_tabw:
            new_tabw = self.create_tab_widget_by_source_tabw(stabw)
            self._tab_widgets.append(new_tabw)
            # new_taw_widget中只包含1个page
            # 删除源TabWidget中的当前页
            # stabw.removePage(stabw.currentIndex())
        else:
            # stabw.setParent(None)
            new_tabw = stabw
            
        if need_create_new_spl:
            new_spl = self.addSplitter(new_orent, parent=tspl)
        else:
            new_spl = tspl
        
        if mr == 'left':
            new_spl.insertWidget(0, new_tabw)
        elif mr == 'right':  # 测试, 
            new_spl.addWidget(new_tabw)
        elif mr == 'top':
            new_spl.insertWidget(0, new_tabw)
        elif mr == 'bottom':
            new_spl.addWidget(new_tabw)
        elif mr == 'center':  # center
            if ttabw == stabw:
                print('ttabw == stabw')
                pass
            else:  # 目标TabWidget是其他tabw
                print(f'new_spl.count = {new_spl.count()}')
                self.move_one_tab_to_another_tabw(stabw, ttabw)
                # new_spl.addWidget(new_tabw)
                print(f'new_spl={new_spl} \nnew_tabw={new_tabw} \nnew_spl.count={new_spl.count()}')
        else:
            raise ValueError(f'Invalid mask_region: {mr}')

        # if stabw.count() == 0:
            # stabw.remove_from_splitter()

        for spl in self.splitters:
            print(f'spl={spl}')
        print(ttabw.count())

        self.load()

    def move_one_tab_to_another_tabw(self, source_tabw, target_tabw):
        """将一个TabWidget中的一个Tab移动到另一个TabWidget中"""
        source_page = source_tabw.currentWidget()
        print(source_page)
        # target_tabw.addPage(source_page)
        old_pages = target_tabw.pages
        old_pages.append(source_page)
        target_tabw.setPages(old_pages)
        # target_tabw.insertPage(0, source_page)
        # source_tabw.move_tab_to_another_tabw(target_tabw)

    def closeEvent(self, event):
        self.parent.settings.setValue("splitter/state", self.splitter.saveState())
        
    def load(self):
        """加载TabWidget"""
        # 清除所有分屏器
        for spl in self.splitters:
            self.layout.removeWidget(spl)
            # spl.deleteLater()

        # 加载分屏器
        # for spl in self.splitters]:
            # self.layout.addWidget(spl)
        self.layout.addWidget(self.splitters[-1])

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
        stabw = st.body.parent

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
        if ctabw == stabw and stabw.count() == 1:  # 源tabw只有一个tab，不做处理
            return
        if ctabw is None:  # 在多个tabw的接缝处，不做处理
            return
        ctabw.mask_page(ev)  # 在当前tabw上显示mask

    def moved_tab(self, ev, shadow_tabbar):
        """鼠标拖动Tab结束"""
        st = shadow_tabbar
        stabw = st.body.parent  # 拖动的tab所在的tabw, source tab widget
        # print(f'body_of_st={body_of_st} body_tab_idx={body_tab_idx}')
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))  # 获取鼠标在tab widget中的位置
        
        ctabw = self.current_tab_widget(pos=ev_posw)
        if ctabw is None:
            return
        mr = ctabw.currentWidget()._mask_region  # 蒙版位置, left, right, top, bottom, center
        ctabw.clear_mask()  # 清除蒙版
        self.split_screen(stabw, ctabw, mr) 









        


