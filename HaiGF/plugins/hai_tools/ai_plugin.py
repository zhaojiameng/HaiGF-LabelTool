

from HaiGF import HPlugin, HAction
from .main_side_bar.main_side_bar import HaiWidget
from .widgets.page import WorkflowPage


class AIPlugin(HPlugin):
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
        print('mw, ', self.mw)
        print('cfb, ', self.cfb)

    
    def install(self):
        """在此处实现模块的安装"""
        self.action = self.get_action()
        self.cfb.add_action(self.action)

        # 主侧栏
        self.msb_widget = HaiWidget(self.mw)
        self.msb_widget.set_title(self.tr('AI Tools'))
        self.msb_widget.set_title_actions([HAction(text='test', parent=self.mw, slot=self.test)])

        self.msb.add_widget(self.msb_widget, self.action)

        # 中央控件
        page = WorkflowPage(self.mw)
        self.cw.addPage(page)


        pass

    def test(self):
        print('test')


    def get_action(self):
        """返回一个action，用于在主窗口的菜单栏中显示"""
        action = HAction(
            text=self.tr('AI Tools'),  # 文本
            parent=self.mw,  # 父对象，一般为HMainWindow
            slot=None, # 槽函数
            shortcut="Ctrl+I",  # 快捷键
            icon="ai",  # 图标路径：gui_framework/icons，自动搜索.svg和.png
            tip=f'{self.tr("AI Tools")} (Ctrl+I)',  # 提示
            checkable=True,  # 是否可选中
            enabled=True,  # 是否可用
            checked=False,  # 是否选中
            )
        return action
    