import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QWidget, QGraphicsPolygonItem
from PySide2.QtGui import QPainterPath
from PySide2.QtCore import QPointF
from pyqtgraph.graphicsItems import GraphicsObject
from pyqtgraph import functions as fn
from pyqtgraph import Point
from pyqtgraph import ROI

#类curveplogan,继承QGraphicsPolygonItem,实现插入点时同时插入两个控制点，点间的连线变为贝塞尔曲线
class CurvePlogan(QGraphicsPolygonItem):
    def __init__(self, parent=None, points=[]):
        super().__init__(parent)
        self.points = []
        self.control_points = []
        self.setPen(QtGui.QPen(QtCore.Qt.red, 2))
        for point in  points:
            self.addPoint(point)
        


    def addPoint(self, point):
        self.points.append(point)
        p1 = QPointF(point.x() - point.x() / 2, point.y() - point.y() / 2)
        p2 = QPointF(point.x() + point.x() / 2, point.y() + point.y() / 2)
        self.control_points.append(p1)
        self.control_points.append(p2)
       

    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        #抗锯齿
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPath(self.shape())
        

    def shape(self):
        path = QPainterPath()
        if len(self.points) == 0:
            return path
        path.moveTo(self.points[0])
        for i in range(1, len(self.points)):
            path.cubicTo(self.control_points[2 * i - 1], self.control_points[2 * i], self.points[i])
        path.cubicTo(self.control_points[-1], self.control_points[0], self.points[0])
        return path

    
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
   def __init__(self, positions, closed=False, pos=None, **args):
        super().__init__(positions, closed, pos, **args)

   def addSegment(self, h1, h2, index=None):
        seg = _MyPolyLineSegment(handles=(h1, h2), pen=self.pen, hoverPen=self.hoverPen,
                                parent=self, movable=False)
        if index is None:
            self.segments.append(seg)
        else:
            self.segments.insert(index, seg)
        seg.sigClicked.connect(self.segmentClicked)
        seg.setAcceptedMouseButtons(QtCore.Qt.MouseButton.LeftButton)
        seg.setZValue(self.zValue()+1)
        for h in seg.handles:
            h['item'].setDeletable(True)
            h['item'].setAcceptedMouseButtons(h['item'].acceptedMouseButtons() | QtCore.Qt.MouseButton.LeftButton) 


    
class MyLineSegmentROI(ROI):
    r"""
    ROI subclass with two freely-moving handles defining a line.

    ============== =============================================================
    **Arguments**
    positions      (list of two length-2 sequences) The endpoints of the line 
                   segment. Note that, unlike the handle positions specified in 
                   other ROIs, these positions must be expressed in the normal
                   coordinate system of the ROI, rather than (0 to 1) relative
                   to the size of the ROI.
    \**args        All extra keyword arguments are passed to ROI()
    ============== =============================================================
    """
    
    def __init__(self, positions=(None, None), pos=None, handles=(None,None), **args):
        if pos is None:
            pos = [0,0]
            
        ROI.__init__(self, pos, [1,1], **args)
        if len(positions) > 2:
            raise Exception("LineSegmentROI must be defined by exactly 2 positions. For more points, use PolyLineROI.")
        
        for i, p in enumerate(positions):
            self.addFreeHandle(p, item=handles[i])
            
    @property
    def endpoints(self):
        # must not be cached because self.handles may change.
        return [h['item'] for h in self.handles]
        
    def listPoints(self):
        return [p['item'].pos() for p in self.handles]

    def getState(self):
        state = ROI.getState(self)
        state['points'] = [Point(h.pos()) for h in self.getHandles()]
        return state

    def saveState(self):
        state = ROI.saveState(self)
        state['points'] = [tuple(h.pos()) for h in self.getHandles()]
        return state

    def setState(self, state):
        ROI.setState(self, state)
        p1 = [state['points'][0][0]+state['pos'][0], state['points'][0][1]+state['pos'][1]]
        p2 = [state['points'][1][0]+state['pos'][0], state['points'][1][1]+state['pos'][1]]
        self.movePoint(self.getHandles()[0], p1, finish=False)
        self.movePoint(self.getHandles()[1], p2)
            
    def paint(self, p, *args):
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        p.setPen(self.currentPen)
        
        p.drawPath(self.shape())
        
    def boundingRect(self):
        return self.shape().boundingRect()
    
    def shape(self):
        p = QtGui.QPainterPath()

        #绘制形状
    
        
      
        return p
    
    def getArrayRegion(self, data, img, axes=(0,1), order=1, returnMappedCoords=False, **kwds):
        """
        Use the position of this ROI relative to an imageItem to pull a slice 
        from an array.
        
        Since this pulls 1D data from a 2D coordinate system, the return value 
        will have ndim = data.ndim-1
        
        See :meth:`~pyqtgraph.ROI.getArrayRegion` for a description of the
        arguments.
        """
        imgPts = [self.mapToItem(img, h.pos()) for h in self.endpoints]

        d = Point(imgPts[1] - imgPts[0])
        o = Point(imgPts[0])
        rgn = fn.affineSlice(data, shape=(int(d.length()),), vectors=[Point(d.norm())], origin=o, axes=axes, order=order, returnCoords=returnMappedCoords, **kwds)

        return rgn
        

class _MyPolyLineSegment(MyLineSegmentROI):
    # Used internally by PolyLineROI
    def __init__(self, *args, **kwds):
        self._parentHovering = False
        MyLineSegmentROI.__init__(self, *args, **kwds)
        
    def setParentHover(self, hover):
        # set independently of own hover state
        if self._parentHovering != hover:
            self._parentHovering = hover
            self._updateHoverColor()
        
    def _makePen(self):
        if self.mouseHovering or self._parentHovering:
            return self.hoverPen
        else:
            return self.pen
        
    def hoverEvent(self, ev):
        # accept drags even though we discard them to prevent competition with parent ROI
        # (unless parent ROI is not movable)
        if self.parentItem().translatable:
            ev.acceptDrags(QtCore.Qt.MouseButton.LeftButton)
        return MyLineSegmentROI.hoverEvent(self, ev)
