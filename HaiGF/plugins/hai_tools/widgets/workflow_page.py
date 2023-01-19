
import uuid
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PyFlow.Core.GraphManager import GraphManagerSingleton
from HaiGF import HPage
from HaiGF.apis import HGF

from .BlueprintCanvas import BlueprintCanvasWidget, BlueprintCanvas, getNodeInstance

from ..PyFlow.UI.Canvas.UINodeBase import UINodeBase
from ..PyFlow.Core import NodeBase

class WorkflowPage(HPage):
    def __init__(self, parent=None, *args, **kwargs):
        
        # super().__init__(self.graphManager.get(), parent, *args, **kwargs)
        super().__init__(parent)
        self.p = parent

        self.set_title(self.tr("workflow"))

        self.set_icon(HGF.ICONS('left-branch'))

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.graphManager = GraphManagerSingleton().get()
        self.canvas = BlueprintCanvas(self.graphManager, self.p)
        self.layout.addWidget(self.canvas)

        self.add_node()



    def add_node(self):

        # 
        # self.graphManager.get().addNode(node)
        jsonTemplate = NodeBase.jsonTemplate()
        jsonTemplate["type"] = "nodeClass"
        jsonTemplate["name"] = "nodename"
        jsonTemplate["package"] = "packageName"
        jsonTemplate["uuid"] = str(uuid.uuid4())
        jsonTemplate["x"] = 0
        jsonTemplate["y"] = 100
        # 添加一个节点
        # alg_node = NodeBase(name='test', uid=None)  # Nodebase对象
        alg_node = AlgorithmNode(name='test', uid=None)  # Nodebase对象
        alg_node.setDeprecated(True)
        # alg_node.setExperimental()
        # 添加input pin
        # input_pin = alg_node.createInputPin('input', 'StringPin')
        # alg_node.addInputPin('input', 'StringPin')


        alg_node = UINodeBase(alg_node)  # NodeBase转为QGraphicsWidget

        lb = QLabel('test')
        alg_node.addWidget(lb)

        self.canvas.addNode(alg_node, jsonTemplate, parentGraph=None)
        pass


class AlgorithmNode(NodeBase):
    def __init__(self, name, uid=None):
        super().__init__(name, uid)
        from ..PyFlow import INITIALIZE
        INITIALIZE()

        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('path', 'StringPin')
        self.outExec = self.createOutputPin(pinName='outExec', dataType='ExecPin', defaultValue=None)


    def compute(self, *args, **kwargs):
        return super().compute(*args, **kwargs)
