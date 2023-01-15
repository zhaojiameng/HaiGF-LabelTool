# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'example.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import GraphicsLayoutWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1328, 895)
        font = QFont()
        font.setPointSize(11)
        Form.setFont(font)
        Form.setStyleSheet(u"")
        self.Buttons = QLabel(Form)
        self.Buttons.setObjectName(u"Buttons")
        self.Buttons.setGeometry(QRect(40, 110, 91, 20))
        font1 = QFont()
        font1.setPointSize(15)
        self.Buttons.setFont(font1)
        self.buttonsGroup = QGroupBox(Form)
        self.buttonsGroup.setObjectName(u"buttonsGroup")
        self.buttonsGroup.setGeometry(QRect(20, 130, 171, 231))
        self.button = QPushButton(self.buttonsGroup)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(10, 10, 151, 41))
        self.button.setFont(font1)
        self.flatButton = QPushButton(self.buttonsGroup)
        self.flatButton.setObjectName(u"flatButton")
        self.flatButton.setGeometry(QRect(10, 60, 151, 41))
        self.flatButton.setFont(font1)
        self.flatButton.setStyleSheet(u"QPushButton#highLight{\n"
"rgb(0, 85, 255)\n"
"}")
        self.flatButton.setFlat(True)
        self.highLight = QPushButton(self.buttonsGroup)
        self.highLight.setObjectName(u"highLight")
        self.highLight.setGeometry(QRect(10, 110, 151, 41))
        self.highLight.setFont(font1)
        self.highLight.setStyleSheet(u"QPushButton#highLight{\n"
"background-color:rgb(85, 170, 255);\n"
"}")
        self.highLight.setAutoDefault(False)
        self.roundButton = QPushButton(self.buttonsGroup)
        self.roundButton.setObjectName(u"roundButton")
        self.roundButton.setGeometry(QRect(50, 160, 60, 60))
        self.roundButton.setMinimumSize(QSize(60, 60))
        self.roundButton.setMaximumSize(QSize(60, 60))
        self.roundButton.setFont(font1)
        self.roundButton.setStyleSheet(u"QPushButton{\n"
"border-radius:30px;\n"
"border:2px groove gragy;\n"
"border-style:outset;\n"
"border:none;\n"
"background-color:rgb(229, 229, 229);\n"
"}")
        self.RadioButtons = QLabel(Form)
        self.RadioButtons.setObjectName(u"RadioButtons")
        self.RadioButtons.setGeometry(QRect(40, 380, 141, 20))
        self.RadioButtons.setFont(font1)
        self.radioButtonsGroup = QGroupBox(Form)
        self.radioButtonsGroup.setObjectName(u"radioButtonsGroup")
        self.radioButtonsGroup.setGeometry(QRect(20, 410, 171, 281))
        self.radioButton = QRadioButton(self.radioButtonsGroup)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(10, 30, 151, 21))
        self.radioButton.setFont(font1)
        self.radioButton.setStyleSheet(u"")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QRadioButton(self.radioButtonsGroup)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(10, 110, 151, 16))
        self.radioButton_2.setFont(font1)
        self.radioButton_2.setIconSize(QSize(16, 21))
        self.radioButton_3 = QRadioButton(self.radioButtonsGroup)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(10, 180, 151, 16))
        self.radioButton_3.setFont(font1)
        self.radioButton_4 = QRadioButton(self.radioButtonsGroup)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(10, 250, 151, 16))
        self.radioButton_4.setFont(font1)
        self.checkBoxes = QLabel(Form)
        self.checkBoxes.setObjectName(u"checkBoxes")
        self.checkBoxes.setGeometry(QRect(220, 110, 141, 20))
        self.checkBoxes.setFont(font1)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(200, 130, 191, 231))
        self.checksGroup = QGroupBox(self.groupBox)
        self.checksGroup.setObjectName(u"checksGroup")
        self.checksGroup.setGeometry(QRect(20, 70, 161, 141))
        self.checksGroup.setStyleSheet(u"QGroupBox#checksGroup{\n"
"border:none;\n"
"}")
        self.checksGroup.setFlat(True)
        self.checkBox = QCheckBox(self.checksGroup)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(10, 10, 131, 16))
        self.checkBox.setFont(font1)
        self.checkBox_2 = QCheckBox(self.checksGroup)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(40, 40, 91, 16))
        self.checkBox_2.setFont(font1)
        self.checkBox_3 = QCheckBox(self.checksGroup)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(40, 80, 101, 16))
        self.checkBox_3.setFont(font1)
        self.tabs = QLabel(Form)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setGeometry(QRect(830, 110, 141, 20))
        self.tabs.setFont(font1)
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(410, 130, 191, 231))
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 11, 131, 31))
        self.comboBox.setFont(font1)
        self.flatComboBox = QComboBox(self.groupBox_2)
        self.flatComboBox.addItem("")
        self.flatComboBox.addItem("")
        self.flatComboBox.addItem("")
        self.flatComboBox.setObjectName(u"flatComboBox")
        self.flatComboBox.setEnabled(True)
        self.flatComboBox.setGeometry(QRect(10, 70, 131, 31))
        self.flatComboBox.setFont(font1)
        self.flatComboBox.setStyleSheet(u"QComboBox#flatComboBox{\n"
"flat:true;\n"
"}")
        self.editComboBox = QComboBox(self.groupBox_2)
        self.editComboBox.addItem("")
        self.editComboBox.addItem("")
        self.editComboBox.addItem("")
        self.editComboBox.setObjectName(u"editComboBox")
        self.editComboBox.setGeometry(QRect(10, 130, 131, 31))
        self.editComboBox.setFont(font1)
        self.editComboBox.setEditable(True)
        self.numberComboBox = QComboBox(self.groupBox_2)
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.addItem("")
        self.numberComboBox.setObjectName(u"numberComboBox")
        self.numberComboBox.setGeometry(QRect(10, 190, 131, 31))
        self.numberComboBox.setFont(font1)
        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(620, 130, 181, 231))
        self.groupBox_3.setFont(font1)
        self.groupBox_3.setLayoutDirection(Qt.LeftToRight)
        self.spinBox = QSpinBox(self.groupBox_3)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(20, 11, 131, 41))
        self.spinBox.setFont(font1)
        self.spinBox.setLayoutDirection(Qt.LeftToRight)
        self.spinBox.setStyleSheet(u"QSpinBox::up-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:right;\n"
"width:40px;\n"
"height:40px;\n"
"\n"
"}\n"
"QSpinBox::down-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:left;\n"
"width:40px;\n"
"height:40px;\n"
"}")
        self.spinBox.setAlignment(Qt.AlignCenter)
        self.spinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBox.setMinimum(2)
        self.spinBox.setMaximum(50)
        self.textSpinBoxes = QSpinBox(self.groupBox_3)
        self.textSpinBoxes.setObjectName(u"textSpinBoxes")
        self.textSpinBoxes.setGeometry(QRect(20, 80, 131, 41))
        self.textSpinBoxes.setFont(font1)
        self.textSpinBoxes.setStyleSheet(u"QSpinBox::up-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:right;\n"
"width:40px;\n"
"height:40px;\n"
"}\n"
"QSpinBox::down-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:left;\n"
"width:40px;\n"
"height:40px;\n"
"}")
        self.textSpinBoxes.setAlignment(Qt.AlignCenter)
        self.textSpinBoxes.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.doubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setGeometry(QRect(20, 160, 131, 41))
        self.doubleSpinBox.setStyleSheet(u"QDoubleSpinBox::up-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:right;\n"
"width:40px;\n"
"height:40px;\n"
"}\n"
"QDoubleSpinBox::down-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:left;\n"
"width:40px;\n"
"height:40px;\n"
"}")
        self.doubleSpinBox.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.comboBoxes = QLabel(Form)
        self.comboBoxes.setObjectName(u"comboBoxes")
        self.comboBoxes.setGeometry(QRect(420, 110, 141, 20))
        self.comboBoxes.setFont(font1)
        self.spinBoxes = QLabel(Form)
        self.spinBoxes.setObjectName(u"spinBoxes")
        self.spinBoxes.setGeometry(QRect(630, 110, 141, 20))
        self.spinBoxes.setFont(font1)
        self.menuBar = QFrame(Form)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(10, 10, 1311, 91))
        self.menuBar.setAutoFillBackground(True)
        self.menuBar.setStyleSheet(u"#menuBar{\n"
"backgroud:rgb(202, 202, 202);\n"
"}")
        self.menuBar.setFrameShape(QFrame.Box)
        self.menuBar.setFrameShadow(QFrame.Plain)
        self.comboBoxes_2 = QLabel(self.menuBar)
        self.comboBoxes_2.setObjectName(u"comboBoxes_2")
        self.comboBoxes_2.setGeometry(QRect(520, 50, 141, 20))
        self.comboBoxes_2.setFont(font1)
        self.fileTool = QPushButton(self.menuBar)
        self.fileTool.setObjectName(u"fileTool")
        self.fileTool.setGeometry(QRect(20, 0, 71, 21))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setUnderline(False)
        self.fileTool.setFont(font2)
        self.fileTool.setFlat(True)
        self.editTool = QPushButton(self.menuBar)
        self.editTool.setObjectName(u"editTool")
        self.editTool.setGeometry(QRect(100, 0, 71, 21))
        self.editTool.setFont(font)
        self.editTool.setFlat(True)
        self.helpTool = QPushButton(self.menuBar)
        self.helpTool.setObjectName(u"helpTool")
        self.helpTool.setGeometry(QRect(180, 0, 71, 21))
        self.helpTool.setFont(font)
        self.helpTool.setFlat(True)
        self.action1 = QPushButton(self.menuBar)
        self.action1.setObjectName(u"action1")
        self.action1.setGeometry(QRect(930, 60, 71, 21))
        self.action1.setFont(font)
        self.action1.setFlat(True)
        self.action2 = QPushButton(self.menuBar)
        self.action2.setObjectName(u"action2")
        self.action2.setGeometry(QRect(1000, 60, 71, 21))
        self.action2.setFont(font)
        self.action2.setFlat(True)
        self.action3 = QPushButton(self.menuBar)
        self.action3.setObjectName(u"action3")
        self.action3.setGeometry(QRect(1090, 60, 71, 21))
        self.action3.setFont(font)
        self.action3.setFlat(True)
        self.action4 = QPushButton(self.menuBar)
        self.action4.setObjectName(u"action4")
        self.action4.setGeometry(QRect(1170, 60, 71, 21))
        self.action4.setFont(font)
        self.action4.setFlat(True)
        self.line = QFrame(self.menuBar)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(1070, 30, 16, 51))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.RadioButtons_2 = QLabel(Form)
        self.RadioButtons_2.setObjectName(u"RadioButtons_2")
        self.RadioButtons_2.setGeometry(QRect(200, 380, 191, 20))
        self.RadioButtons_2.setFont(font1)
        self.radioButtonsGroup_2 = QGroupBox(Form)
        self.radioButtonsGroup_2.setObjectName(u"radioButtonsGroup_2")
        self.radioButtonsGroup_2.setGeometry(QRect(200, 410, 191, 281))
        self.progressBar = QProgressBar(self.radioButtonsGroup_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(30, 220, 118, 23))
        self.progressBar.setStyleSheet(u"QProgressBar{\n"
"text-align:center;\n"
"background-color:rgb(207, 207, 207);\n"
"color:rgb(0, 0, 0);\n"
"border-style:none;\n"
"border-radius:10px;\n"
"}")
        self.progressBar.setValue(24)
        self.radioButtonsGroup_3 = QGroupBox(Form)
        self.radioButtonsGroup_3.setObjectName(u"radioButtonsGroup_3")
        self.radioButtonsGroup_3.setGeometry(QRect(410, 410, 191, 281))
        self.dial = QDial(self.radioButtonsGroup_3)
        self.dial.setObjectName(u"dial")
        self.dial.setGeometry(QRect(0, 0, 181, 121))
        self.dial.setValue(0)
        self.dial.setSliderPosition(0)
        self.horizontalSlider = QSlider(self.radioButtonsGroup_3)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(10, 251, 161, 21))
        self.horizontalSlider.setStyleSheet(u"/*\u69fd*/\n"
"#horizontalSlider::groove:horizontal {\n"
"height:12px; \n"
"left:0px; \n"
"right:0px; \n"
"border:0px;   \n"
"border-radius:6px;\n"
"background:rgb(217, 217, 217) \n"
"}\n"
"/*\u5df2\u7ecf\u5212\u8fc7\u7684*/\n"
"#horizontalSlider::sub-page:horizontal{\n"
"background:rgb(0, 0, 0);\n"
"}\n"
"#horizontalSlider::handle:horizontal{\n"
"width:30px;\n"
"height:30px;\n"
"background-color:rgb(255,255,255);\n"
"margin:-11px 0px -11px 0px;\n"
"border-radius:15px;\n"
"}\n"
"")
        self.horizontalSlider.setValue(19)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.RadioButtons_3 = QLabel(Form)
        self.RadioButtons_3.setObjectName(u"RadioButtons_3")
        self.RadioButtons_3.setGeometry(QRect(410, 380, 191, 20))
        self.RadioButtons_3.setFont(font1)
        self.RadioButtons_4 = QLabel(Form)
        self.RadioButtons_4.setObjectName(u"RadioButtons_4")
        self.RadioButtons_4.setGeometry(QRect(620, 380, 191, 20))
        self.RadioButtons_4.setFont(font1)
        self.radioButtonsGroup_4 = QGroupBox(Form)
        self.radioButtonsGroup_4.setObjectName(u"radioButtonsGroup_4")
        self.radioButtonsGroup_4.setGeometry(QRect(620, 410, 181, 281))
        self.lineEdit = QLineEdit(self.radioButtonsGroup_4)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 10, 161, 41))
        self.readLine = QLineEdit(self.radioButtonsGroup_4)
        self.readLine.setObjectName(u"readLine")
        self.readLine.setGeometry(QRect(10, 80, 161, 41))
        self.readLine.setReadOnly(True)
        self.textEdit = QTextEdit(self.radioButtonsGroup_4)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 150, 161, 121))
        self.textEdit.setStyleSheet(u"QTextEdit{\n"
"border:none;\n"
"background:rgb(241, 241, 241);\n"
"}")
        self.RadioButtons_5 = QLabel(Form)
        self.RadioButtons_5.setObjectName(u"RadioButtons_5")
        self.RadioButtons_5.setGeometry(QRect(10, 720, 121, 20))
        self.RadioButtons_5.setFont(font1)
        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(130, 710, 131, 31))
        self.comboBox_2.setFont(font1)
        self.comboBox_3 = QComboBox(Form)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(360, 710, 131, 31))
        self.comboBox_3.setFont(font1)
        self.RadioButtons_6 = QLabel(Form)
        self.RadioButtons_6.setObjectName(u"RadioButtons_6")
        self.RadioButtons_6.setGeometry(QRect(290, 720, 61, 20))
        self.RadioButtons_6.setFont(font1)
        self.comboBox_4 = QComboBox(Form)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setGeometry(QRect(620, 710, 131, 31))
        self.comboBox_4.setFont(font1)
        self.RadioButtons_7 = QLabel(Form)
        self.RadioButtons_7.setObjectName(u"RadioButtons_7")
        self.RadioButtons_7.setGeometry(QRect(510, 720, 101, 20))
        self.RadioButtons_7.setFont(font1)
        self.comboBox_5 = QComboBox(Form)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setGeometry(QRect(920, 710, 131, 31))
        self.comboBox_5.setFont(font1)
        self.RadioButtons_8 = QLabel(Form)
        self.RadioButtons_8.setObjectName(u"RadioButtons_8")
        self.RadioButtons_8.setGeometry(QRect(780, 720, 71, 20))
        self.RadioButtons_8.setFont(font1)
        self.RadioButtons_9 = QLabel(Form)
        self.RadioButtons_9.setObjectName(u"RadioButtons_9")
        self.RadioButtons_9.setGeometry(QRect(850, 720, 71, 20))
        self.RadioButtons_9.setFont(font1)
        self.RadioButtons_10 = QLabel(Form)
        self.RadioButtons_10.setObjectName(u"RadioButtons_10")
        self.RadioButtons_10.setGeometry(QRect(1060, 720, 91, 20))
        self.RadioButtons_10.setFont(font1)
        self.comboBox_6 = QComboBox(Form)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setGeometry(QRect(1150, 710, 131, 31))
        self.comboBox_6.setFont(font1)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(820, 150, 491, 541))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 120, 471, 411))
        self.page = GraphicsLayoutWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = GraphicsLayoutWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.barButton = QPushButton(self.frame)
        self.barButton.setObjectName(u"barButton")
        self.barButton.setGeometry(QRect(10, 20, 91, 41))
        self.barButton.setFont(font1)
        self.barButton.setFlat(True)
        self.spineButton = QPushButton(self.frame)
        self.spineButton.setObjectName(u"spineButton")
        self.spineButton.setGeometry(QRect(110, 20, 81, 41))
        self.spineButton.setFont(font1)
        self.spineButton.setFlat(True)

        self.retranslateUi(Form)

        self.highLight.setDefault(True)
        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Buttons.setText(QCoreApplication.translate("Form", u"Buttons", None))
        self.buttonsGroup.setTitle("")
        self.button.setText(QCoreApplication.translate("Form", u"Button", None))
        self.flatButton.setText(QCoreApplication.translate("Form", u"Flat", None))
        self.highLight.setText(QCoreApplication.translate("Form", u"Highlight", None))
        self.roundButton.setText(QCoreApplication.translate("Form", u"+", None))
        self.RadioButtons.setText(QCoreApplication.translate("Form", u"Radio Buttons", None))
        self.radioButtonsGroup.setTitle("")
        self.radioButton.setText(QCoreApplication.translate("Form", u"Radio Button1", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"Radio Button2", None))
        self.radioButton_3.setText(QCoreApplication.translate("Form", u"Radio Button3", None))
        self.radioButton_4.setText(QCoreApplication.translate("Form", u"Radio Button4", None))
        self.checkBoxes.setText(QCoreApplication.translate("Form", u"Check Boxes", None))
        self.groupBox.setTitle("")
        self.checksGroup.setTitle("")
        self.checkBox.setText(QCoreApplication.translate("Form", u"Parent", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"Child1", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"Child2", None))
        self.tabs.setText(QCoreApplication.translate("Form", u"Tabs", None))
        self.groupBox_2.setTitle("")
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"Normal", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.flatComboBox.setItemText(0, QCoreApplication.translate("Form", u"Flat", None))
        self.flatComboBox.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.flatComboBox.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.editComboBox.setItemText(0, QCoreApplication.translate("Form", u"Editable", None))
        self.editComboBox.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.editComboBox.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.numberComboBox.setItemText(0, QCoreApplication.translate("Form", u"0", None))
        self.numberComboBox.setItemText(1, QCoreApplication.translate("Form", u"1", None))
        self.numberComboBox.setItemText(2, QCoreApplication.translate("Form", u"2", None))
        self.numberComboBox.setItemText(3, QCoreApplication.translate("Form", u"3", None))
        self.numberComboBox.setItemText(4, QCoreApplication.translate("Form", u"4", None))
        self.numberComboBox.setItemText(5, QCoreApplication.translate("Form", u"5", None))
        self.numberComboBox.setItemText(6, QCoreApplication.translate("Form", u"6", None))
        self.numberComboBox.setItemText(7, QCoreApplication.translate("Form", u"7", None))
        self.numberComboBox.setItemText(8, QCoreApplication.translate("Form", u"8", None))
        self.numberComboBox.setItemText(9, QCoreApplication.translate("Form", u"9", None))

        self.groupBox_3.setTitle("")
        self.comboBoxes.setText(QCoreApplication.translate("Form", u"ComboBoxes", None))
        self.spinBoxes.setText(QCoreApplication.translate("Form", u"Spin Boxes", None))
        self.comboBoxes_2.setText(QCoreApplication.translate("Form", u"Example", None))
        self.fileTool.setText(QCoreApplication.translate("Form", u"File", None))
        self.editTool.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.helpTool.setText(QCoreApplication.translate("Form", u"Help", None))
        self.action1.setText(QCoreApplication.translate("Form", u"Action1", None))
        self.action2.setText(QCoreApplication.translate("Form", u"Action2", None))
        self.action3.setText(QCoreApplication.translate("Form", u"Action3", None))
        self.action4.setText(QCoreApplication.translate("Form", u"Action4", None))
        self.RadioButtons_2.setText(QCoreApplication.translate("Form", u"Progress Indicators", None))
        self.radioButtonsGroup_2.setTitle("")
        self.radioButtonsGroup_3.setTitle("")
        self.RadioButtons_3.setText(QCoreApplication.translate("Form", u"Range Controllers", None))
        self.RadioButtons_4.setText(QCoreApplication.translate("Form", u"Text Inputs", None))
        self.radioButtonsGroup_4.setTitle("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Enter something here", None))
        self.readLine.setText(QCoreApplication.translate("Form", u"Read Only", None))
        self.readLine.setPlaceholderText("")
        self.textEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Multi-line text editor..", None))
        self.RadioButtons_5.setText(QCoreApplication.translate("Form", u"Chart Theme:", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"Normal", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"Normal", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.RadioButtons_6.setText(QCoreApplication.translate("Form", u"Theme:", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("Form", u"Normal", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.RadioButtons_7.setText(QCoreApplication.translate("Form", u"Sub-Theme:", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("Form", u"Normal", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.RadioButtons_8.setText(QCoreApplication.translate("Form", u"Colors:", None))
        self.RadioButtons_9.setText(QCoreApplication.translate("Form", u"Accent", None))
        self.RadioButtons_10.setText(QCoreApplication.translate("Form", u"Primarty", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Form", u"Normal", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("Form", u"Second", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("Form", u"Third", None))

        self.barButton.setText(QCoreApplication.translate("Form", u"Bar", None))
        self.spineButton.setText(QCoreApplication.translate("Form", u"Spine", None))
    # retranslateUi

