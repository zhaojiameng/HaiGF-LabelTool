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
            Widget.setObjectName(u"ExamplePage")
        Widget.resize(800, 600)


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
        self.openDirButton.setText(QCoreApplication.translate("Widget", u"Open Folder ...", None))
    # retranslateUi

