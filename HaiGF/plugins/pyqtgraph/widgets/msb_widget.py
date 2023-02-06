
import os
from PySide2 import QtCore, QtGui, QtWidgets
import functools

from HaiGF.apis import HMainSideBarWidget, HAction

from .msb_ui import Ui_Form
from .python_highliter import PythonHighlighter

class PyqyGraphMSBWidget(HMainSideBarWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent

        self.set_title(self.tr('PyQtGraph'))
        self.set_title_actions([HAction(text='test', parent=self.p)])

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        
    

