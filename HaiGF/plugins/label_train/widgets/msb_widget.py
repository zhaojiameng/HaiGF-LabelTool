
from HaiGF import HMainSideBarWidget, HAction


class AntrainMSBWidget(HMainSideBarWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent


        self.set_title(self.tr('Annotation and Train Tools'))

        title_actions = [
            HAction(text='test antrain', parent=self.p, slot=None),]
        self.set_title_actions(title_actions)

        


