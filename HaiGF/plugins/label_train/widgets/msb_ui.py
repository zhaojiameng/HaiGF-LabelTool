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
        self.runButton1 = QtWidgets.QPushButton(self.layoutWidget)
        self.runButton1.setObjectName('撤销')

        self.spacer1 = QWidget()
        self.spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer2 = QWidget()
        self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer3 = QWidget()
        self.spacer3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self.roiLabel = QtWidgets.QLabel(self.layoutWidget)
        self.roiLabel.setObjectName('ROI分析')
        self.roiButton = QtWidgets.QPushButton(self.layoutWidget)
        self.roiButton.setObjectName('分析')
        self.roiButton1 = QtWidgets.QPushButton(self.layoutWidget)
        self.roiButton1.setObjectName('撤销')

        

        self.annoLabel = QtWidgets.QLabel(self.layoutWidget)
        self.annoLabel.setObjectName('标注形状')
        self.annoButton = QtWidgets.QPushButton(self.layoutWidget)
        self.annoButton.setObjectName('标注')
        self.roiComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.roiComboBox.addItem("Line ROI")
        self.roiComboBox.addItem("Rect ROI")
        self.roiComboBox.addItem("Ellipse ROI")
        self.roiComboBox.addItem("Circle ROI")
        self.roiComboBox.addItem("PolyLine ROI")
        self.roiComboBox.addItem("Polygon ROI")

        self.isoLabel = QtWidgets.QLabel(self.layoutWidget)
        self.isoLabel.setObjectName('等值分析')
        self.isoButton = QtWidgets.QPushButton(self.layoutWidget)
        self.isoButton.setObjectName('分析')
        self.isoButton1 = QtWidgets.QPushButton(self.layoutWidget)
        self.isoButton1.setObjectName('撤销')
       

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        # self.runButton.clicked.connect()
        self.gridLayout.addWidget(self.cannyLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.threshold1SpinBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.threshold2SpinBox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.runButton, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.runButton1, 2, 1, 1, 1)

        self.gridLayout.addWidget(self.spacer1, 3, 0, 1, 2)

        self.gridLayout.addWidget(self.annoLabel, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.annoButton, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.roiComboBox, 5, 0, 1, 2)

        self.gridLayout.addWidget(self.spacer2,7, 0, 1, 2)

        self.gridLayout.addWidget(self.roiLabel, 8, 0, 1, 2)
        self.gridLayout.addWidget(self.roiButton, 9, 0, 1, 1)
        self.gridLayout.addWidget(self.roiButton1, 9, 1, 1, 1)

        self.gridLayout.addWidget(self.spacer3, 10, 0, 1, 2)

        self.gridLayout.addWidget(self.isoLabel, 11, 0, 1, 2)
        self.gridLayout.addWidget(self.isoButton, 12, 0, 1, 1)
        self.gridLayout.addWidget(self.isoButton1, 12, 1, 1, 1)




        self.gridLayout_2.addWidget(self.layoutWidget, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.spacer)

       



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Annotator & Trainer"))
        self.cannyLabel.setText(_translate("Form", "Canny边缘检测"))
        self.runButton.setText(_translate("Form", "运行"))
        self.runButton1.setText(_translate("Form", "撤销"))

        
        self.roiComboBox.setItemText(0, _translate("Form", "Line ROI"))
        self.roiComboBox.setItemText(1, _translate("Form", "Rect ROI"))
        self.roiComboBox.setItemText(2, _translate("Form", "Ellipse ROI"))
        self.roiComboBox.setItemText(3, _translate("Form", "Circle ROI"))
        self.roiComboBox.setItemText(4, _translate("Form", "PolyLine ROI"))
        self.roiComboBox.setItemText(5, _translate("Form", "BezierLine ROI"))
        self.roiLabel.setText(_translate("Form", "ROI分析"))
        self.roiButton.setText(_translate("Form", "应用"))
        self.roiButton1.setText(_translate("Form", "撤销"))
        self.annoLabel.setText(_translate("Form", "标注形状"))
        self.annoButton.setText(_translate("Form", "标注"))
        self.isoLabel.setText(_translate("Form", "等值分析"))
        self.isoButton.setText(_translate("Form", "应用"))
        self.isoButton1.setText(_translate("Form", "撤销"))


