# This Python file uses the following encoding: utf-8
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from pathlib import Path
import damei as dm

from .ui_form import Ui_MainWindow
from HaiGF.apis import __version__, __appname__
from .actions.actions import AllActions
from HaiGF.apis import HGF
from HaiGF.apis import HPlugin
from ..utils.plugin_manager import PluginManager


# from ..widgets import ExplorerWidget

logger = dm.get_logger('hai_main_window')
here = Path(__file__).parent

class HMainWindow(QMainWindow):
    """
    This is the main window of the hai gui framework, inherited from QMainWindow.
    Alias: `mw`.
    """
    newFileExecuted = QtCore.Signal(bool)
    fileBeenLoaded = QtCore.Signal()

    def __init__(self, parent=None):
        """This is the init function of the main window."""
        super().__init__(parent)
        self.cfg = HGF.CONFIG
        
        self.actions = AllActions(parent=self)
        self.settings = QtCore.QSettings(__appname__, __appname__)

        
        self.mw_ui = Ui_MainWindow()
        self.mw_ui.setupUi(self)
        self.setWindowTitle(f'{__appname__} v{__version__}')
        self.setWindowIcon(HGF.ICONS('anno'))

        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        
        # 设置无标题栏
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowMinMaxButtonsHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置窗口圆角矩形
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        
        # self.mw_ui.retranslateUi(self)
        # self.setStyleSheet("QMainWindow{background-color: rgb(255, 255, 255);}")
        # self.setStyleSheet("QMainWindow{background-color: rgb(0, 255, 255);}")
        # 设置前景色和背景色
        self.setFont(HGF.MAIN_FONT)
        self.setStyleSheet(
            "QMainWindow{"+f"background-color: {HGF.COLORS.WhiteSmoke}; \
                color: rgb(255, 255, 255); font-family: {HGF.FONT_FAMILY};\
                "+"}")
            
        self.plugin_manager = PluginManager()
    
    @property
    def mw(self):
        return self
        
    @property
    def msb(self):
        return self.main_side_bar

    @property
    def cfb(self):
        return self.core_func_bar

    @property
    def cw(self):
        return self.central_widget

    @property
    def asb(self):
        return self.aux_side_bar

    @property
    def pw(self):
        return self.panel_widget

    @property
    def plugins(self):
        return self.plugin_manager.plugins


    def install_plugin(self, plugin: HPlugin):
        """
        Call the `install` method of the custom plugin to install it.\n
        :param plugin: A plugin instance in inherited from `HPlugin`.
        """
        # 判断model是否已经安装，如果已经安装则不再安装
        # assert isinstance(plugin, HPlugin), 'plugin must be a HPlugin instance'
        plugin = plugin(self)  # 实例化plugin
        plugin_name = plugin.__class__.__name__
        if plugin_name in self.plugin_manager.plugins:
            raise Exception(f'Plugin {plugin_name} has been installed')
        self.plugin_manager.register_plugin(plugin_name=plugin_name, plugin=plugin)
        plugin.install()
        # print(self.plugin_manager.plugin_names)

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

    def onRequestFillProperties(self, propertiesFillDelegate):
        logger.info(f'onRequestFillProperties: {propertiesFillDelegate}')

    def onRequestClearProperties(self):
        logger.info('onRequestClearProperties')

    def errorMessage(self, title, message):
        return QMessageBox.critical(
            self, title, "<p><b>%s</b></p>%s" % (title, message)
        )

    def init_plugins(self):
        print('init_plugins')
        # register plugins
        


if __name__ == "__main__":

    app = QApplication(sys.argv)
    # translator = QTranslator()
    # translator.load("qtbase_ru.qm")
    # widget = MainWindow()
    widget = HMainWindow()
    widget.show()
    sys.exit(app.exec_())
