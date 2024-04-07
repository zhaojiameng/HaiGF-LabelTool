from PySide2.QtWidgets import *
from PySide2.QtGui import *
class LabeledRectItem(QGraphicsItemGroup):
    def __init__(self, label, x, y, width, height, parent=None):
        super(LabeledRectItem, self).__init__(parent)

        # 创建矩形框
        self.rect = QGraphicsRectItem(x, y, width, height)
        #如果label是‘0’，则矩形框为红色，否则为绿色
        if label == '0':
            self.rect.setPen(QPen(Qt.red, 2))
        else:
            self.rect.setPen(QPen(Qt.green, 2))
            


