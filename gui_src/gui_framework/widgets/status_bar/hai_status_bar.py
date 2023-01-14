from PySide2.QtWidgets import *
from gui_src.apis import HGF


class HStatusBar(QStatusBar):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        # self.setObjectName("statusbar")
        self.showMessage("Ready")

        # widget = QWidget()
        # widget.setW
        label = QLabel("Ready")
        label2 = QLabel("Ready2")
        label.show()
        label.setStyleSheet("background-color: red")
        label2.setStyleSheet("background-color: blue")
        self.addWidget(label, stretch=1)
        self.addWidget(label2, 2)
        self.setStyleSheet(HGF.STATUS_BAR_CSS)   
        



