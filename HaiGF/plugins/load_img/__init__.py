
from HaiGF import HPlugin
from HaiGF.apis import newIcon

from .pages.canvas import Canvas



class LoadImagePlugin(HPlugin):
    """
    继承后，自动拥有如下对象：
    self.mw: HMainWindow  # 主窗口
    self.cfb: HMainWidow.core_func_bar  # 核心功能栏
    self.msb: HMainWindow.main_side_bar  # 主侧边栏
    self.cw: HMainWindow.central_widget  # 中央控件
    self.asb: HMainWindow.aux_side_bar  # 辅助侧边栏
    self.pw: HMainWindow.panel_widget  # 面板控件
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        

    def install(self):
        # self.cw.
        page = self.get_page()
        page.set_title('load image')
        page.set_icon(newIcon('ai'))
        self.cw.addPage(page)


    def get_page(self):
        return Canvas(self.cw, icon=None, title='Image')