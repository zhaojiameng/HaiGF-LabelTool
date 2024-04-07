import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QWidget, QGraphicsPolygonItem, QStyle, QGraphicsRectItem
from PySide2.QtGui import QPainterPath, QKeyEvent
from PySide2.QtCore import QPointF, QLineF
#引入QGraphicsSceneMouseEvent，用于鼠标事件
from PySide2.QtWidgets import QGraphicsSceneMouseEvent
from pyqtgraph import functions as fn
from pyqtgraph import Point
from pyqtgraph import ROI
import numpy as np
from PySide2.QtCore import Qt

#类curveplogan,继承QGraphicsPolygonItem,实现插入点时同时插入两个控制点，点间的连线变为贝塞尔曲线
class CurvePlogan(QGraphicsPolygonItem):
    def __init__(self, parent=None, points=[], img_shape=[]):
        super().__init__(parent)
        self.points = []
        self.control_points = []
        self.img_shape = img_shape
        self.scale = 12.0
        self.point_size = 2.0
        self.original_pen = pg.mkPen('y')
        self.current_pen = pg.mkPen('g')
        self.setAcceptHoverEvents(True) # 允许鼠标悬停事件
        self.current_hover = False # 当前是否鼠标悬停在形状内部
        self.current_vertex = None # 当前选中的顶点
        self.current_control_point = None # 当前选中的控制点
        self.adjusted = False # 是否正在调整形状
        for point in  points:
            self.addPoint(point)

    def boundingRect(self):
        rect = super().boundingRect()
        rect.adjust(-self.point_size, -self.point_size, self.point_size, self.point_size)
        return rect

    def adjust_point(self, point):
        if point.x() < 0:
            point.setX(0)
        if point.y() < 0:
            point.setY(0)
        if point.x() > self.img_shape[1]:
            point.setX(self.img_shape[1])
        if point.y() > self.img_shape[0]:
            point.setY(self.img_shape[0])
        return point

    def addPoint(self, point):
        point = self.adjust_point(point)
        self.points.append(point)
        p1 = self.adjust_point(QPointF(point.x() - point.x() / self.scale, point.y() - point.y() / self.scale))
        p2 = self.adjust_point(QPointF(point.x() + point.x() / self.scale, point.y() + point.y() / self.scale))
        self.control_points.append(p1)
        self.control_points.append(p2)

    def adjustShape(self):
        self.adjusted = not self.adjusted
        self.update()
       
    def paintHandle(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        path = QPainterPath()
        for i in range(len(self.points)):
            path.addEllipse(self.points[i], self.point_size, self.point_size)
            path.addEllipse(self.control_points[2 * i], self.point_size, self.point_size)
            path.addEllipse(self.control_points[2 * i + 1], self.point_size, self.point_size)
        painter.drawPath(path)

        #绘制控制线,白色虚线
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.DashLine))
        pathL = QPainterPath()
        for i in range(len(self.points)):
            pathL.moveTo(self.points[i])
            pathL.lineTo(self.control_points[2 * i])
            pathL.moveTo(self.points[i])
            pathL.lineTo(self.control_points[2 * i + 1])
        painter.drawPath(pathL)

    def paint(self, painter, option, widget):
        #抗锯齿
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        #调整形状时，绘制控制点
        if self.adjusted:
            self.paintHandle(painter)
            
        painter.setPen(self.original_pen)
        path = self.shape()

        # 判断鼠标是否在形状内部，设置画笔颜色
        if self.current_hover:
            painter.setPen(self.current_pen)
        else:
            painter.setPen(self.original_pen)

        painter.drawPath(path)
        # #半透明红色虚线绘制boundingRect
        # painter.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DashLine))
        # painter.drawRect(self.boundingRect())

    def is_point_on_curve(self, point: QPointF, index: int, width=3.0):
        path = QPainterPath()
        path.moveTo(self.points[index])
        path.cubicTo(self.control_points[2 * index + 1], self.control_points[(2 * index + 2) % len(self.control_points)], self.points[(index + 1) % len(self.points)])
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(width)
        strokepath = stroker.createStroke(path) 
        if strokepath.contains(point):
            return True
        return False
        
    def shape(self):
        path = QPainterPath()
        if len(self.points) == 0:
            return path
        path.moveTo(self.points[0])
        for i in range(1, len(self.points)):
            path.cubicTo(self.control_points[2 * i - 1], self.control_points[2 * i], self.points[i])
        path.cubicTo(self.control_points[-1], self.control_points[0], self.points[0])
        return path
    
    #移除CurvePlogan
    def remove(self):
        self.scene().removeItem(self)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.pos()
        if event.button() == QtCore.Qt.RightButton:
            #判断鼠标是否在顶点上
            for i in range(len(self.points)):
                if QLineF(self.points[i], pos).length() < 10:
                    self.removePoint(i)
                    return
            super().mousePressEvent(event)
            return
        
        #判断鼠标是否在顶点或控制点上,或者在顶点和顶点之间的连线上，或者在形状内部
        #判断鼠标是否在顶点上
        for i in range(len(self.points)):
            if QLineF(self.points[i], pos).length() < 10:
                self.current_vertex = i
                return
        #判断鼠标是否在控制点上
        for i in range(len(self.control_points)):
            if QLineF(self.control_points[i], pos).length() < 10:
                self.current_control_point = i
                return
        # #判断鼠标是否在形状的边线上
        for i in range(len(self.points)):
            if self.is_point_on_curve(pos, i):
                self.insertPoint(i + 1, pos)
                return
            
        if self.shape().contains(pos):
            self.current_hover = True
            self.update()
            return      
        # super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        #鼠标在形状内部,移动形状
        current_pos = event.pos()
        if self.current_hover:
            old_pos = event.lastPos()
            self.moveBy(current_pos.x() - old_pos.x(), current_pos.y() - old_pos.y())
            self.update()
        elif self.current_vertex is not None:
            #计算顶点移动后的偏移量
            self.offset = current_pos - self.points[self.current_vertex]
            self.points[self.current_vertex] = current_pos
            self.updateControlPoints()
            self.updateBoundingRect()
        elif self.current_control_point is not None:
            #计算控制点移动后的偏移量
            self.offset = current_pos - self.control_points[self.current_control_point]
            self.control_points[self.current_control_point] = current_pos
            self.updateBoundingRect()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.current_vertex = None
        self.current_control_point = None
        self.current_hover = False
        super().mouseReleaseEvent(event)

    #插入顶点
    def insertPoint(self, index, pos):
        #计算插入点的控制点
        pos = self.adjust_point(pos)
        p1 = self.adjust_point(QPointF(pos.x() - pos.x() / self.scale, pos.y() - pos.y() / self.scale))
        p2 = self.adjust_point(QPointF(pos.x() + pos.x() / self.scale, pos.y() + pos.y() / self.scale))
        #插入顶点和控制点
        if index == len(self.points):
            self.points.append(pos)
            self.control_points.append(p1)
            self.control_points.append(p2)
        else:
            self.points.insert(index, pos)
            self.control_points.insert(2 * index, p1)
            self.control_points.insert(2 * index + 1, p2)
        self.updateBoundingRect()


    #删除顶点
    def removePoint(self, index):
        assert len(self.points) > 1
        self.points.pop(index)
        self.control_points.pop(2 * index)
        self.control_points.pop(2 * index)
        self.updateBoundingRect()

    def updateControlPoints(self): 
        self.control_points[2 * self.current_vertex] += self.offset
        self.control_points[2 * self.current_vertex + 1] += self.offset

    def updateBoundingRect(self):
        self.prepareGeometryChange()
        self.setPolygon(self.shape().toFillPolygon())
        self.update()

    

