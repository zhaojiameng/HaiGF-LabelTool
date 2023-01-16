from HaiGF import HPage
from PySide2 import QtWidgets, QtGui
import cv2
import numpy as np

class Canvas_1(HPage):
    def __init__(self, parent=None, icon=None, title=None, **kwargs):
        super().__init__(parent, icon, title, **kwargs)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.img = QtWidgets.QLabel(self)
        self.img.setObjectName("img")
        self.openImg = QtWidgets.QPushButton(self)
        self.openImg.setObjectName("openImg")
        self.openImg.clicked.connect(self.load_img(filePath='000000.jpg'))
        self.horizontalLayout.addWidget(self.img)
        self.horizontalLayout.addWidget(self.openImg)

    def load_img(self,filePath):
        image = QtGui.QPixmap(filePath)
        self.img.setPixmap(image)
        self.img.show()

    def mouseDoubleClickEvent(self, event):
        return super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        return super().mousePressEvent(event)

    def wheelEvent(self, event):
        """
        鼠标滚动时，画布在窗体内放缩
        """
        if self.item:
            if (event.angleDelta().y() > 0.5):
                
                self.zoomscale = self.zoomscale * 1.2
            
            elif (event.angleDelta().y() < 0.5):
                
                self.zoomscale = self.zoomscale / 1.2

            self.item.setScale(self.zoomscale)

