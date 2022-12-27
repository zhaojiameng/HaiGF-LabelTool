
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QTranslator

from hai_ltt import MainWindow
from hai_ltt import __version__, __appname__


def main():
    translator = QTranslator()
    translator.load("translate/traslate.qm")

    app = QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.installTranslator(translator)
    
    mw = MainWindow()

    mw.show()
    mw.raise_()
    sys.exit(app.exec_())
