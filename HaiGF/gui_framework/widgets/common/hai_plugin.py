
from PySide2 import QtWidgets, QtCore, QtGui
import os, sys



class HPlugin(QtWidgets.QWidget):
    """
    这是HaiGF的插件基类，所有插件都应该继承自此类，其继承自QWidget。

    Example:
        >>> from HaiGF import HPlugin
        >>> class MyPlugin(HPlugin):
        >>>     def __init__(self, parent=None):
        >>>         super().__init__(parent)
        >>>    
        >>>     def install(self):
        >>>         # Please override this method by wirting your own code to install the plugin.
        >>>         pass

    继承后，自动链接到如下对象
        >>> self.mw:  HMainWindow  # 主窗口
        >>> self.cfb: HMainWidow.core_func_bar  # 核心功能栏
        >>> self.msb: HMainWindow.main_side_bar  # 主侧边栏
        >>> self.cw:  HMainWindow.central_widget  # 中央控件
        >>> self.asb: HMainWindow.aux_side_bar  # 辅助侧边栏
        >>> self.pw:  HMainWindow.panel_widget  # 面板控件
        >>> self.sb:  HMainWindow.status_bar  # 状态栏
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.mw = parent

    @property
    def cfb(self):
        return self.mw.core_func_bar
    
    @property
    def msb(self):
        return self.mw.main_side_bar
    
    @property
    def cw(self):
        return self.mw.central_widget 

    @property
    def asb(self):
        return self.mw.aux_side_bar

    @property
    def pw(self):
        return self.mw.panel_widget