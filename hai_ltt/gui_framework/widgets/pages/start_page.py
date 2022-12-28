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

from hai_ltt.apis import root_path, __appname__
from .ui_start_page import Ui_Widget

logger = dm.get_logger('start_page')

class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.mw = self.parent.mw
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

    @QtCore.Slot()
    def on_openFileButton_clicked(self):
        print('File button clicked')

    @QtCore.Slot()
    def on_openDirButton_clicked(self):

        # defaultOpenDirPath = root_path
        defaultOpenDirPath = self.mw.settings.value('lastDirPath', root_path)

        selected_dir = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self,
                self.tr("%s - Open Directory") % __appname__,
                defaultOpenDirPath,
                QtWidgets.QFileDialog.ShowDirsOnly
                | QtWidgets.QFileDialog.DontResolveSymlinks,
            )
        )
        self.mw.load_file_or_dir(dir=selected_dir)
