
import sys, os
from pathlib import Path
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QTranslator

from .gui_framework import FrameworkMainWindow
from .gui_application import AppMainWindow
from .apis import __version__, __appname__

here = Path(__file__).parent

def main(name='framework'):
    translator = QTranslator()
    translator.load(f"{here}/gui_framework/translate/translate_zh_CN.qm")

    app = QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.installTranslator(translator)
    
    if name == 'framework':
        mw = FrameworkMainWindow()
    else:
        mw = AppMainWindow()

    mw.show()
    mw.raise_()
    sys.exit(app.exec_())

