import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5 import QtWidgets
from PySide2 import QtGui, QtCore
from PySide2.QtGui import QPainterPath
from PySide2.QtCore import QPointF


class BezierROI(pg.ROI):
    def __init__(self, pos, size, **args):
        super().__init__(pos, size, **args)
        self.bezier_points = []

    def boundingRect(self):
        if len(self.bezier_points) > 0:
            x, y = zip(*self.bezier_points)
            return QtCore.QRectF(min(x), min(y), max(x)-min(x), max(y)-min(y))
        else:
            return super().boundingRect()

    def paint(self, p, opt, widget):
        if len(self.bezier_points) > 0:
            path = QtGui.QPainterPath()
            path.moveTo(*self.bezier_points[0])
            for i in range(1, len(self.bezier_points), 3):
                path.cubicTo(*self.bezier_points[i:i+3])
            p.setPen(self.currentPen)
            p.drawPath(path)
        else:
            super().paint(p, opt, widget)

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.bezier_points.append(self.mapFromParent(ev.pos()))
            ev.accept()
            self.sigRegionChanged.emit(self)

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.bezier_points[-1] = self.mapFromParent(ev.pos())
            ev.accept()
            self.sigRegionChanged.emit(self)

    def movePoint(self, point, newPos):
        index = self.getPointIndex(point)
        if index == len(self.bezier_points) - 1:
            self.bezier_points[-1] = newPos
        self.sigRegionChanged.emit(self)



class MyLineROI(pg.LineROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        #设置可移除
        self.removable = True

class MyRectROI(pg.RectROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        self.removable = True
        

class MyEllipseROI(pg.EllipseROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        self.removable = True
        

class MyCircleROI(pg.CircleROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(pg.mkPen('y'))
        self.removable = True
        

class MyPolyLineROI(pg.PolyLineROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.setPen(pg.mkPen('y'))
        self.removable = True
       
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



class BezierLineROI(pg.PolyLineROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.removable = True

    def shape(self):
        p = QPainterPath()
        if len(self.handles) == 0:
            return p
        p.moveTo(self.handles[0]['item'].pos())
        for i in range(len(self.handles)):
            sp = self.handles[i]['item'].pos()
            if i == len(self.handles) - 1:
                ep = self.handles[0]['item'].pos()
            else:
                ep = self.handles[i+1]['item'].pos()
            
            c1, c2 = self.getQuadFromLine(sp, ep)
            p.cubicTo(c1, c2, ep)
        return p
    
    def getQuadFromLine(self, pt1, pt2):
        """根据线段的两个端点计算控制点"""
        x1, y1 = pt1.x(), pt1.y()
        x2, y2 = pt2.x(), pt2.y()
        return QPointF((x1 + x2) / 2, y1), QPointF((x1 + x2) / 2, y2)
    
    def paint(self, p, *args):
        """重写paint方法，绘制贝塞尔曲线"""
        if self.getState()['size'] is None:
            return

        # 生成路径
        path = self.shape()

        # 绘制
        p.setPen(pg.mkPen('y'))
        p.drawPath(path)

    
if __name__ == '__main__':
    app = pg.mkQApp()
    win = pg.GraphicsLayoutWidget()
    win.show()

    view = win.addViewBox()
    view.setAspectLocked(True)

    bezierROI = BezierLineROI([[0, 0], [1, 1], [2, 0]])
    view.addItem(bezierROI)

    app.exec_()
