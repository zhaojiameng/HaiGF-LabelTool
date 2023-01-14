# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


from pathlib import Path
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import damei as dm

from gui_src.apis import root_path, __appname__
from .example import Ui_Form
from .ui_example_page  import Ui_Widget
from ...common.hai_page import HPage

logger = dm.get_logger('example_page')

class ExamplePage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        # self.mw = self.parent.mw
        self.ui = Ui_Form()
        self.ui.setupUi(self)




