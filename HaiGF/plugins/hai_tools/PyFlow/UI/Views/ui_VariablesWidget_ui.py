# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VariablesWidget_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(341, 363)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pbNewVar = QPushButton(Form)
        self.pbNewVar.setObjectName(u"pbNewVar")
        self.pbNewVar.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.pbNewVar)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.wListWidget = QWidget(Form)
        self.wListWidget.setObjectName(u"wListWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wListWidget.sizePolicy().hasHeightForWidth())
        self.wListWidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.wListWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.lytListWidget = QVBoxLayout()
        self.lytListWidget.setObjectName(u"lytListWidget")

        self.gridLayout.addLayout(self.lytListWidget, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.wListWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Create var", None))
        self.pbNewVar.setText(QCoreApplication.translate("Form", u"+", None))
    # retranslateUi

