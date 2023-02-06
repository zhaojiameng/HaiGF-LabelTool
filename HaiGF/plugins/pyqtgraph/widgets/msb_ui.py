


from pyqtgraph.Qt import QtCore, QtGui, QtWidgets


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
        self.qtLibCombo = QtWidgets.QComboBox(self.layoutWidget)  # 
        self.qtLibCombo.setObjectName("qtLibCombo")
        self.gridLayout.addWidget(self.qtLibCombo, 4, 1, 1, 1)
        self.loadBtn = QtWidgets.QPushButton(self.layoutWidget)  # 运行按钮
        self.loadBtn.setObjectName("loadBtn")
        self.gridLayout.addWidget(self.loadBtn, 6, 1, 1, 1)
        self.exampleTree = QtWidgets.QTreeWidget(self.layoutWidget)  # 列表
        self.exampleTree.setObjectName("exampleTree")
        self.exampleTree.headerItem().setText(0, "1")
        self.exampleTree.header().setVisible(False)
        self.gridLayout.addWidget(self.exampleTree, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.layoutWidget)  # 左下角的Qt Library
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.exampleFilter = QtWidgets.QLineEdit(self.layoutWidget)
        self.exampleFilter.setObjectName("exampleFilter")
        self.gridLayout.addWidget(self.exampleFilter, 0, 0, 1, 2)
        self.searchFiles = QtWidgets.QComboBox(self.layoutWidget)
        self.searchFiles.setObjectName("searchFiles")
        self.searchFiles.addItem("")
        self.searchFiles.addItem("")
        self.gridLayout.addWidget(self.searchFiles, 1, 0, 1, 2)

        # self.layoutWidget1 = QtWidgets.QWidget(self.splitter)  # 右边的代码窗口
        # self.layoutWidget1.setObjectName("layoutWidget1")
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        # self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout.setObjectName("verticalLayout")
        # self.loadedFileLabel = QtWidgets.QLabel(self.layoutWidget1)
        # font = QtGui.QFont()
        # font.setBold(True)
        # self.loadedFileLabel.setFont(font)
        # self.loadedFileLabel.setText("")
        # self.loadedFileLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.loadedFileLabel.setObjectName("loadedFileLabel")
        # self.verticalLayout.addWidget(self.loadedFileLabel)
        # self.codeView = QtWidgets.QPlainTextEdit(self.layoutWidget1)  # 右侧的代码窗口
        # font = QtGui.QFont()
        # font.setFamily("Courier New")
        # self.codeView.setFont(font)
        # self.codeView.setObjectName("codeView")
        # self.verticalLayout.addWidget(self.codeView)

        # self.gridLayout_2.addWidget(self.splitter, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.layoutWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyQtGraph"))
        self.loadBtn.setText(_translate("Form", "Run Example"))
        self.label.setText(_translate("Form", "Qt Library:"))
        self.exampleFilter.setPlaceholderText(_translate("Form", "Type to filter..."))
        self.searchFiles.setItemText(0, _translate("Form", "Title Search"))
        self.searchFiles.setItemText(1, _translate("Form", "Content Search"))

