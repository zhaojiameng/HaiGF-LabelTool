"""
HAI Main Side Bar Widget    
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class HMainSideBarWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._title = kwargs.pop('title', 'Title')
        self._title_actions = kwargs.pop('title_actions', [])
    
    def load(self):
        pass

    @property
    def title(self):
        return self._title
    
    @property
    def title_actions(self):
        return self._title_actions