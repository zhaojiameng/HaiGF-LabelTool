from pathlib import Path

from HaiGF import HPlugin, HAction
from HaiGF.apis import HExamplesPage
from .widgets.msb_widget import AnnoMSBWidget

here = Path(__file__).parent

class AnnoPlugin(HPlugin):
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
        self.action = self.create_action()
        self.cfb.add_action(self.action)

        self.msb_widget = self.create_msb_widget()
        self.msb.add_widget(self.msb_widget, self.action)

        self.page = self.create_page()
        # self.page = HExamplesPage(self.cw, title='ex3')

        # self.cw.add_page(self.page)
        self.page.hide()

        # self.open_image_file()
        
        
    def create_action(self):
        """返回一个action，用于在主窗口的菜单栏中显示"""
        action = HAction(
            text=self.tr('Annotation Tools'),  # 文本
            parent=self.mw,  # 父对象，一般为HMainWindow
            slot=self.on_annotation_action_clicked, # 槽函数
            shortcut="Ctrl+Shift+A",  # 快捷键
            icon="anno",  # 图标路径：gui_framework/icons，自动搜索.svg和.png
            tip=f'{self.tr("Annotation Tools")} (Ctrl+Shift+A)',  # 提示
            checkable=True,  # 是否可选中
            enabled=True,  # 是否可用
            checked=False,  # 是否选中
            )
        return action

    def create_msb_widget(self):
        """返回一个主侧边栏控件，用于在主侧边栏中显示"""
        msb_widget = AnnoMSBWidget(self.mw)
        return msb_widget

    def create_page(self):
        from .widgets.cw_page import CanvasPage
        page = CanvasPage(self.cw)
        return page

    def custom_func(self):
        """
        自定义函数，可通过插件类名访问，例如：mw.CustomerPlugin.custom_func()
        """
        pass

    def on_annotation_action_clicked(self):
        """槽函数"""
        pass

    def open_image_file(self, file_path=None):
        file_path = file_path if file_path else f'{here}/resources/000000.jpg'
        # print(file_path)
        self.page.set_title(file_path)
        self.page.load_img(file_path)

        if not self.page in self.cw.tab_widgets[0].pages:
            self.cw.add_page(self.page)
            # self.cw.set_focus(self.page)
        self.cw.set_focus(self.page)

        
    