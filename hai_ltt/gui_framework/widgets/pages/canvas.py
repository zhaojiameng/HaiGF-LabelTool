

from hai_ltt.gui_framework.widgets.common.hai_page import HPage
from PySide2 import QtWidgets, QtGui
import cv2
import numpy as np


# def load_canvas(self):
#     return

class Canvas(HPage):
    def __init__(self, parent=None, icon=None, title=None, **kwargs):
        super().__init__(parent, icon, title, **kwargs)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setScene(self.scene)
        self.zoomscale=1      #图片放缩尺度
        self.addImg = QtWidgets.QPushButton(self)
        self.addImg.setObjectName("addImg") 
        self.addImg.clicked.connect(self.load_image)                                      
        self.horizontalLayout.addWidget(self.graphicsView)
        self.horizontalLayout.addWidget(self.addImg)
        self.item = None



    def load_image(self):
        """
        根据图片路径加载图片
        """
        filePath = '000000.jpg'
        img = cv2.imread(filePath)
        # img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)

        cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 把opencv 默认BGR转为通用的RGB
        y, x = img.shape[:-1]
        frame = QtGui.QImage(cvimg, x, y, QtGui.QImage.Format_RGB888)
        self.scene.clear()  #先清空上次的残留
        pix = QtGui.QPixmap.fromImage(frame).scaled(self.scene.size())
        self.item = QtWidgets.QGraphicsPixmapItem(pix)
        self.scene.addItem(self.item)
        # self.scene.setSceneRect(-x/2, -y/2, x, y)
        # self.scene.addPixmap(self.pix)

        # self.graphicsView.scene_img = QGraphicsScene()
        # self.imgShow = QPixmap()
        # self.imgShow.load(fileName)
        # self.imgShowItem = QGraphicsPixmapItem()
        # self.imgShowItem.setPixmap(QPixmap(self.imgShow))
        # #self.imgShowItem.setPixmap(QPixmap(self.imgShow).scaled(8000,  8000))    #自己设定尺寸
        # self.graphicsView.fitInView(QGraphicsPixmapItem(QPixmap(self.imgShow)))    #图像自适应大小
        


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
