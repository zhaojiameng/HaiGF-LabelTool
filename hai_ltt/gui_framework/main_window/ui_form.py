# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QByteArray,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget, QDockWidget, QTabWidget,
    QTabBar, QLabel, QVBoxLayout, QHBoxLayout)

from ..widgets import get_toolbar, get_central_widget, get_main_side_bar, get_panel_widget
from .. import utils
from ...version import __appname__
from ..widgets import ExplorerWidget, AIWidget

class Ui_MainWindow(object):

    def setupProperties(self, mw):
        """设置主窗口属性"""
        # if not mw.objectName():
            # mw.setObjectName(u"mw")
        size = mw.settings.value('window/size', QSize(1280, 720))
        position = mw.settings.value('window/position', QPoint(0, 0))
        state = mw.settings.value('window/state', QByteArray())
        # 设置spacing为0
        mw.layout().setSpacing(0)
        mw.layout().setContentsMargins(0, 0, 0, 0)
        mw.resize(size)
        mw.move(position)
        mw.restoreState(state)
        

    def setupUi(self, mw):
        self.setupProperties(mw=mw)  # 设置主窗口属性
        self.setupMenuBar(mw=mw)  # 设置菜单栏
        self.setupCoreFuncBar(mw=mw)  # 设置核心功能栏
        self.setupMainSideBar(mw=mw)  # 设置主侧栏
        self.setupAuxSideBar(mw=mw)  # 设置辅助侧栏
        self.setupCentralWidget(mw=mw)  # 设置中央控件
        # self.setupCanvas(mw=mw)  # 设置画布
        self.setupPanel(mw=mw)  # 设置面板
        self.setupStatusBar(mw=mw)  # 设置状态栏

        QMetaObject.connectSlotsByName(mw)

    def setupMenuBar(self, mw):
        """设置菜单栏"""
        menubar = QMenuBar(mw)
        menubar.setObjectName(u"menubar")
        menubar.setGeometry(QRect(0, 0, 800, 22))
        mw.meaubar = menubar
        mw.setMenuBar(menubar)

    def setupCoreFuncBar(self, mw):
        """设置核心功能栏"""
        core_func_bar = get_toolbar("core_func_bar", parent=mw, actions=None)
        actions=[
                mw.actions.explorer_action, 
                mw.actions.anno_action, 
                mw.actions.ai_action,
                'Spacer',  # 占位
                mw.actions.user_action,
                mw.actions.setting_action,
                ]
        core_func_bar.addActions(actions=actions)
        mw.core_func_bar = core_func_bar
        mw.addToolBar(Qt.LeftToolBarArea, core_func_bar)
        # 设置工具区域背景颜色
        # Qt.LeftToolBarArea.set
        
        
    def setupMainSideBar(self, mw):
        """设置主侧栏，在左侧"""
        msb = get_main_side_bar(mw)
    
        explorer_widget = ExplorerWidget(mw)
        msb.add_widget(explorer_widget, mw.actions.explorer_action)  # 绑定主侧栏的资源浏览器按钮和控件
        ai_widget = AIWidget(mw)
        msb.add_widget(ai_widget, mw.actions.ai_action)  # 绑定主侧栏的ai按钮和控件
        
        msb.hide()  # 隐藏主侧栏
        mw.main_side_bar = msb  # 设置主侧栏
        mw.addDockWidget(Qt.LeftDockWidgetArea, msb)  # 添加主侧栏到左侧
        mw.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)  # 设置主窗口左上角属于哪个DockWidgetArea
        mw.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)  # 设置主窗口左下角属于哪个DockWidgetArea


    def setupAuxSideBar(self, mw):
        """
        辅助侧栏(右侧)
        """
        
        pass

    def setupCentralWidget(self, mw):
        """设置中心窗口"""
        mw.central_widget = get_central_widget(mw)
        mw.setCentralWidget(mw.central_widget)

    def setupCanvas(self, mw):
        """设置画布"""
        # dock = QDockWidget("Canvas", self.centralwidget)
        # start_tab = QT
        pass

    def setupPanel(self, mw):
        """设置底部选项卡"""
        panel_widget = get_panel_widget(mw)
        panel_widget.setObjectName("Panel")
        mw.addDockWidget(Qt.BottomDockWidgetArea, panel_widget)

    def setupStatusBar(self, mw):
        self.statusbar = QStatusBar(mw)
        self.statusbar.setObjectName(u"statusbar")
        # 设置状态栏背景颜色
        # self.statusbar.setStyleSheet("background-color: rgb(255, 255, 255);")    
        mw.setStatusBar(self.statusbar)


