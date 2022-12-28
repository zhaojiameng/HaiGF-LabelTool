# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from hai_ltt.apis import HGF
from ..blue_button import BlueButton


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"StartPage")
        Widget.resize(800, 600)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        # self.label.setGeometry(QRect(50, 70, 701, 51))
        font = QFont()
        font.setFamily(HGF.FONT_FAMILY)
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet(f"color: {HGF.COLORS.LightBlack};")

        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 150, 211, 51))
        font1 = QFont()
        font1.setFamily(u"Al Bayan")
        font1.setPointSize(18)
        self.label_3.setFont(font1)

        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(80, 200, 211, 51))
        self.label_4.setFont(font1)

        self.openFileButton = BlueButton(text='Open File', parent=Widget)
        self.openFileButton.setObjectName(u"openFileButton")
        self.openFileButton.setGeometry(QRect(90, 200, 121, 32))
        icon = QIcon(QIcon.fromTheme(u"appointment-new"))
        self.openFileButton.setIcon(icon)
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
        self.openDirButton = QPushButton(Widget)
        self.openDirButton.setObjectName(u"openDirButton")
        self.openDirButton.setGeometry(QRect(90, 240, 121, 32))
        icon1 = QIcon()
        iconThemeName = u"appointment-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.openDirButton.setIcon(icon1)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"GUI Freamwork of HAI", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Start up", None))
        self.label_4.setText("")
        self.openFileButton.setText(QCoreApplication.translate("Widget", u"Open File ...", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Recent", None))
        self.openDirButton.setText(QCoreApplication.translate("Widget", u"Open Dir ...", None))
    # retranslateUi

