
from HaiGF import HMainSideBarWidget, HAction
from ..widgets.msb_ui import Ui_Form


class AntrainMSBWidget(HMainSideBarWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent


        self.set_title(self.tr('Annotation and Train Tools'))

        title_actions = [
            HAction(text='test antrain', parent=self.p, slot=None),]
        self.set_title_actions(title_actions)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.runButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        mw = self.p

        plg = mw.plugins['AntrainPlugin']
        plg.canny_detect(self.ui.threshold1SpinBox.value(), self.ui.threshold2SpinBox.value())

        


