
import os, sys
from pathlib import Path
import uuid
import weakref
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from ..PyFlow.UI.Canvas.UINodeBase import UINodeBase
from ..PyFlow.Core import NodeBase, GraphBase, PinBase
from ..PyFlow.Core.GraphManager import GraphManagerSingleton
from ..PyFlow.Core.Common import PinDirection
from ..PyFlow.Packages.PyFlowBase.Pins.ExecPin import ExecPin

here = Path(__file__).parent

def get_node(title, **kwargs):
    # title = 'yolov5'
    image = f'{here.parent}/resources/{title}.png'
    x = kwargs.pop('x', 0)
    y = kwargs.pop('y', 0)

    node = AlgorithmNode(title)
    node.setPosition(x, y)
    node.set_package_name('AI Package')
    node.set_lib('AI Lib')
    # node.set_graph(get_graph(**kwargs))  # 不应该添加
    node.uid = uuid.uuid4()  # 也会自动生成

    pin_test = PinBase('test pin', node, PinDirection.Input)
    pin_test2 = PinBase('test pin2', node, PinDirection.Output)
    pin_test3 = PinBase('test pin3', node, PinDirection.Input)
    pin_test4 = ExecPin('test pin4', node, PinDirection.Input)
    pin_test5 = ExecPin('test pin5', node, PinDirection.Output)
    node.set_pins([pin_test, pin_test2, pin_test3, pin_test4, pin_test5])


    # node.setDeprecated(True)
    # node.setExperimental()

    ui_node = UINodeBase(node)
     # 加载图像到一个控件
    lb = QLabel()
    # lb.setMaximumSize(200, 200)
    pix_img = QPixmap(image)
    w, h = ui_node.nodeNameWidget.size().width(), ui_node.nodeNameWidget.size().height()
    lb.setMaximumHeight(3*h)
    # lb.setPixmap(pix_img)
    lb.setScaledContents(True)  # 让图片自适应label大小
    # 防止锯齿
    lb.setPixmap(pix_img.scaled(lb.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
    # print(lb.size())
    # lb.setText('test widget')s
    ui_node.addWidget(lb)


    return ui_node


def get_graph(**kwargs):
    graph_manager = kwargs.get('graph_manager', GraphManagerSingleton().get())
    graph = GraphBase('AI Graph', graph_manager)
    return weakref.ref(graph)

class AlgorithmNode(NodeBase):
    def __init__(self, name, uid=None):
        super().__init__(name, uid)
        self.loadImage = Signal(str)
        # from ..PyFlow import INITIALIZE
        # INITIALIZE()

        # self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        # self.entity = self.createInputPin('path', 'StringPin')
        # self.outExec = self.createOutputPin(pinName='outExec', dataType='ExecPin', defaultValue=None)
    @staticmethod
    def category():
        return 'UI'

    @staticmethod
    def keywords():
        return ['image']

    @staticmethod
    def description():
        return 'AI Algorithm Node'

    def compute(self, *args, **kwargs):
        return super().compute(*args, **kwargs)

    