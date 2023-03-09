"""
The cw page 2.
It is a  mafnification page.
"""
import os
from pathlib import Path
import cv2
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QRectF, QSizeF, QPoint
from PySide2.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QFont, QCursor
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMenu, QAction, QLineEdit, QDialog, QDialogButtonBox, QVBoxLayout, QFileDialog, QInputDialog, QMessageBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from HaiGF import HPage, HGF
import copy
import xml.etree.ElementTree as ET
import json
import damei as dm

logger = dm.get_logger('cw_page')
here = Path(__file__).parent.parent

class LabelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Label')
        self.layout = QVBoxLayout(self)
        self.label_edit = QLineEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.layout.addWidget(self.label_edit)
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
  
class RectangleItem(QGraphicsRectItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.label = ''

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

class ImageMagnificationPage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('magnifaication'))
        self.set_icon(HGF.ICONS('label_train'))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_rightmenu)
       
        self.rect_items = []
        self.rect_item = None
        self.drawing = False
        self.label_dialog = LabelDialog(self)
    
        self.image = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
      
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.win = pg.GraphicsLayoutWidget()
        self.win.resize(800, 800)
    
        self.layout.addWidget(self.win)
        self.p1 = self.win.addPlot(title="")
        self.p1.setMenuEnabled(False)
    
        # Item for displaying image data
        self.img = pg.ImageItem(border='w')
        self.p1.addItem(self.img)
        self.setMouseTracking(True)
        self.p1.scene().mousePressEvent = self.mousePressEvent
        self.p1.scene().mouseMoveEvent = self.mouseMoveEvent
        self.p1.scene().mouseReleaseEvent = self.mouseReleaseEvent
        self.win.show()
    def show_image(self, image):
        self.image = image
        self.img.setImage(image)
        self.img.setRect(QRectF(0, 0, image.shape[1], image.shape[0]))
       
    def create_ROI(self):
        """create a ROI"""
        self.roi = RectangleItem([20, 40], [20, 50], movable=True,removable=True)
        self.p1.addItem(self.roi)
        self.roi.setZValue(10)  # make sure ROI is drawn above image

    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     if hasattr(self, 'start_point') and hasattr(self, 'end_point'):
    #         painter = QPainter(self)
    #         painter.setPen(QPen(QColor(255, 0, 0), 1))
    #         line_path = QtGui.QPainterPath()
    #         line_path.addRect(self.start_point.x(), self.start_point.y(), self.end_point.x() - self.start_point.x(), self.end_point.y() - self.start_point.y())
    #         painter.drawPath(line_path)

    #event.pos 是什么？
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.drawing:
                self.drawing = True
                # Get global position of mouse cursor
                pos = QCursor.pos()
                print(pos)
                pos = QPoint(pos.x() - 717, pos.y() - 88)
                print('-------------')
                print(pos)
                self.start_point = pos
                self.rect_item = RectangleItem(QRectF(pos.x(), pos.y(), 0, 0))
                self.rect_item.setPen(QPen(QColor(0, 255, 0), 1))
                self.p1.scene().addItem(self.rect_item)
                self.rect_item.setZValue(10)
        
    def mouseMoveEvent(self, event):
        if self.drawing:
            pos = QCursor.pos()
            # pos = self.p1.mapToScene(event.pos())
            pos = QPoint(pos.x() - 717, pos.y() - 88)

            self.rect_item.setRect(self.start_point.x(), self.start_point.y(), pos.x() - self.start_point.x(), pos.y() - self.start_point.y())
            self.end_point = pos
                  
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing:
                self.end_point = QCursor.pos()
                self.end_point = QPoint(self.end_point.x() - 717, self.end_point.y() - 88)
                # self.end_point = self.p1.mapToScene(event.pos())
                print(self.start_point, self.end_point)
                self.rect_item.setRect(self.start_point.x(), self.start_point.y(), self.end_point.x() - self.start_point.x(), self.end_point.y() - self.start_point.y())
                self.drawing = False
                self.label_dialog.label_edit.clear()
                if self.label_dialog.exec_():
                    label = self.label_dialog.label_edit.text()
                    #未输入标签时删除这个矩形
                    if label == '':
                        self.p1.scene().removeItem(self.rect_item)
                    else:
                        self.rect_item.set_label(label)
                        self.rect_items.append(self.rect_item)
                    self.rect_item = None
                print(len(self.rect_items))

    def create_rightmenu(self):
        """create rightmenu on layout"""
        #菜单对象
        self.layout_menu = QMenu(self)

        self.actionA = QAction(u'保存标注 & xml',self)#创建菜单选项对象
        self.layout_menu.addAction(self.actionA)#把动作A选项对象添加到菜单self.win_menu上

        self.actionB = QAction(u'保存标注 & json',self)
        self.layout_menu.addAction(self.actionB)

        self.actionA.triggered.connect(self.save_xml) #将动作A触发时连接到槽函数 button
        self.actionB.triggered.connect(self.save_json)

        self.layout_menu.popup(QCursor.pos())#声明当鼠标在win控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
    
    def save_xml(self):
        """需要从局部标注转换到全局标注"""
        # 创建XML文档
        width, height = self.image.shape[1], self.image.shape[0]
        root = ET.Element("annotation")
        ET.SubElement(root, "folder").text = "VOC2007"
        ET.SubElement(root, "filename").text = "image.jpg"
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(width)
        ET.SubElement(size, "height").text = str(height)
        ET.SubElement(size, "depth").text = "3"
        for rect_item in self.rect_items:
            x, y, w, h = rect_item.rect().x(), rect_item.rect().y(), rect_item.rect().width(), rect_item.rect().height()
            object = ET.SubElement(root, "object")
            ET.SubElement(object, "name").text = rect_item.label
            bndbox = ET.SubElement(object, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(x)
            ET.SubElement(bndbox, "ymin").text = str(y)
            ET.SubElement(bndbox, "xmax").text = str(x + w)
            ET.SubElement(bndbox, "ymax").text = str(y + h)
        xml_str = ET.tostring(root, encoding="unicode")
        # 保存XML文档，保存位置待定
        with open("image.xml", "w") as f:
            f.write(xml_str)

    def save_json(self):
        """需要从局部标注转换到全局标注"""
        width, height = self.image.shape[1], self.image.shape[0]
        # 创建JSON文档
        json_dict = {
            "filename": "image.jpg",
            "size": {"width": width, "height": height, "depth": 3},
            "object": {"name": "rectangle", "bndbox": {"xmin": 10, "ymin": 10, "xmax": 100, "ymax": 100}}
        }
        json_str = json.dumps(json_dict)
        # 保存JSON文档，保存位置待定
        with open("image.json", "w") as f:
            f.write(json_str)
      
class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QGraphicsView.NoFrame)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.image_item = None
        self.rect_items = []
        self.drawing = False
        self.label_dialog = LabelDialog(self)

    def set_image(self, pixmap):
        self.image_item = self.scene.addPixmap(pixmap)
        self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.drawing:
                self.drawing = True
                self.start_point = event.pos()
                self.rect_item = RectangleItem(QRectF(self.start_point, QSizeF(0, 0)))
                self.rect_item.setPen(QPen(QColor(255, 0, 0), 2))
                self.scene.addItem(self.rect_item)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing:
            end_point = event.pos()
            rect = QRectF(self.start_point, end_point).normalized()
            self.rect_item.setRect(rect)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing:
                self.drawing = False
                self.label_dialog.label_edit.clear()
                if self.label_dialog.exec_():
                    label = self.label_dialog.label_edit.text()
                    self.rect_item.set_label(label)
                    self.rect_items.append(self.rect_item)
                    self.rect_item = None
        super().mouseReleaseEvent(event)




    

                
               

    