import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

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

class MyPolygonROI(pg.PolyLineROI):
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
                index = self.getNearestCorner(pos)
                self.removeHandle(index)
            else:
                pos = self.mapToParent(ev.pos())
                self.addFreeHandle(pos)

class MyWidget(pg.GraphicsLayoutWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roiComboBox = QtGui.QComboBox()
        self.roiComboBox.addItem("Line ROI")
        self.roiComboBox.addItem("Rect ROI")
        self.roiComboBox.addItem("Ellipse ROI")
        self.roiComboBox.addItem("Circle ROI")
        self.roiComboBox.addItem("PolyLine ROI")
        self.roiComboBox.addItem("Polygon ROI")
        self.roiComboBox.currentTextChanged.connect(self.updateRoiType)
        self.roiType = "Line ROI"
        self.plotItem = self.addPlot(row=0, col=0)
        self.plotItem.setMouseEnabled(x=False, y=False)
        self.plotItem.showAxis('left', False)
        self.plotItem.showAxis('bottom', False)
        self.roi = MyLineROI([[-50, 0], [50, 0]], width=5)
        self.plotItem.addItem(self.roi)
        self.updateRoiType()

    def updateRoiType(self):
        self.plotItem.removeItem(self.roi)
        if self.roiType == "Line ROI":
            self.roi = MyLineROI([[-50, 0], [50, 0]], width=5)
        elif self.roiType == "Rect ROI":
            self.roi = MyRectROI([-50, -50], [100, 100])
        elif self.roiType == "Ellipse ROI":
            self.roi = MyEllipseROI([-50, -25], [100, 50])
        elif self.roiType == "Circle ROI":
            self.roi = MyCircleROI([0, 0], 50)
        elif self.roiType == "PolyLine ROI":
            self.roi = MyPolyLineROI([[0, 0], [50, 0], [25, 25]])
        elif self.roiType == "Polygon ROI":
            self.roi = MyPolygonROI([[0, 0], [50, 0], [25, 25]])
        self.plotItem.addItem(self.roi)

