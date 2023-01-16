"""
Main side bar of HAI Tools
"""

from PySide2.QtWidgets import *
from HaiGF.apis import HMainSideBarWidget



class HaiWidget(HMainSideBarWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        self.init_ui()

    
    def init_ui(self):
        label = QLabel("HAI Tools")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(label)
        self.setLayout(self.layout)

    

