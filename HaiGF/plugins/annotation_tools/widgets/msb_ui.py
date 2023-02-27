


from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *

from HaiGF import HGF



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(846, 552)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")

        self.layoutWidget = QtWidgets.QWidget(self.splitter)  # 左边的树形结构
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.btn1 = QToolButton()
        self.btn1.setIcon(HGF.ICONS('ai.png'))
        self.btn1.setToolTip('创建矩形')

        self.btn2 = QToolButton()
        self.btn2.setIcon(HGF.ICONS('close.png'))
        self.btn2.setToolTip('创建圆形')

        self.btn3 = QToolButton()
        self.btn3.setIcon(HGF.ICONS('me.png'))
        self.btn3.setToolTip('创建不规则多边形')

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        # self.runButton.clicked.connect()
        self.gridLayout.addWidget(self.btn1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.btn2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.btn3, 2, 0, 1, 1)
       

        self.gridLayout_2.addWidget(self.layoutWidget, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.spacer)

       



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Annotator & Trainer"))
       
