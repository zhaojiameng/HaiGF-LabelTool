
from PySide2 import QtWidgets, QtCore, QtGui
import os, sys



class HPlugin(QtWidgets.QWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.mw = parent

    @property
    def cfb(self):
        return self.mw.core_func_bar
    
    @property
    def msb(self):
        return self.mw.main_side_bar
    
    @property
    def cw(self):
        return self.mw.central_widget 

    @property
    def asb(self):
        return self.mw.aux_side_bar

    @property
    def pw(self):
        return self.mw.panel_widget