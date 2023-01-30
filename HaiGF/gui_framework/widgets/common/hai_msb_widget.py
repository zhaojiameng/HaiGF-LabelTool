"""
HAI Main Side Bar Widget    
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from HaiGF.apis import HGF

class HMainSideBarWidget(QWidget):
    """
    Inherited from `QWidget`, this is the base class of all widgets in the main side bar.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._title = kwargs.pop('title', 'Title')
        self._title_actions = kwargs.pop('title_actions', [])

        self.setStyleSheet(HGF.MAIN_SIDE_BAR_CSS)
    
    def load(self):
        pass

    @property
    def title(self):
        return self._title
    
    @property
    def title_actions(self):
        return self._title_actions

    def set_title(self, title: str):
        """
        Set title of the widget
        """
        self._title = title

    def set_title_actions(self, actions: list):
        """
        Set title actions of the widget
        """
        self._title_actions = actions