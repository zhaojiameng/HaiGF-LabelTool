


from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *



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
        
        self.cannyLabel = QtWidgets.QLabel(self.layoutWidget)
        self.cannyLabel.setObjectName('Canny标签')
        
        
        self.threshold1SpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        
        self.threshold1SpinBox.setMinimum(0)
        self.threshold1SpinBox.setMaximum(255)
        self.threshold1SpinBox.setValue(50)
        
        self.threshold2SpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        
        self.threshold2SpinBox.setMinimum(0)
        self.threshold2SpinBox.setMaximum(255)
        self.threshold2SpinBox.setValue(150)
        
        self.runButton = QtWidgets.QPushButton(self.layoutWidget)
        self.runButton.setObjectName('运行')

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        # self.runButton.clicked.connect()
        self.gridLayout.addWidget(self.cannyLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.threshold1SpinBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.threshold2SpinBox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.runButton, 2, 0, 1, 2)

        self.gridLayout_2.addWidget(self.layoutWidget, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.spacer)

       



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Annotator & Trainer"))
        self.cannyLabel.setText(_translate("Form", "Canny边缘检测"))
        self.runButton.setText(_translate("Form", "运行"))
