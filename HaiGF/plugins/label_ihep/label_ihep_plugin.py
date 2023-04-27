from pathlib import Path
from HaiGF.apis import HPlugin, HAction
from HaiGF.apis import newIcon
from PySide2 import QtCore
import damei as dm


here = Path(__file__).parent

class LabelIhepPlugin(HPlugin):
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
        
        #中央控件添加页面
        # self.page, self.page1 = self.create_page()
        # self.cw.add_page(self.page, self.action)
        # self.cw.add_page(self.page1, self.action)
        self.page2 = self.create_page2()
        self.page2.hide()
        

    def create_action(self):
        """返回一个action，用于在主窗口的菜单栏中显示"""
        action = HAction(
            text=self.tr('label ihep Q&A'),  # 文本
            parent=self.mw,  # 父对象，一般为HMainWindow
            slot=self.on_antrain_action_clicked, # 槽函数
            shortcut="Ctrl+Shift+I",  # 快捷键
            icon="ihep",  # 图标路径：gui_framework/icons，自动搜索.svg和.png
            tip=f'{self.tr("label ihep Q&A")} (Ctrl+Shift+L)',  # 提示
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
        from .widgets.msb_widget import LabelIhepMSBWidget
        msb_widget = LabelIhepMSBWidget(self.mw)
        return msb_widget

    def create_page(self):
        """返回一个页面，用于在中央控件中显示"""
        from .widgets.cw_page import MarkIhepPage
        page = MarkIhepPage(self.cw)
        from .widgets.cw_page_1 import MarkIhepPage1
        page1 = MarkIhepPage1(self.cw)
        return page, page1
    
    def create_page2(self):
        from .widgets.cw_page_2 import MarkIhepPage2
        page2 = MarkIhepPage2(self.cw)
        return page2
    
    def update_label(self):
        if not hasattr(self, 'page2'):
            pass
        else:
            self.page2.save()

    def show_data(self, record):
        self.page2.data = record
        if self.page2 not in self.cw.pages:
            self.page2.create_page()
            self.cw.add_page(self.page2, self.action) 
        else:
            self.page2.update_page()
        self.cw.set_focus(self.page2)

    def auto_upload(self, state):
        self.page2.auto_upload = state

    def set_annotate_user(self, user):
        self.page2.labeler = user

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            print('tab')
            self.page2.tab_press()
    

    

    

            

    

   
    