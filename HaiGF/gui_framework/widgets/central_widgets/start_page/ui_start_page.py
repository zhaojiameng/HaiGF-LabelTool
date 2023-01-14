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

from HaiGF.apis import HGF, utils
from ...common.blue_button import BlueButton
from ...common.item_model import ItemModel


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"StartPage")
        Widget.resize(800, 600)
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 10, 10)
        layout.setSpacing(10)

        # space_label = QLabel()

        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(HGF.FIRST_LEVEL_TITLE_CSS)
        print(Widget)
        print(Widget.tr('Start up'))
        self.label.setText(Widget.tr("Welcome to HAI GUI Framework!"))
        self.label.setWordWrap(True)

        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_4")
        self.label_2.setFont(HGF.FONT)
        self.label_2.setText(Widget.tr('HAI GUI is a framework for convenient development of desktop applications based on AI algorithms'))
        self.label_2.setWordWrap(True)

        self.label_3 = QLabel(Widget)  # start up
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 120, 211, 51))
        self.label_3.setStyleSheet(HGF.SECOND_LEVEL_TITLE_CSS)
        self.label_3.setText(Widget.tr("Start Up"))

        
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 280, 211, 51))
        # self.label_5.setFont(font1)
        self.label_5.setStyleSheet(HGF.SECOND_LEVEL_TITLE_CSS)
        self.label_5.setText(Widget.tr('Recent'))

        self.openFileButton = BlueButton(text='Open File', parent=Widget)
        self.openFileButton.setObjectName(u"openFileButton")
        self.openFileButton.setMinimumSize(120, 32)
        # self.openFileButton.setGeometry(QRect(90, 180, 121, 32))
        # self.openFileButton.move(90, 180)
        icon = utils.newIcon('file-addition-one')
        self.openFileButton.setIcon(icon)
        self.openFileButton.setText(Widget.tr('Open File ...'))

        self.openDirButton = BlueButton(text='Open Folder', parent=Widget)
        self.openDirButton.setObjectName(u"openDirButton")
        # self.openDirButton.setGeometry(QRect(90, 220, 121, 32))
        self.openDirButton.setMinimumSize(120, 32)
        # self.openDirButton.move(90, 220)
        icon1 = utils.newIcon('folder-open')
        self.openDirButton.setIcon(icon1)
        self.openDirButton.setText(Widget.tr('Open Folder ...'))

        self.recentListView = QListView(Widget)
        self.recentListView.setObjectName(u"recentListView")
        # self.recentListView.setGeometry(QRect(90, 330, 256, 192))
        self.recentListView.setAutoFillBackground(False)
        self.recentListView.setFrameShape(QFrame.NoFrame)
        self.recentListView.setFrameShadow(QFrame.Sunken)
        recent_files = ['No recent files']
        item_model = ItemModel.from_list(recent_files)
        self.recentListView.setModel(item_model)
        self.recentListView.setStyleSheet(f"color: {HGF.COLORS.DimGray};")
        self.recentListView.setFont(HGF.FONT)

        # self.retranslateUi(Widget)    
        # layout.addWidget(space_label, 0, 0)
        layout.addWidget(self.label, 0, 1, 1, 20)
        layout.addWidget(self.label_2, 5, 2, 1, 20)
        layout.addWidget(self.label_3, 10, 1, 1, 20)
        layout.addWidget(self.openFileButton, 20, 2, 1, 1)
        layout.addWidget(self.openDirButton, 30, 2, 1, 1)
        layout.addWidget(self.label_5, 40, 1, 1, 20)
        layout.addWidget(self.recentListView, 50, 2, 1, 20)

        Widget.setLayout(layout)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"GUI Freamwork of HAI", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Start up", None))
        self.label_4.setText("")
        self.openFileButton.setText(QCoreApplication.translate("Widget", u"Open File ...", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Recent", None))
        self.openDirButton.setText(QCoreApplication.translate("Widget", u"Open Folder ...", None))
    # retranslateUi

