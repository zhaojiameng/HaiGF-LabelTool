
from PySide2.QtWidgets import *
from PyFlow.Core.GraphManager import GraphManagerSingleton
from HaiGF import HPage

from .BlueprintCanvas import BlueprintCanvasWidget

class WorkflowPage(BlueprintCanvasWidget, HPage):
    def __init__(self, parent=None, *args, **kwargs):
        self.graphManager = GraphManagerSingleton()
        super().__init__(self.graphManager.get(), parent, *args, **kwargs)
        self.p = parent
        # self.init_ui()
    
    def init_ui(self):
        label = QLabel("Workflow Page")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(label)
        self.setLayout(self.layout)