from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from .. import HTabWidget, HTabBar
from ..central_widgets.start_page import HStartPage
from hai_ltt.apis import HGF

def get_panel_widget(parent=None, **kwargs):
    panel_widget = PanelWidget(parent=parent, **kwargs)
    # page = HStartPage(parent=panel_widget, **kwargs)
    # panel_widget.setPages([page])
    return panel_widget


class PanelWidget(QDockWidget):
    """是dock，但有TabWidget的属性"""
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent

        tab_bar_widget = DockTitleBar(parent=self)
        self.setTitleBarWidget(tab_bar_widget)
        # self.setMovable(True)

        self._pages = []

        self.setup_ui()
        # self.titleBarWidget().setStyleSheet('background-color: rgb(120, 23, 10);')
        # 设置背景蓝色
        # self.setStyleSheet('background-color: rgb(120, 23, 120);')

    @property
    def c_idx(self):
        return self.tabBar().c_idx
    
    def tabBar(self):
        return self.titleBarWidget().children()[0]

    def setup_ui(self):
        # 不可移动
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        # dock添加一个widget
        page = QTextBrowser()
        # page.setFont(HGF.FONT)
        page.setText(self.tr('Some outputs here... '))
        page.setFrameShape(QFrame.NoFrame)
        page.setStyleSheet(HGF.MAIN_TEXT_CSS)

        page2 = QTextEdit()
        page2.setFrameShape(QFrame.NoFrame)
        # page2.setFont(HGF.FONT)
        page2.setText(self.tr('>>Please input something: '))
        page2.setStyleSheet(HGF.MAIN_TEXT_CSS)
        cursor = page2.textCursor()
        cursor.movePosition(QTextCursor.End)

        self.add_tab(self.tr('Outputs'), page, tip=self.tr('Outputs %s') % '(Ctrl+Shift+U)')
        self.add_tab(self.tr('Terminal'), page2, tip=self.tr('Terminal %s') % '(Ctrl+`)')

        self.load()

    def add_tab(self, title, page, tip=None):
        self._pages.append(page)
        # tab = QWidget()
        self.tabBar().add_tab(title)
        # self.tabBar().setFontSize(18)   
        if tip:
            self.tabBar().setTabToolTip(self.tabBar().count() - 1, tip)

    def clear_tabs(self):
        self._pages = []
        self.tabBar().clear()

    def load(self):
        """根据c_idx加载page, 其他page隐藏"""
        self.setWidget(self._pages[self.c_idx])


class DockTitleBar(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent

        tab_bar = DockTabBar(parent=self)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 添加一个stretch，使得tab_bar靠左
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(tab_bar)
        # layout.addStretch()
        layout.addWidget(spacer)
        self.setLayout(layout)
        # 标题栏的背景颜色
        self.setStyleSheet(
            f'background-color: {HGF.COLORS.WhiteSmoke};')
                # color: {HGF.COLORS.Blue};')  # 字体颜色

    
class DockTabBar(QTabBar):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        # self.addTab('Output')
        # self.addTab('Terminal')
        self.setExpanding(False)
        
        self.c_idx = 0
        # self.setIconSize(QSize(16, 16))
        # 设置tab无背景
        # self.setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(122, 112, 33);')
        # self.sizePolicy().setHorizontalPolicy(QSizePolicy.Maximum)

    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        self.c_idx = self.tabAt(ev.pos())
        self.p.p.load()

    def add_tab(self, title):
        self.addTab(title)

    def paintEvent(self, ev):
        # super().paintEvent(ev)
        # print('paintEvent', ev)
        # return super().paintEvent(ev)
        p = QPainter(self)
        p.setPen(QColor(HGF.COLORS.Black))
        p.setBrush(QColor(HGF.COLORS.WhiteSmoke))
        p.setFont(HGF.TAB_FONT)
        # 绘制无边框矩形
        # p.drawRoundedRect(self.rect(), 0, 0)

        # 绘制文字
        for i in range(self.count()):
            # p.drawText(self.tabRect(i), Qt.AlignCenter, self.tabText(self.c_idx))
            tab_text = self.tabText(i)
            tab_rect = self.tabRect(i)
            if i == self.c_idx:
                p.setPen(QColor(HGF.COLORS.Black))
                p.drawText(tab_rect, Qt.AlignCenter, tab_text)
                p.setPen(QColor(HGF.COLORS.RoyalBlue))
                x1, y1, x2, y2 = tab_rect.getCoords()
                for j in range(HGF.CONFIG['line_width']):
                    p.drawLine(x1, y2 - j, x2, y2 - j)
                # p.drawLine(tab_rect.bottomLeft(), tab_rect.bottomRight())
            else:
                p.setPen(QColor(HGF.COLORS.Gray))
                p.drawText(tab_rect, Qt.AlignCenter, tab_text)
        p.end()
        # 适应窗口大小
        self.adjustSize()
        
        

    
        

