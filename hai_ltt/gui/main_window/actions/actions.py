
import functools
from ... import utils

class AllActions(object):
    def __init__(self, parent=None):
        self.parent = parent
        self._init()

    def set_actions(self, **kwargs):
        """
        把所有的action都放到self.actions里面
        使用：
        >>> actions = AllActions()
        >>> actions.<action_name>
        """
        self.__dict__.update(kwargs)

    def set_groups(self, **kwargs):
        """
        把action编组
        使用：
        >>> actions = AllActions()
        >>> actions.<group_name>
        """
        # TODO: 用于编组action，方便后续操作
        pass

    def _init(self):
        mw = self.parent
        Action = functools.partial(utils.newAction, parent=mw)
        explorer_action = Action(
            text=mw.tr("Explorer"), 
            slot=None,
            shortcut="Ctrl+E", 
            icon="explorer",
            tip=f'{mw.tr("Explorer")} (Ctrl+E)',
            checkable=True,
            enabled=True,
            checked=False,  
            )
        anno_action = Action( 
            text=mw.tr("Label Tools"),
            shortcut="Ctrl+A", 
            icon="anno",
            checkable=True,
            tip=f'{mw.tr("Label Tools")} (Ctrl+A)',
            )
        ai_action = Action(
            text=None,
            shortcut="Ctrl+I",
            icon="ai",
            tip=f'{mw.tr("AI Tools")} (Ctrl+I)',
            )
        
        setting_action = Action(
            text=mw.tr("Settings"),
            shortcut="Ctrl+,",
            icon="setting",
            tip=f'{mw.tr("Settings")} (Ctrl+,)',
            )

        self.set_actions(
            explorer_action=explorer_action,
            anno_action=anno_action,
            ai_action=ai_action,
            setting_action=setting_action,
            )

        self.set_groups(
            core_func_bar=[
                explorer_action, 
                anno_action, 
                ai_action, 
                ],
        )

        



    

