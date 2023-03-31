"""
The cw page 2.
It is a  mafnification page.
"""
import os
from pathlib import Path
import pyqtgraph as pg
import cv2
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QRectF, QSizeF, QPoint
from PySide2.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QFont, QCursor
from PySide2.QtWidgets import QGraphicsRectItem, QMenu, QAction, QLineEdit, QDialog, QDialogButtonBox, QVBoxLayout, QFileDialog
from pyqtgraph.Qt import QtGui
from HaiGF import HPage, HGF
import copy
import xml.etree.ElementTree as ET
import json
import damei as dm
import numpy as np

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
    
    # def mousePressEvent(self, event):
    #     super().mousePressEvent(event)
    #     if event.button() == Qt.LeftButton:
    #         self.setCursor(QCursor(Qt.ClosedHandCursor))
    #         self.start_point = event.pos()
    #         self.update()
    #     elif event.button() == Qt.RightButton:
    #         self.label_dialog = LabelDialog(self)
    #         self.label_dialog.label_edit.setText(self.label)
    #         if self.label_dialog.exec_():
    #             self.set_label(self.label_dialog.label_edit.text())
    #             self.update()
    
    # #拖动矩形框
    # def mouseMoveEvent(self, event):
    #     super().mouseMoveEvent(event)
    #     if event.buttons() == Qt.LeftButton:
    #         pos = event.pos()
    #         self.setPos(pos)
    #         self.update()

class ImageMagnificationPage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('magnifaication'))
        self.set_icon(HGF.ICONS('label_train'))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_rightmenu)

        self.img_manification = []
       
        self.rect_items = []
        self.rect_item = None
        self.drawing = False
        self.label_dialog = LabelDialog(self)
    
        self.image = None
        self.filePath = None
        self.folderPath = None
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
        self.img.mousePressEvent = self.mousePressEvent
        self.img.mouseMoveEvent = self.mouseMoveEvent
        self.img.mouseReleaseEvent = self.mouseReleaseEvent
        self.p1.addItem(self.img)
        self.setMouseTracking(True)
        self.win.show()

    def show_image(self, image, img_manification, img_path):
        if self.filePath is None:
            self.filePath = img_path
        elif self.filePath != img_path:
            self.save_xml()
            self.filePath = img_path
            self.rect_items = []

        self.p1.clear()
        self.p1.addItem(self.img)
        self.image = image
        self.img_manification = img_manification
        self.img.setImage(image)
        self.img.setRect(QRectF(0, 0, image.shape[1], image.shape[0]))
       
    def get_Rect(self, p1, p2):
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        if x1 < x2:
            x = x1
            width = x2 - x1
        else:
            x = x2
            width = x1 - x2
        if y1 < y2:
            y = y1
            height = y2 - y1
        else:
            y = y2
            height = y1 - y2
        return QRectF(x, y, width, height)
    
    def fix_coordinate(self, pos):
        x, y = pos.x(), pos.y()
        if x < 0:
            x = 0
        if x > self.image.shape[1]:
            x = self.image.shape[1]
        if y < 0:
            y = 0
        if y > self.image.shape[0]:
            y = self.image.shape[0]
        return QPoint(x, y)
       
    #event.pos 是什么？
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if  self.drawing:
                self.start_point = self.img.mapToParent(self.fix_coordinate(event.pos()))
                self.rect_item = RectangleItem(self.get_Rect(self.start_point, self.start_point))
                self.rect_item.setPen(QPen(QColor(0, 255, 0), 0.1))
                self.p1.addItem(self.rect_item)
                self.rect_item.setZValue(10)
            # else:
            #     #判断是否在矩形内,如果在矩形内则可以拖动矩形
            #     for rect_item in self.rect_items:
            #         if rect_item.rect().contains(event.pos()):
            #             self.rect_item = rect_item
            #             return
                
    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = self.img.mapToParent(self.fix_coordinate(event.pos()))
            self.rect_item.setRect(self.get_Rect(self.start_point, self.end_point))
        # else:
        #     #拖动矩形
        #     if self.rect_item is not None:
        #         self.rect_item.setRect(self.rect_item.rect().translated(event.pos() - self.rect_item.rect().center()))

                  
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing:
                self.end_point = self.img.mapToParent(self.fix_coordinate(event.pos()))
                self.rect_item.setRect(self.get_Rect(self.start_point, self.end_point))
                if self.label_dialog.exec_():
                    label = self.label_dialog.label_edit.text()
                    #未输入标签时删除这个矩形
                    if label != '':
                        x, y, w, h = self.rect_item.rect().x(), self.rect_item.rect().y(), self.rect_item.rect().width(), self.rect_item.rect().height()
                        real_rect = RectangleItem(QRectF(x + self.img_manification[2], y + self.img_manification[3], w, h))
                        real_rect.set_label(label)
                        self.rect_items.append(real_rect)
                    else:
                        self.p1.removeItem(self.rect_item)
                else:
                    self.p1.removeItem(self.rect_item)
                self.rect_item = None
        # else:
        #     #停止拖动矩形
        #     self.rect_item = None

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
        # if len(self.rect_items) == 0:
        #     return
        
        #如果folderPath为空，说明是第一次保存，需要弹出对话框选择保存路径,
        if self.folderPath is None:
            self.folderPath = QFileDialog.getExistingDirectory(self, "文件保存", "/")

        #filepath为folderPath和filename的拼接,后缀名为xml
        filepath = os.path.join(self.folderPath, os.path.splitext(os.path.basename(self.filePath))[0] + '.xml')
        if filepath: # check if the user selected a file
            path, filename = os.path.split(filepath) # split the file path and file name
        else:
            return
        # 创建XML文档
        width, height = self.img_manification[0], self.img_manification[1]
        root = ET.Element("annotation")
        ET.SubElement(root, "folder").text = str(path)
        ET.SubElement(root, "filename").text = str(filename)
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
            ET.SubElement(bndbox, "ymin").text = str(y - h)
            ET.SubElement(bndbox, "xmax").text = str(x + w)
            ET.SubElement(bndbox, "ymax").text = str(y)
        xml_str = ET.tostring(root, encoding="unicode")
        # 保存XML文档，保存位置待定
        with open(filepath, "w") as f:
            print(filepath)
            f.write(xml_str)

    def save_json(self):
        """需要从局部标注转换到全局标注"""
        filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "/" ,'xml(*.xml)')
        if filepath: # check if the user selected a file
            path, filename = os.path.split(filepath) # split the file path and file name
        else:
            return
        width, height = self.img_manification[0], self.img_manification[1]
        # 创建JSON文档
        json_dict = {
            "folder": path,
            "filename": filename,
            "size": {"width": width, "height": height, "depth": 3},
            "object": []
        }
        for rect_item in self.rect_items:
            x, y, w, h = rect_item.rect().x(), rect_item.rect().y(), rect_item.rect().width(), rect_item.rect().height()
            object = {
                "name": rect_item.label,
                "bndbox": {"xmin": x, "ymin": y - h, "xmax": x + w, "ymax": y}
            }
            json_dict["object"].append(object)
        json_str = json.dumps(json_dict)
        # 保存JSON文档，保存位置待定
        with open(filepath, "w") as f:
            f.write(json_str)
      
    def chang_mode(self):
        self.drawing = not self.drawing
        #光标变为十字形
        if self.drawing:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def keyPressEvent(self, event):
        """press key E to draw rectangle"""
        if event.key() == Qt.Key_D:
            self.chang_mode()




    

                
               

    