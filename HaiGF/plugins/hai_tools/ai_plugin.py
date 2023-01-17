

from HaiGF import HPlugin, HAction
from .main_side_bar.main_side_bar import HaiWidget
from .widgets.page import WorkflowPage

import damei as dm

_logger = dm.get_logger('ai_plugin')


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
        self._haic = None

    
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

    @property
    def ml(self):  # manage_list
        return self.manager_list  # 管理列表

    @property
    def haic(self):
        if self._haic is None:
            try:
                from hai_gui.hai import hai_client  # 适配无hai_client库
                self._hai = hai_client.HAIClient(self.hai_ip, self.hai_port)
                # print(self._haic.connect())
            except ImportError:
                _logger.warning('hai_client not found')
                self._haic = None
        return self._haic

    def test(self):
        print('test')


    def get_action(self):
        """返回一个action，用于在主窗口的菜单栏中显示"""
        ai_action = HAction(
            text=self.tr('AI Tools'),  # 文本
            parent=self.mw,  # 父对象，一般为HMainWindow
            slot=self.on_ai_action_clicked, # 槽函数
            shortcut="Ctrl+I",  # 快捷键
            icon="ai",  # 图标路径：gui_framework/icons，自动搜索.svg和.png
            tip=f'{self.tr("AI Tools")} (Ctrl+I)',  # 提示
            checkable=True,  # 是否可选中
            enabled=True,  # 是否可用
            checked=False,  # 是否选中
            )
        return ai_action

    def on_ai_action_clicked(self):
        """
        资源管理，即算法、脚本等。
        逻辑：点击算法，如果已连接，刷新算法，未连接时，弹出连接服务端界面，连接。
        """
        _logger.info('ai action clicked')
        if self.hai is None or not self.hai.connected:
            self.errorMessage(title='Connect Error', 
            message=f'Failed to connect to HAI server "{self.config["ip"]}:{self.config["port"]}", \
                    please check.')
            self.ml.clean()
            return 
        moduels = self.hai.hub.list(ret_fmt='json')
        print(moduels)
        moduels = self.moduels_list2dict(moduels)
        print(moduels)

        modals = moduels['NAME']
        modal_imgs = None

        self.ml.updateModals(mw=self, modals=modals, modal_imgs=modal_imgs)
    