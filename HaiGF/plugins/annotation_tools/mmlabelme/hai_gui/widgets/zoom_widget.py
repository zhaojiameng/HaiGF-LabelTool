# from qtpy import QtCore
# from qtpy import QtGui
# from qtpy import QtWidgets

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt


class ZoomWidget(QtWidgets.QSpinBox):
    def __init__(self, value=100):
        super(ZoomWidget, self).__init__()
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setRange(1, 1000)
        self.setSuffix(" %")
        self.setValue(value)
        self.setToolTip(self.tr("Zoom Level"))
        self.setStatusTip(self.toolTip())
        self.setAlignment(QtCore.Qt.AlignCenter)

    def minimumSizeHint(self):
        height = super(ZoomWidget, self).minimumSizeHint().height()
        fm = QtGui.QFontMetrics(self.font())
        width = fm.width(str(self.maximum()))
        return QtCore.QSize(width, height)
