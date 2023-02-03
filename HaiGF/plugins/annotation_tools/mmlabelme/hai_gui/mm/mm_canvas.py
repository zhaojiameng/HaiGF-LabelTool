"""
mm_canvas
多模态画布
"""
# from qtpy import QtCore
# from qtpy import QtWidgets
# from qtpy import QtGui

from PySide2 import QtCore, QtWidgets, QtGui
from hai_gui.widgets import Canvas as BaseCanvas


class MMCanvas(QtWidgets.QWidget):
    """多模态画布"""
    toggleModal = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        self.num_mm = kwargs.pop('num_mm', 2)  # 模态数目

        self.canvases = [VisibleCanvas, InfraRedCanvas]
        self.canvas = self.canvases[0]

    def swith_modal(self, idx):
        self.canvas = self.canvases[idx]



class VisibleCanvas(BaseCanvas):
    """可见光画布"""
    def __init__(self, *args, **kwargs):
        super(VisibleCanvas, self).__init__(*args, **kwargs)


class InfraRedCanvas(BaseCanvas):
    """红外画布"""
    def __init__(self, *args, **kwargs):
        super(InfraRedCanvas, self).__init__(*args, **kwargs)


class PointCloudCanvas(BaseCanvas):
    """点云画布"""
    def __init__(self, *args, **kwargs):
        super(PointCloudCanvas, self).__init__(*args, **kwargs)


class RadarCanvas(BaseCanvas):
    """雷达画布"""
    def __init__(self, *args, **kwargs):
        super(RadarCanvas, self).__init__(*args, **kwargs)
