

from HaiGF.apis import HPage, HGF

from .page_ui import Ui_Form


class PyqtGraphPage(HPage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent

        self.set_title(self.tr('pyqtgraph example'))
        self.set_icon(HGF.ICONS.get('curve-adjustment'))

        self.ui = Ui_Form()
        self.ui.setupUi(self)

    #     self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)

    # def on_pushButton_clicked(self):
    #     self.p.show_message('test')