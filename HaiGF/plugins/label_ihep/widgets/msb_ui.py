from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *

from HaiGF.gui_framework.utils.qt import newIcon
from ...label_train.common.radio_button import RadioButton



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

        self.fetchButton = QtWidgets.QPushButton(self.layoutWidget)
        self.fetchButton.setObjectName('获取数据')
        # Create a tree widget to display the data as a list
        self.tree = QtWidgets.QTreeWidget(self.layoutWidget)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["index","Record"])
        self.preButton = QtWidgets.QPushButton(self.layoutWidget)
        self.preButton.setObjectName('上一条')
        self.preButton.setEnabled(False)
        self.nextButton = QtWidgets.QPushButton(self.layoutWidget)
        self.nextButton.setObjectName('下一条')
        self.nextButton.setEnabled(False)

        self.autoUploadButton = RadioButton(self.layoutWidget, '自动上传', newIcon('autosave'))
        
        self.uploadButton = QtWidgets.QPushButton(self.layoutWidget)
        self.uploadButton.setObjectName('上传数据')
 
        self.saveButton = QtWidgets.QPushButton(self.layoutWidget)
        self.saveButton.setObjectName('保存数据')

        self.annotateUserLabel = QtWidgets.QLabel(self.layoutWidget)
        self.annotateUserLabel.setObjectName('标注人员')

        self.annotateUserEditer = QtWidgets.QLineEdit(self.layoutWidget)
        self.annotateUserEditer.setPlaceholderText('edit name here')


        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.spacer1 = QWidget()
        self.spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer2 = QWidget()
        self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer3 = QWidget()
        self.spacer3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.gridLayout.addWidget(self.fetchButton, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.tree, 1, 0, 2, 2)
        self.gridLayout.addWidget(self.preButton, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.nextButton, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.spacer1, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.autoUploadButton, 5, 0, 1, 2)
        self.gridLayout.addWidget(self.uploadButton, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.saveButton, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.spacer2, 7, 0, 1, 2)
        self.gridLayout.addWidget(self.annotateUserLabel, 8, 0, 1, 1)
        self.gridLayout.addWidget(self.annotateUserEditer, 8, 1, 1, 1)

        self.gridLayout_2.addWidget(self.layoutWidget, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.spacer)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Label Ihep Q&A"))
        self.fetchButton.setText(_translate("Form", "获取数据"))
        self.preButton.setText(_translate("Form", "上一条"))
        self.nextButton.setText(_translate("Form", "下一条"))
        self.autoUploadButton.setText(_translate("Form", "自动上传"))
        self.uploadButton.setText(_translate("Form", "上传数据"))
        self.saveButton.setText(_translate("Form", "保存数据"))
        self.annotateUserLabel.setText(_translate("Form", "标注人员:"))
        
        

        
        



