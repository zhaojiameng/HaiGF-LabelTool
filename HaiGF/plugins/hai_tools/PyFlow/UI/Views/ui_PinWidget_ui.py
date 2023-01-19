# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PinWidget_ui.ui'
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
        Form.resize(168, 75)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lePinName = QLineEdit(Form)
        self.lePinName.setObjectName(u"lePinName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lePinName.sizePolicy().hasHeightForWidth())
        self.lePinName.setSizePolicy(sizePolicy1)
        self.lePinName.setMinimumSize(QSize(0, 0))
        self.lePinName.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.lePinName)

        self.cbType = QComboBox(Form)
        self.cbType.setObjectName(u"cbType")
        sizePolicy1.setHeightForWidth(self.cbType.sizePolicy().hasHeightForWidth())
        self.cbType.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.cbType)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cbHideLabel = QCheckBox(Form)
        self.cbHideLabel.setObjectName(u"cbHideLabel")

        self.horizontalLayout_2.addWidget(self.cbHideLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lePinName.setText(QCoreApplication.translate("Form", u"pinName", None))
#if QT_CONFIG(tooltip)
        self.cbHideLabel.setToolTip(QCoreApplication.translate("Form", u"should hide label", None))
#endif // QT_CONFIG(tooltip)
        self.cbHideLabel.setText(QCoreApplication.translate("Form", u"hide label", None))
    # retranslateUi

