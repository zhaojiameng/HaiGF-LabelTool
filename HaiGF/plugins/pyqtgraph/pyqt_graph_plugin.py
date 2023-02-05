

from HaiGF import HPlugin

class PyqtGraphPlugin(HPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
        """
        继承后，自动获得如下对象：
        self.mw:  HMainWindow  # 主窗口
        self.cfb: HMainWidow.core_func_bar  # 核心功能栏
        self.msb: HMainWindow.main_side_bar  # 主侧边栏
        self.cw:  HMainWindow.central_widget  # 中央控件
        self.asb: HMainWindow.aux_side_bar  # 辅助侧边栏
        self.pw:  HMainWindow.panel_widget  # 面板控件
        """
        pass
    
    def install(self):
        """
        需要重写该函数，实现插件安装时的操作，例如：在核心功能栏添加action，在主侧栏添加控件等。
        """
        pass

    def custom_func(self):
        """
        自定义函数，可通过插件类名访问，例如：mw.CustomerPlugin.custom_func()
        """
        pass