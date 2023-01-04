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
        self.shadow_tabbar = QTabBar(self)  # 影子
        # 置于顶层
        self.shadow_tabbar.raise_()
        self.c_idx = 0  # 当前tab的index
        # 设置self左对齐

        self.tabCloseRequested.connect(self.on_tabCloseRequested)

    def mousePressEvent(self, ev):
        logger.info(f'mousePressEvent: {ev}')
        super().mousePressEvent(ev)
        tab_idx = self.tabAt(ev.pos())
        if tab_idx == -1:
            return
        self.c_idx = tab_idx  # 存储current tab idx
        self.setCurrentIndex(self.tabAt(ev.pos()))  # 切换tab
        self.setup_shadow_tabbar(tab_idx)  # 更新影子
        self.shadow_tabbar.hide()  # 隐藏因子

    def mouseMoveEvent(self, ev):
        # logger.info(f'mouseMoveEvent: {ev.x()} {ev.y()}')
        # 获取当前鼠标对应的tab
        tab_idx = self.tabAt(ev.pos())
        if tab_idx != -1:  # 在self范围内
            super().mouseMoveEvent(ev)
        
        # 当前tabbar跟随鼠标移动
        self.shadow_tabbar.show()  # 显示影子
        # 如果移动到pages里，显示区域
        self.parent.parent.moving_tab(ev, self.shadow_tabbar)

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        print(f'mouseReleaseEvent: {ev}')
        self.shadow_tabbar.hide()  # 隐藏影子
        self.parent.parent.moved_tab(ev)

    def on_tabCloseRequested(self, index):
        # logger.info(f'on_tabCloseRequested: {index}')
        self.parent.removeTab(index)

    def dragMoveEvent(self, ev):
        logger.info(f'dragMoveEvent: {ev}')
        super().dragMoveEvent(ev)

    def setup_shadow_tabbar(self, tab_idx):
        """根据tab的索引，更新影子tab的图标、text等"""
        tab_icon = self.tabIcon(tab_idx)
        tab_text = self.tabText(tab_idx)
        tab_closable = self.tabsClosable()
        
        for i in range(self.shadow_tabbar.count()):  # clear
            self.shadow_tabbar.removeTab(0)
        self.shadow_tabbar.addTab(tab_icon, tab_text)
        self.shadow_tabbar.setTabsClosable(tab_closable)

        


