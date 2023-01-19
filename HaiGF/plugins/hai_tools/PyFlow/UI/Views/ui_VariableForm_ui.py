# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VariableForm_ui.ui'
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
        Form.resize(228, 30)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout.addWidget(self.widget)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.horizontalLayout.addWidget(self.labelName)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pbKill = QPushButton(Form)
        self.pbKill.setObjectName(u"pbKill")
        self.pbKill.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.pbKill)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"var name", None))
        self.pbKill.setText("")
    # retranslateUi

