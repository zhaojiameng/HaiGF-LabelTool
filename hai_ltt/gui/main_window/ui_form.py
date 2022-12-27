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

from ..widgets import get_toolbar, get_central_widget
from .. import utils
from ...version import __appname__


class Ui_MainWindow(object):

    def setupProperties(self, mw):
        """设置主窗口属性"""
        # if not mw.objectName():
            # mw.setObjectName(u"mw")
        size = mw.settings.value('window/size', QSize(1280, 720))
        position = mw.settings.value('window/position', QPoint(0, 0))
        state = mw.settings.value('window/state', QByteArray())
        
        mw.resize(size)
        mw.move(position)
        mw.restoreState(state)
        mw.setWindowTitle(__appname__)

    def setupUi(self, mw):
        self.setupProperties(mw=mw)  # 设置主窗口属性
        self.setupMenuBar(mw=mw)  # 设置菜单栏
        self.setupCoreFuncBar(mw=mw)  # 设置核心功能栏
        self.setupMainSideBar(mw=mw)  # 设置主侧栏
        self.setupAuxSideBar(mw=mw)  # 设置核心功能区
        self.setupCentralWidget(mw=mw)  # 设置中央控件
        # self.setupCanvas(mw=mw)  # 设置画布
        self.setupPanel(mw=mw)  # 设置面板
        self.setupStatusBar(mw=mw)  # 设置状态栏

        QMetaObject.connectSlotsByName(mw)

    def setupMenuBar(self, mw):
        """设置菜单栏"""
        self.menubar = QMenuBar(mw)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        mw.setMenuBar(self.menubar)

    def setupCoreFuncBar(self, mw):
        """设置核心功能栏"""
        core_func_bar = get_toolbar("core_func_bar", actions=None)
        actions=[
                mw.actions.explorer_action, 
                mw.actions.anno_action, 
                mw.actions.ai_action,
                None,  # 占位
                mw.actions.setting_action,
                ]
        core_func_bar.addActions(actions=actions)

        mw.addToolBar(Qt.LeftToolBarArea, core_func_bar)
        # 设置工具区域背景颜色
        # Qt.LeftToolBarArea.set
        
        
    def setupMainSideBar(self, mw):
        """设置左侧"""
        pass

    def setupAuxSideBar(self, mw):
        """
        辅助侧栏(右侧)
        """
        pass

    def setupCentralWidget(self, mw):
        """设置中心窗口"""
        central_widget = get_central_widget(mw)
        mw.setCentralWidget(central_widget)

    def setupCanvas(self, mw):
        """设置画布"""
        # dock = QDockWidget("Canvas", self.centralwidget)
        # start_tab = QT
        pass

    def setupPanel(self, mw):
        """设置底部选项卡"""
        # tab_widget = QTabWidget(mw)
        docker = QDockWidget("Bottom", mw)
        docker2 = QDockWidget("Bottom2", mw)
        docker.setWidget(QLabel('s1'))
        docker2.setWidget(QLabel('s2'))
        docker.setFeatures(QDockWidget.DockWidgetMovable)
        # docker.setMovable(False)
        # tab_widget.addTab(QLabel('s3'), "S4")
        mw.addDockWidget(Qt.BottomDockWidgetArea, docker)
        mw.addDockWidget(Qt.BottomDockWidgetArea, docker2)
        pass

    def setupStatusBar(self, mw):
        self.statusbar = QStatusBar(mw)
        self.statusbar.setObjectName(u"statusbar")
        mw.setStatusBar(self.statusbar)


