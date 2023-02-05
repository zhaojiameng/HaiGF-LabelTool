from HaiGF import HPlugin, HAction, HMainSideBarWidget, HPage



class PyqtGraphPlugin(HPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
        """
        Your can access to the following objects after inherit HPlugin:
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
        Please rewrite this function to install your plugin.
        For example:
            self.action = HAction("CUSTOMER ACTION", self.mw)
            self.cfb.add_action(self.action)
            self.widget = HMainSideBarWidget(self.mw)
            self.msb.add_widget(self.widget, self.action)

            self.page = HPage(self.mw)
            self.cw.add_page(self.page)
        """
        self.action= self.create_action()
        self.cfb.add_action(self.action)

        self.widget = HMainSideBarWidget(self.mw)
        self.msb.add_widget(self.widget, self.action)

        self.page = HPage(self.mw)
        self.cw.add_page(self.page)
        pass

    def customer_func(self):
        """
        You can define your own functions here, and access them externally by mw.plugins['<PLUGIN NAME>'].customer_func.
        For example (in other file):
            mw.plugins['CustomerPlugin'].customer_func()
        """
        print("Hello, World")

    def create_action(self):
        """返回一个action，用于在主窗口的菜单栏中显示"""
        short_cut = 'Ctrl+Shift+p'
        action = HAction(
            text=self.tr("Pygt Graph Examples"),  # 文本
            parent=self.mw,  # 父对象，一般为HMainWindow
            slot=None, # 槽函数
            shortcut=short_cut,  # 快捷键
            icon="histogram",  # 图标路径：gui_framework/icons，自动搜索.svg和.png
            tip=f'Pygt Graph Examples {short_cut}',  # 提示
            checkable=True,  # 是否可选中
            enabled=True,  # 是否可用
            checked=False,  # 是否选中
            )
        return action

