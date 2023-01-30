
from PySide2.QtWidgets import *
from HaiGF import HPage

class PyEditorPage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.set_title(self.tr('Customer Page'))
        # self.set_icon(<QIcon>)

        self.setup_ui()

    def setup_ui(self):
        # setup customer ui here (QWidget).
        self.layout = QVBoxLayout(self)
        lb = QLabel('Hello World')
        self.layout.addWidget(lb)
        pass