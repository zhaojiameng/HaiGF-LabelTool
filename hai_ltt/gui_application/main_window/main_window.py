
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore
import damei as dm
from pathlib import Path

# from .ui_form import Ui_MainWindow
from hai_ltt.apis import __version__, __appname__
# from .actions.actions import AllActions
from hai_ltt.gui_framework import FrameworkMainWindow

logger = dm.get_logger('main_window')

class AppMainWindow(FrameworkMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
