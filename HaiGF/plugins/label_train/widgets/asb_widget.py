from HaiGF import HaiClient, HAction
from HaiGF import AuxSideBar

class AntrainASBWidget(AuxSideBar):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        
        self.set_title(self.tr('asb widget'))

        title_actions = [
            HAction(text='test antrain', parent=self.p, slot=None),]
        self.set_title_actions(title_actions)