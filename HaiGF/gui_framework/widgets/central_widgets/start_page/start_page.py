# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


from pathlib import Path
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import damei as dm

from HaiGF.apis import root_path, __appname__
from .ui_start_page import Ui_Widget
from ...common.hai_page import HPage
from ...common.blue_button import BlueButton
from ...common.item_model import ItemModel
from .... import utils
from HaiGF.apis import HGF

logger = dm.get_logger('start_page')

class HStartPage(HPage):
    def __init__(self, parent=None, icon=None, title=None):
        icon = utils.newIcon('start')
        title = 'Start'
        super().__init__(parent, icon=icon, title=title)
    
        self.p = parent
        self._title = self.tr('Start')
        # self.mw = self.parent.mw

        # 设置UI界面
        # self.ui = Ui_self()
        # self.ui.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        self.resize(800, 600)
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 10, 10)
        layout.setSpacing(10)

        # space_label = QLabel()

        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(HGF.FIRST_LEVEL_TITLE_CSS)
        self.label.setText(self.tr("Welcome to HAI GUI Framework~"))
        self.label.setWordWrap(True)

        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_4")
        # self.label_2.setFont(HGF.FONT)
        self.label_2.setText(self.tr('HAI GUI is a framework for convenient development of desktop applications based on AI algorithms'))
        self.label_2.setWordWrap(True)
        # print(HGF.MAIN_TEXT_CSS)
        self.label_2.setStyleSheet(HGF.MAIN_TEXT_CSS)

        self.label_3 = QLabel(self)  # start up
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 120, 211, 51))
        self.label_3.setStyleSheet(HGF.SECOND_LEVEL_TITLE_CSS)
        self.label_3.setText(self.tr("Start Up"))

        
        self.label_5 = QLabel(self)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 280, 211, 51))
        # self.label_5.setFont(font1)
        self.label_5.setStyleSheet(HGF.SECOND_LEVEL_TITLE_CSS)
        self.label_5.setText(self.tr('Recent'))

        self.openFileButton = BlueButton(text='Open File', parent=self)
        self.openFileButton.setObjectName(u"openFileButton")
        self.openFileButton.setMinimumSize(120, 32)
        # self.openFileButton.setGeometry(QRect(90, 180, 121, 32))
        # self.openFileButton.move(90, 180)
        icon = utils.newIcon('file-addition-one')
        self.openFileButton.setIcon(icon)
        self.openFileButton.setText(self.tr('Open File ...'))

        self.openDirButton = BlueButton(text='Open Folder', parent=self)
        self.openDirButton.setObjectName(u"openDirButton")
        # self.openDirButton.setGeometry(QRect(90, 220, 121, 32))
        self.openDirButton.setMinimumSize(120, 32)
        # self.openDirButton.move(90, 220)
        icon1 = utils.newIcon('folder-open')
        self.openDirButton.setIcon(icon1)
        self.openDirButton.setText(self.tr('Open Folder ...'))

        self.recentListView = QListView(self)
        self.recentListView.setObjectName(u"recentListView")
        # self.recentListView.setGeometry(QRect(90, 330, 256, 192))
        self.recentListView.setAutoFillBackground(False)
        self.recentListView.setFrameShape(QFrame.NoFrame)
        self.recentListView.setFrameShadow(QFrame.Sunken)
        recent_files = [self.tr('No recent files')]
        item_model = ItemModel.from_list(recent_files)
        self.recentListView.setModel(item_model)
        self.recentListView.setStyleSheet(f"color: {HGF.COLORS.DimGray};")
        self.recentListView.setFont(HGF.FONT)

        # self.retranslateUi(self)
        # layout.addWidget(space_label, 0, 0)
        layout.addWidget(self.label, 0, 1, 1, 20)
        layout.addWidget(self.label_2, 5, 2, 1, 20)
        layout.addWidget(self.label_3, 10, 1, 1, 20)
        layout.addWidget(self.openFileButton, 20, 2, 1, 1)
        layout.addWidget(self.openDirButton, 30, 2, 1, 1)
        layout.addWidget(self.label_5, 40, 1, 1, 20)
        layout.addWidget(self.recentListView, 50, 2, 1, 20)

        self.setLayout(layout)

        QMetaObject.connectSlotsByName(self)


    @QtCore.Slot()
    def on_openFileButton_clicked(self):
        print('File button clicked')

    @QtCore.Slot()
    def on_openDirButton_clicked(self):
        mw = self.p.p.p
        # defaultOpenDirPath = root_path
        defaultOpenDirPath = mw.settings.value('lastDirPath', root_path)
        
        selected_dir = str(
            QFileDialog.getExistingDirectory(
                self,
                self.tr("%s - Open Directory") % __appname__,
                defaultOpenDirPath,
                QFileDialog.ShowDirsOnly
                | QFileDialog.DontResolveSymlinks,
            )
        )
        mw.load_file_or_dir(dir=selected_dir)

    
