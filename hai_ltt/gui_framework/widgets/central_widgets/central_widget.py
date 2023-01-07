
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
from .. import HSplitter

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

    start_tab_widget.addPage(empty_page2)     
    start_tab_widget.insertPage(2, empty_page)
    
    
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
        elif len(vis_tabws) == 1 and pos is None:
            return vis_tabws[0]
        else:
            assert pos is not None, '多个TabWidget时，需要传入pos参数'
            ctabw = []
            for tabw in vis_tabws:
                geom = tabw.geometry()  # x, y, w, h
                geom2 = tabw.tabBar().geometry()  # x, y, w, h
                # print(f'geom={geom}, geom2={geom2}, pos={pos}')
                if geom.contains(pos) and not geom2.contains(pos):
                    ctabw.append(tabw)
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
            return f'TabWidget{len(self._tab_widgets)}'
            # if self.tab_widgets == []:
            #     return 'TabWidget0'
            # else:
            #     # names = [tabw.objectName() for tabw in self.tab_widgets]
            #     # maxidx = max([int(tabw.objectName().replace('TabWidget', '')) for tabw in self.tab_widgets])
            #     return f'TabWidget{maxidx + 1}'

            ctabw = self.current_tab_widget()
            ctabw_idx = self.tab_widgets.index(ctabw) if ctabw else -1
            new_tabw_idx = ctabw_idx + 1
            name = f'TabWidget{new_tabw_idx}'
            return name


    def create_splitter(self, orientation=Qt.Horizontal, parent=None):
        """添加分屏器到_splitters列表"""
        parent = parent if parent else self
        splitter = HSplitter(parent=parent, orientation=orientation)
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
        self.setSplitter(splitter)

    def create_tab_widget_by_source_tabw(self, source_tabw):
        """
        根据源TabWidget及其index tab, 创建新的TabWidget
        """
        tabw = HTabWidget(self)
        name = self.automatic_naming(tabw=tabw)
        tabw.setObjectName(name)
        # page = source_tabw.currentWidget()
        page = source_tabw.pages[source_tabw.tabBar().c_idx]
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
        return tab_widget.parent()
        # for splitter in self.splitters:
            # if splitter.indexOf(tab_widget) != -1:
                # return splitter
        # return None

    def judge_need_delete_source_tabw(self, source_tabw, target_tabw):
        """判断是否需要删除源TabWidget"""
        if source_tabw.count() == 1 and target_tabw != source_tabw:
            return True
        else:
            return False
    
    def judge_need_create_new_splitter(self, mask_region, tspl):
        """判断是否需要创建新的Splitter和方向"""
        mr = mask_region
        orent = tspl.orientation()  # 原Splitter的方向
        map_dict = {
            'left': Qt.Horizontal,
            'right': Qt.Horizontal,
            'top': Qt.Vertical,
            'bottom': Qt.Vertical,
            'center': orent
        }
        if map_dict[mr] != orent:
            return True, map_dict[mr]
        else:
            return False, orent
        # if mask_region in ['left', 'right']:
        #     if orent == Qt.Horizontal:
        #         return False, orent
        #     else:
        #         return True, Qt.Vertical
        # elif mask_region in ['top', 'bottom']:
        #     if orent == Qt.Vertical:
        #         return False, orent
        #     else:
        #         return True, Qt.Horizontal
        # else:  # center
        #     return False, orent

    def split_screen(self, source_tabw, target_tabw, mask_region=None):
        """
        在moved_tab后调用，实现分屏。
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

        need_create_new_tabw = True if mr in ['left', 'right', 'top', 'bottom'] else False
        need_delete_source_tabw = self.judge_need_delete_source_tabw(stabw, ttabw)
        need_create_new_spl, new_orent = self.judge_need_create_new_splitter(mr, tspl=tspl)
        num_of_tabws = len(self._tab_widgets) + bool(need_create_new_tabw) - bool(need_delete_source_tabw)
        # print(f'Stabw={stabw} \nTtabw={ttabw} \nTspl={tspl} \nMr={mr} \nOrent={orent}')
        # print(f'need_create_new_tabw   ={need_create_new_tabw} \nneed_create_new_spl    ={need_create_new_spl}')
        # print(f'need_delete_source_tabw={need_delete_source_tabw} \nnew_orent={new_orent}')
        # print(f'num_of_tabws={num_of_tabws}')
        if num_of_tabws >= 4:
            self.parent().show_warning('Only support 3 tab widgets at most.')
            return

        if need_create_new_tabw:
            new_tabw = self.create_tab_widget_by_source_tabw(stabw)
            # stabw, new_tabw = stabw.split_into_two_tabw()
            self._tab_widgets.append(new_tabw)
            stabw.remove_current_page()  # 移除当前Tab
        else:  # 不创建
            new_tabw = ttabw
            if mr == 'center' and stabw != ttabw:  
                new_tabw.add_tab_from_another_tabw(stabw)  # 添加源Tab到目标TabWidget
                stabw.remove_current_page()  # 移除当前Tab

        if need_delete_source_tabw:
            # print('delete source tabw:', stabw in self._tab_widgets)
            stabw.setParent(None)
            self._tab_widgets.remove(stabw)
            # stabw.hide()
            # self.delete_tab_widget(stabw)

        # 清除原有的Splitters
        self.clear_splitters()

        # print(f'num_of_tabw: {len(self._tab_widgets)} \nnum_of_spl : {len(self._splitters)}')
        if len(self._tab_widgets) == 1:
            # 获取最终的Splitter
            final_spl = self.create_splitter(orientation=new_orent)
            self._splitters = [final_spl]
            # tabw = self._tab_widgets[0]
            final_spl.set_widget(self._tab_widgets[0])
            self.setSplitter(final_spl)
        elif len(self._tab_widgets) == 2:
            final_spl = self.create_splitter(orientation=new_orent)  # 创建新的Splitter
            self._splitters = [final_spl]  # 保存新的Splitter
            ## 获取widgets
            sorted_nt_tabw = self.sort_new_tabw_vs_ttabw(new_tabw, ttabw, mr)
            if sorted_nt_tabw is None:  # mr=center的时候
                return
            final_spl.set_widgets(sorted_nt_tabw)
            self.setSplitter(final_spl)
        elif len(self._tab_widgets) == 3:
            t1, t2, t3 = self._tab_widgets  # t1和t2是原来的，t3是新的
            final_spl = self.create_splitter(orientation=orent)
            sorted_nt_tabw = self.sort_new_tabw_vs_ttabw(new_tabw, ttabw, mr)
            if need_create_new_spl:
                new_spl = self.create_splitter(orientation=new_orent)
                self._splitters = [final_spl, new_spl]
                new_spl.set_widgets(sorted_nt_tabw)
                xx_widgets = [t1, new_spl] if t2 == ttabw else [new_spl, t2]  # 排序t1 t2
            else:
                self._splitters = [final_spl]
                xx_widgets = [t1] + sorted_nt_tabw if t2 == ttabw else sorted_nt_tabw + [t2]
            final_spl.set_widgets(xx_widgets)
            self.setSplitter(final_spl)
        else:
            raise NotImplementedError(f'Not implemented for len(self._tab_widgets)={len(self._tab_widgets)}')
        
        # for tabw in self._tab_widgets:
            # tabw.show()
        
    def sort_new_tabw_vs_ttabw(self, new_tabw, ttabw, mask_region):
        """排序，根据mask_region的值，对new_tabw和ttabw进行排序，返回排序后组成的列表"""
        mr = mask_region
        if mr in ['left', 'top']:
            widgets = [new_tabw, ttabw]
        elif mr in ['right', 'bottom']:
            widgets = [ttabw, new_tabw]
        elif mr == 'center':
            widgets = None
        else:
            raise ValueError(f'Invalid mask_region={mr}')
        return widgets


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
        
    def setSplitter(self, splitter):
        """加载TabWidget"""
        # 清除所有分屏器
        for spl in self.splitters:
            self.layout.removeWidget(spl)
        self.layout.addWidget(splitter)

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
        for tabw in self._tab_widgets:  # 清除其他tabw的mask
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
        stabw = st.body.p  # 拖动的tab所在的tabw, source tab widget
        # print(f'body_of_st={body_of_st} body_tab_idx={body_tab_idx}')
        ev_posw = self.mapFromGlobal(QPoint(ev.globalX(), ev.globalY()))  # 获取鼠标在tab widget中的位置
        
        ctabw = self.current_tab_widget(pos=ev_posw)
        if ctabw is None:
            return
        mr = ctabw.currentWidget()._mask_region  # 蒙版位置, left, right, top, bottom, center
        ctabw.clear_mask()  # 清除蒙版
        self.split_screen(stabw, ctabw, mr) 

    
    def clear_splitters(self):
        """清除所有分屏器"""
        for spl in self.splitters:
            self.layout.removeWidget(spl)
        self._splitters = []









        


