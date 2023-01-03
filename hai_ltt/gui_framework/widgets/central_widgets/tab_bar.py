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
        self.c_tabbar = QTabBar(self.parent)
        # 设置self左对齐

        self.tabCloseRequested.connect(self.on_tabCloseRequested)

    def mousePressEvent(self, ev):
        logger.info(f'mousePressEvent: {ev}')
        tab_idx = self.tabAt(ev.pos())
        if tab_idx == -1:
            return
        self.setCurrentIndex(self.tabAt(ev.pos()))  # 切换tab

        # 创建一个影子tabbar
        tab_icon = self.tabIcon(tab_idx)
        tab_text = self.tabText(tab_idx)
        tab_closable = self.tabsClosable()
        
        self.c_tabbar.setTabsClosable(tab_closable)
        for i in range(self.c_tabbar.count()):
            self.c_tabbar.removeTab(0)
        self.c_tabbar.addTab(tab_icon, tab_text)
        self.c_tabbar = self.c_tabbar
        self.c_tabbar.move(ev.x(), ev.y())
        self.c_tabbar.hide()


    def mouseMoveEvent(self, ev):
        print(f'mouseMoveEvent: {ev}')
        # 获取当前鼠标对应的tab
        tab_idx = self.tabAt(ev.pos())
        if tab_idx == -1:
            return
        
        # 当前tabbar跟随鼠标移动
        self.c_tabbar.show()
        w, h = self.c_tabbar.sizeHint().width(), self.c_tabbar.sizeHint().height()
        x, y = int(ev.x()-w/2), int(ev.y()-h/2)
        self.c_tabbar.move(x, y)
        # 如果移动到其他标签处，切换标签
        tab_idx2 = self.tabAt(ev.pos())  # 第二个标签
        if tab_idx2 != -1 and tab_idx2 != tab_idx:
            self.moveTab(tab_idx, tab_idx2)


    def mouseReleaseEvent(self, ev):
        self.c_tabbar.hide()

    def on_tabCloseRequested(self, index):
        logger.info(f'on_tabCloseRequested: {index}')
        self.parent.removeTab(index)

