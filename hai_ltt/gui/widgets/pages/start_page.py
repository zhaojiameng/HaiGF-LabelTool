# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 50, 341, 51))
        font = QFont()
        font.setFamily(u"Al Bayan")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 90, 341, 51))
        self.label_2.setFont(font)
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 160, 211, 51))
        font1 = QFont()
        font1.setFamily(u"Al Bayan")
        font1.setPointSize(18)
        self.label_3.setFont(font1)
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(80, 200, 211, 51))
        self.label_4.setFont(font1)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(90, 220, 101, 32))
        icon = QIcon(QIcon.fromTheme(u"appointment-new"))
        self.pushButton.setIcon(icon)
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 280, 211, 51))
        self.label_5.setFont(font1)
        self.recentListView = QListView(Widget)
        self.recentListView.setObjectName(u"recentListView")
        self.recentListView.setGeometry(QRect(90, 330, 256, 192))
        self.recentListView.setAutoFillBackground(False)
        self.recentListView.setFrameShape(QFrame.NoFrame)
        self.recentListView.setFrameShadow(QFrame.Sunken)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Label Trian Tools of HAI", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u4eba\u5de5\u667a\u80fd\u6807\u6ce8\u8bad\u7ec3\u5de5\u5177", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Start up", None))
        self.label_4.setText("")
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Open ...", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Recent", None))
    # retranslateUi

