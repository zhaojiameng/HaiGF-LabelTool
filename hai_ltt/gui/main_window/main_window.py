# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore
# from PySide2.QtCore import QTranslator
from .ui_form import Ui_MainWindow
from ...version import __version__, __appname__
from .actions.actions import AllActions

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.actions = AllActions(parent=self)
        self.settings = QtCore.QSettings(__appname__, __appname__)
        
        self.mw_ui = Ui_MainWindow()
        self.mw_ui.setupUi(self)
        # self.mw_ui.retranslateUi(self)
        # self.setStyleSheet("QMainWindow{background-color: rgb(255, 255, 255);}")

    def closeEvent(self, event):
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.saveState())
        
        self.settings.setValue("splitter/state", self.central_widget.splitter.saveState())

    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    # translator = QTranslator()
    # translator.load("qtbase_ru.qm")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
