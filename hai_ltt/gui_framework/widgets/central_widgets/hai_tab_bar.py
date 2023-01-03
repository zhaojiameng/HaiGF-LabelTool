from PySide2.QtWidgets import *

import damei as dm

logger = dm.get_logger('tab_bar')

class HTabBar(QTabBar):  # HAI TabBar
    """Tab标签"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTabsClosable(True)
        self.setMovable(True)
        self.shadow_tabbarr = QTabBar(self)  # 影子
        # 置于顶层
        self.shadow_tabbarr.raise_()
        self.c_idx = 0  # 当前tab的index
        # 设置self左对齐

        self.tabCloseRequested.connect(self.on_tabCloseRequested)

    def mousePressEvent(self, ev):
        logger.info(f'mousePressEvent: {ev}')
        super().mousePressEvent(ev)
        tab_idx = self.tabAt(ev.pos())
        if tab_idx == -1:
            return
        self.c_idx = tab_idx
        self.setCurrentIndex(self.tabAt(ev.pos()))  # 切换tab

        # 创建一个影子tabbar
        tab_icon = self.tabIcon(tab_idx)
        tab_text = self.tabText(tab_idx)
        tab_closable = self.tabsClosable()
        
        self.shadow_tabbarr.setTabsClosable(tab_closable)
        for i in range(self.shadow_tabbarr.count()):
            self.shadow_tabbarr.removeTab(0)
        self.shadow_tabbarr.addTab(tab_icon, tab_text)
        self.shadow_tabbarr.move(ev.x(), ev.y())
        self.shadow_tabbarr.hide()


    def mouseMoveEvent(self, ev):
        logger.info(f'mouseMoveEvent: {ev.x()} {ev.y()}')
        super().mouseMoveEvent(ev)
        # 获取当前鼠标对应的tab
        tab_idx = self.tabAt(ev.pos())
        # if tab_idx == -1:
            # logger.info('return')
            # return
        
        # 当前tabbar跟随鼠标移动
        self.shadow_tabbarr.show()
        w, h = self.shadow_tabbarr.sizeHint().width(), self.shadow_tabbarr.sizeHint().height()
        x, y = int(ev.x()-w/2), int(ev.y()-h/2)
        self.shadow_tabbarr.move(100, 0)
        self.shadow_tabbarr.move(x, y)

        # 如果移动到其他标签处，切换标签
        # if tab_idx != self.c_idx:
            # self.moveTab(self.c_idx, tab_idx)
            # self.c_idx = tab_idx
        
        # 如果移动到pages里，显示区域
        self.parent.moving_tab(ev, self.shadow_tabbarr)

    def mouseReleaseEvent(self, ev):
        self.shadow_tabbarr.hide()

    def on_tabCloseRequested(self, index):
        logger.info(f'on_tabCloseRequested: {index}')
        self.parent.removeTab(index)

    
    def dragMoveEvent(self, ev):
        logger.info(f'dragMoveEvent: {ev}')
        super().dragMoveEvent(ev)

