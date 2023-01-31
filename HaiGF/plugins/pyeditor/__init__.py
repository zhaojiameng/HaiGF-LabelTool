
from HaiGF import HPlugin

class PyEditorPlugin(HPlugin):
    def __init__(self, parent=None):
        super(PyEditorPlugin, self).__init__(parent)
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

    def open_file(self, file_path):
        """
        接口，打开一个Py文件，向中央控件添加新的页面
        安装本插件后再其他地方调用：mw.PyEditorPlugin.open_file()
        """
        print('open_file')
        # text = text if text else f'import os\n\nprint(os.getcwd())'

        pass