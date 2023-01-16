
from PySide2.QtWidgets import *


def get_aux_side_bar(parent=None):
    """返回一个AuxSideBar对象"""
    return AuxSideBar('AuxSideBar', parent=parent)

class AuxSideBar(QDockWidget):
    """
    This is the Auxillary Side Bar of HaiGF, ihnerited from QDockWidget. 
    """
    def __init__(self, title, parent=None):
        super(AuxSideBar, self).__init__(title, parent=parent)
        self.p = parent
        self.layout = self.layout()

        m = (0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)