class MyLineROI(pg.LineROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        #设置可移除
        # self.removable = True

class MyRectROI(pg.RectROI):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        self.row = None
        # self.removable = True
        self.label = None

    def set_row(self, row):
        self.row = row

    def set_pen(self, label):
        if label == 1:
            self.setPen(pg.mkPen('r'))

    def set_label(self, label):
        self.label = label

        
class MyEllipseROI(pg.EllipseROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        # self.removable = True
        
class MyCircleROI(pg.CircleROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        # self.removable = True
        
class MyPolyLineROI(pg.PolyLineROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.setPen(pg.mkPen('y'))
        # self.removable = True
       
        self.sigHoverEvent.connect(self.hoverEvent)

    def hoverEvent(self, ev):
        if ev.isEnter():
            self.setPen(pg.mkPen('g', width=2))
        elif ev.isExit():
            self.setPen(pg.mkPen('y'))

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            if ev.double():
                pos = self.mapToParent(ev.pos())
                index = self.getNearestSegment(pos)
                self.removeSegment(index)
            else:
                pos = self.mapToParent(ev.pos())
                self.addFreeHandle(pos)


class MyGraphicsLayoutWidget(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.p1 = self.addPlot()
        self.img = pg.ImageItem(np.random.rand(100, 100))
        self.roi1 = pg.RectROI([20, 20], [30, 30])
        self.roi2 = pg.CircleROI([50, 50], 20)
        self.item3 = pg.PolyLineROI([[10, 10], [50, 10], [50, 50], [10, 50]], closed=True)
        self.p1.addItem(self.img)
        self.p1.addItem(self.roi1)
        self.p1.addItem(self.roi2)
        self.p1.addItem(self.item3)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            pos = ev.pos()
            item = self.itemAt(pos)
            if isinstance(item, pg.ImageItem):
                print("Clicked on ImageItem")
            elif isinstance(item, pg.RectROI):
                print("Clicked on RectROI")
            elif isinstance(item, pg.CircleROI):
                print("Clicked on CircleROI")
            elif isinstance(item, pg.PolyLineROI):
                print("Clicked on PolyLineROI")

if __name__ == '__main__':
    app = pg.mkQApp()
    win = MyGraphicsLayoutWidget()
    win.show()
    app.exec_()
