import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5 import QtWidgets
from PySide2.QtGui import QPainterPath
from PySide2.QtCore import QPointF


class MyROI(pg.ROI):
    sigRegionDoubleClick = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handleDoubleClick = self._handleDoubleClick

    def _handleDoubleClick(self, handle):
        self.sigRegionDoubleClick.emit(handle)


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


    


# class BezierLineROI(pg.PolyLineROI):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def getBezierControlPoints(self, p1, p2, p3):
#         """
#         计算贝塞尔曲线的控制点
#         :param p1: 第一个点
#         :param p2: 第二个点
#         :param p3: 第三个点
#         :return: 控制点列表
#         """
#         c1 = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
#         c2 = QPointF((p2.x() + p3.x()) / 2, (p2.y() + p3.y()) / 2)
#         return [c1, c2]

#     def generatePath(self):
#         """
#         生成曲线路径
#         :return: QPainterPath对象
#         """
#         path = QPainterPath()
#         pts = self.getState()['points']
#         if len(pts) < 3:
#             return path

#         # 生成曲线路径
#         path.moveTo(pts[0][0], pts[0][1])
#         for i in range(1, len(pts) - 1):
#             p1 = QPointF(pts[i - 1][0], pts[i - 1][1])
#             p2 = QPointF(pts[i][0], pts[i][1])
#             p3 = QPointF(pts[i + 1][0], pts[i + 1][1])
#             ctrl_pts = self.getBezierControlPoints(p1, p2, p3)
#             path.cubicTo(ctrl_pts[0], ctrl_pts[1], p3)

#         return path

#     def paint(self, p, *args):
#         """
#         重写paint方法，绘制贝塞尔曲线
#         """
#         if self.getState()['size'] is None:
#             return

#         # 生成路径
#         path = self.generatePath()

#         # 绘制
#         p.setPen(pg.mkPen('y'))
#         p.drawPath(path)

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

# from pyqtgraph import QtGui, QtCore
# import pyqtgraph as pg
# import numpy as np



# class BezierLineROI(pg.PolyLineROI):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.curvePoints = []
#         self.bezierHandles = []
#         self.generateBezierCurvePoints()

#     def mousePressEvent(self, ev):
#         super().mousePressEvent(ev)
#         self.generateBezierCurvePoints()

#     def movePoint(self, index, pos, finish=True):
#         super().movePoint(index, pos, finish)
#         self.generateBezierCurvePoints()

    

#     def addHandle(self, handlePos,  **kwargs):
#         super().addHandle(handlePos,  **kwargs)
#         self.generateBezierCurvePoints()


#     def removeHandle(self, handle):
#         super().removeHandle(handle)
#         self.generateBezierCurvePoints()

#     def generateBezierCurvePoints(self):
#         if len(self.handles) < 3:
#             return
#         self.curvePoints = []
#         self.bezierHandles = []
#         for i in range(len(self.handles) - 2):
#             p0 = self.handles[i]['item'].pos()
#             p1 = self.handles[i + 1]['item'].pos()
#             p2 = self.handles[i + 2]['item'].pos()
#             self.curvePoints.append(p1)
#             cp0, cp1 = self.getBezierControlPoints(p0, p1, p2)
#             self.bezierHandles.append(cp0)
#             self.bezierHandles.append(cp1)
#         self.curvePoints.append(self.handles[-1]['item'].pos())
#         self.setData(np.array(self.curvePoints))
#         self.curve.setBezierHandles(self.bezierHandles)

#     @staticmethod
#     def getBezierControlPoints(p0, p1, p2, t=0.5):
#         # https://stackoverflow.com/questions/57685392/how-to-draw-a-curve-between-two-points-in-pyqtgraph
#         d01 = np.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)
#         d12 = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
#         fa = t * d01 / (d01 + d12)
#         fb = t - fa
#         cp0 = [p1[0] + fa * (p0[0] - p2[0]), p1[1] + fa * (p0[1] - p2[1])]
#         cp1 = [p1[0] - fb * (p0[0] - p2[0]), p1[1] - fb * (p0[1] - p2[1])]
#         return cp0, cp1
    
if __name__ == '__main__':
    app = pg.mkQApp()
    win = pg.GraphicsLayoutWidget()
    win.show()

    view = win.addViewBox()
    view.setAspectLocked(True)

    bezierROI = BezierLineROI([[0, 0], [1, 1], [2, 0]])
    view.addItem(bezierROI)

    app.exec_()
