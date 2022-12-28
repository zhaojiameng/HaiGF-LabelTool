
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
    
    def load_file_or_dir_func(self, file=None, dir=None):
        assert file or dir, 'file or dir must be specified'
        if file:
            raise NotImplementedError('just dir is supported')
        else:
            self.load_dir(dir=dir)

    def load_dir(self, dir):
        # 加载所有的图片
        pass
