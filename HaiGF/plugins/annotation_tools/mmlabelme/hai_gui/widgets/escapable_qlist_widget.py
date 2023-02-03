# from qtpy.QtCore import Qt
# from qtpy import QtWidgets

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt


class EscapableQListWidget(QtWidgets.QListWidget):
    def keyPressEvent(self, event):
        super(EscapableQListWidget, self).keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.clearSelection()
