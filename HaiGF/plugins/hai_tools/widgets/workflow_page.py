
import uuid
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PyFlow.Core.GraphManager import GraphManagerSingleton

from HaiGF import HPage
from HaiGF.apis import HGF

from .BlueprintCanvas import BlueprintCanvasWidget, BlueprintCanvas, getNodeInstance

from ..PyFlow.UI.Canvas.UINodeBase import UINodeBase
from ..PyFlow.Core import NodeBase\

class WorkflowPage(HPage):
    def __init__(self, parent=None, graph_manager=None, *args, **kwargs):
        
        # super().__init__(self.graphManager.get(), parent, *args, **kwargs)
        super().__init__(parent)
        self.p = parent

        self.set_title(self.tr("workflow"))

        self.set_icon(HGF.ICONS('left-branch'))

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.graphManager = graph_manager if graph_manager else GraphManagerSingleton().get()
        self.canvas = BlueprintCanvas(self.graphManager, self.p)
        self.layout.addWidget(self.canvas)


    def add_node(self, node: UINodeBase):
        """添加一个node到画布，"""
        # self.graphManager.get().addNode(node)
        template = node._rawNode.serialize()
        self.canvas.addNode(node, template, parentGraph=node._rawNode.graph)



