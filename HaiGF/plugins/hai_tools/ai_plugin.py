

from HaiGF.apis import HPlugin, HAction
import damei as dm

from .utils import general


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
        # print('mw, ', self.mw)
        # print('cfb, ', self.cfb)
        self._haic = None
        self.hai_ip = '47.114.37.111'
        # self.hai_ip = '192.168.32.148'
        self.hai_port = 9999

    
    def install(self):
        """在此处实现模块的安装"""
        from .widgets.workflow_page import WorkflowPage
        from .widgets.main_side_bar import HaiWidget

        self.action = self.get_action()
        self.cfb.add_action(self.action)

        # 主侧栏
        self.msb_widget = HaiWidget(self.mw)
        self.msb_widget.set_title(self.tr('AI Tools'))
        self.msb_widget.set_title_actions([HAction(text='test', parent=self.mw, slot=self.test)])
        self.msb.add_widget(self.msb_widget, self.action)

        # 中央控件
        workflow_page = WorkflowPage(self.mw)
        self.cw.addPage(workflow_page)
        


    @property
    def haic(self):
        if self._haic is None:
            try:
                from HaiGF.apis import HaiClient  # 适配无hai_client库
                self._haic = HaiClient.HaiClient(self.hai_ip, self.hai_port)
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
        if self.haic is None or not self.haic.connected:
            self.mw.errorMessage(
                title=self.tr('Connect Error'), 
                message=self.tr('Failed to connect to HAI server %s:%s please check.' % (self.hai_ip, self.hai_port))
            )
            self.msb_widget.clean()
            return 
        moduels = self.haic.hub.list(ret_fmt='json')
        print(moduels)
        moduels = general.moduels_list2dict(moduels)
        print(moduels)

        modals = moduels['NAME']
        modal_imgs = None

        self.msb_widget.updateModals(mw=self.mw, modals=modals, modal_imgs=modal_imgs)
    