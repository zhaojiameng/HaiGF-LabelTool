from PySide2.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QGridLayout, QSizePolicy, QSplitter
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import numpy as np
from src.utils import general


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QGridLayout()
        layout.setMargin(0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.setGeometry(0, 0, 800, 600)


        label = QLabel(self)
        label.setText("Hello World")
        label.setStyleSheet("background-color: red;")
        label.move(300, 100)

        label2 = QLabel(self)
        label2.setText("Hello World2")
        label2.setStyleSheet("background-color: green;")

        label3 = QLabel(self)
        label3.setText("Hello World3")
        label3.setStyleSheet("background-color: blue;")
        # label3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        label4 = QLabel(self)
        label4.setText("Hello World4")
        label4.setStyleSheet("background-color: yellow;")

        # label3.set_pos(label.Bottom)
        # label2.set_pos(label.Right)

        spl = QSplitter(Qt.Horizontal)
        spl2 = QSplitter(Qt.Horizontal)
        spl3 = QSplitter(Qt.Vertical)
        # spl.setParent(self)
        spl.addWidget(label)
        spl.addWidget(label2)
        spl2.addWidget(label3)
        # spl.setParent(spl2)
        spl2.addWidget(label4)
        spl3.addWidget(spl)
        spl3.addWidget(spl2)
        
        # spl2.addWidget(label2)

        layout.addWidget(spl3)
        
        # layout.addWidget(spl2, 1, 0, 1, 2)
        # spl2.setParent(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
