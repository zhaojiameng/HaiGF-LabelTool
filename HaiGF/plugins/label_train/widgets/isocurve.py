from pyqtgraph import IsocurveItem, QtCore, QtGui, QtWidgets
translate = QtCore.QCoreApplication.translate
class MyIsocurve(IsocurveItem):
    def __init__(self, data=None, level=0, pen='w', axisOrder=None, savetable=False):
        super().__init__(data, level, pen, axisOrder)
        self.savetable = savetable
        self.menu = None

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            ev.accept()
        
