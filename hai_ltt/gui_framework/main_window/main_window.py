# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore
import damei as dm
from pathlib import Path

from .ui_form import Ui_MainWindow
from hai_ltt.apis import __version__, __appname__
from .actions.actions import AllActions
from hai_ltt.apis import HGF

from ..widgets import ExplorerWidget

logger = dm.get_logger('framework_main_window')

class FrameworkMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = HGF.CONFIG
        
        self.actions = AllActions(parent=self)
        self.settings = QtCore.QSettings(__appname__, __appname__)
        
        self.mw_ui = Ui_MainWindow()
        self.mw_ui.setupUi(self)
        self.setWindowTitle(self.tr('HAI GUI Framework'))
        # self.mw_ui.retranslateUi(self)
        # self.setStyleSheet("QMainWindow{background-color: rgb(255, 255, 255);}")
        # self.setStyleSheet("QMainWindow{background-color: rgb(0, 255, 255);}")
        # 设置前景色和背景色
        self.setStyleSheet(
            "QMainWindow{"+f"background-color: {HGF.COLORS.WhiteSmoke}; \
                color: rgb(255, 255, 255); font-family: {HGF.FONT_FAMILY};\
                "+"}")

    def load_file_or_dir(self, file=None, dir=None):
        # assert file or dir, 'file or dir must be specified'
        if file:
            dir = Path(file).parent
        self.settings.setValue('lastDirPath', str(dir))
        # TODO：打开资源管理器，资源管理器添加到主侧栏中

        self.load_file_or_dir_func(file=file, dir=dir)  # 面向切面的编程，这里是切面，在子类中重写该函数能实现不同的功能

    def load_file_or_dir_func(self, file=None, dir=None):
        # print(self.main_side_bar)
        # dir = Path(dir).parent
        if file:
            pass
        elif dir:
            # widget = ExplorerWidget(parent=self, dir=dir)
            self.main_side_bar.load_widget_by_name(
                'ExplorerWidget',
                dir=dir,
            )
            self.main_side_bar.show()
        else:  # 没有指定文件或目录
            pass
        # logger.error('Please reimplement this method "load_file_or_dir_func" in subclass')
        # raise NotImplementedError(f'Please reimplement this method "load_file_or_dir_func" in subclass')

    def closeEvent(self, event):
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.saveState())
        # self.settings.setValue("splitter/state", self.central_widget.splitter.saveState())

    def mousePressEvent(self, ev):
        # logger.info(f'mousePressEvent: {ev}')
        logger.debug(f'mousePressEvent: {ev}')

    def show_warning(self, msg):
        self.mw_ui.statusbar.showMessage(msg, 5000)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    # translator = QTranslator()
    # translator.load("qtbase_ru.qm")
    # widget = MainWindow()
    widget = FrameworkMainWindow()
    widget.show()
    sys.exit(app.exec_())
