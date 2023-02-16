from pathlib import Path
from HaiGF.apis import HPlugin, HAction
from HaiGF.apis import newIcon
import damei as dm

from .widgets.msb_widget import AntrainMSBWidget

here = Path(__file__).parent

class AntrainPlugin(HPlugin):
    """
    继承后，自动拥有如下对象：
    self.mw: HMainWindow  # 主窗口
    self.cfb: HMainWidow.core_func_bar  # 核心功能栏
    self.msb: HMainWindow.main_side_bar  # 主侧边栏
    self.cw: HMainWindow.central_widget  # 中央控件
    self.asb: HMainWindow.aux_side_bar  # 辅助侧边栏
    self.pw: HMainWindow.panel_widget  # 面板控件
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    
    def install(self):
        """需要重写该函数，实现插件安装时的操作，例如：在核心功能栏添加action，在主侧栏添加控件等。"""
        
        #核心功能栏添加action
        self.action = self.create_action()
        self.cfb.add_action(self.action)

        # 主侧边栏添加控件
        self.msb_widget = self.create_msb_widget()
        self.msb.add_widget(self.msb_widget, self.action)
        

        # 中央控件添加页面
        # page = self.create_page()
        # page.set_title('annote&train')
        # page.set_icon(newIcon('label_train'))
        # self.cw.addPage(page)
        self.page = self.create_page()
        self.page.hide()

    def create_action(self):
        """返回一个action，用于在主窗口的菜单栏中显示"""
        action = HAction(
            text=self.tr('Annotation and Train Tools'),  # 文本
            parent=self.mw,  # 父对象，一般为HMainWindow
            slot=self.on_antrain_action_clicked, # 槽函数
            shortcut="Ctrl+Shift+L",  # 快捷键
            icon="label_train",  # 图标路径：gui_framework/icons，自动搜索.svg和.png
            tip=f'{self.tr("Annotation and Train Tools")} (Ctrl+Shift+L)',  # 提示
            checkable=True,  # 是否可选中
            enabled=True,  # 是否可用
            checked=False,  # 是否选中
            )
        return action
       
    def on_antrain_action_clicked(self):
        """槽函数"""
        pass

    def create_msb_widget(self):
        """返回一个主侧边栏控件，用于在主侧边栏中显示"""
        msb_widget = AntrainMSBWidget(self.mw)
        return msb_widget

    def create_page(self):
        """返回一个页面，用于在中央控件中显示"""
        from .widgets.cw_page import ImageAnalysisPage
        page = ImageAnalysisPage(self.mw)
        return page

    def open_image_file(self, file_path=None):
        file_path = file_path if file_path else f'{here}/resources/000000.jpg'
        self.page.create_img(file_path)

        if not self.page in self.cw.pages:
            self.cw.add_page(self.page)
        self.cw.set_focus(self.page)


