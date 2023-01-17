
from PySide2.QtWidgets import *
from PyFlow.Core.GraphManager import GraphManagerSingleton
from HaiGF import HPage
from HaiGF.apis import HGF

from .BlueprintCanvas import BlueprintCanvasWidget

class WorkflowPage(BlueprintCanvasWidget, HPage):
    def __init__(self, parent=None, *args, **kwargs):
        self.graphManager = GraphManagerSingleton()
        super().__init__(self.graphManager.get(), parent, *args, **kwargs)
        self.p = parent

        self.set_title(self.tr("workflow"))

        self.set_icon(HGF.ICONS('left-branch'))
        