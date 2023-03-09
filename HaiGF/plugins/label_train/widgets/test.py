import sys


import os
from pathlib import Path
import cv2
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QRectF, QSizeF, QPoint
from PySide2.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QFont
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QLineEdit, QDialog, QDialogButtonBox, QVBoxLayout, QFileDialog, QInputDialog, QMessageBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import copy

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

    def set_image(self, filename):
        pixmap = QPixmap(filename)
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.set_image('image.jpg')
    viewer.show()
    sys.exit(app.exec_())
