from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from ...common.hai_msb_widget import HMainSideBarWidget

class AIWidget(HMainSideBarWidget):
    """用于主侧栏的AI Widget"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._title = kwargs.pop('title', 'AI Tools')
        self._title_actions = kwargs.pop('title_actions', [])

    def load(self):
        pass