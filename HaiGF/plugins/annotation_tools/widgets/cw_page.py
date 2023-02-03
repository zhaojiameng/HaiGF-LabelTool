"""
The cw page
It's a canvas
"""
import os
import cv2
# import PIL
import numpy as np

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt
from HaiGF import HPage, HGF
from HaiGF.utils import general

from ..mmlabelme import load_Canvas, Canvas
from ..mmlabelme import ZoomWidget

class CanvasPage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.set_title(self.tr('annotate'))
        self.set_icon(HGF.ICONS('anno'))
        self.setup_ui()

        self._image = None

    def setup_ui(self):
        # setup customer ui here (QWidget).
        # print('setup ui')
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QtWidgets.QScrollArea()  # 自动滚动区
        # self.canvas = load_Canvas(self=self)  # 画布
        self.canvas = Canvas()  # 画布

        self.scrollArea.setWidget(self.canvas)
        self.scrollArea.setWidgetResizable(True)
        self.scrollBars = {Qt.Vertical: self.scrollArea.verticalScrollBar(), Qt.Horizontal: self.scrollArea.horizontalScrollBar()}
        # self.canvas.zoomRequest.connect(self.zoomRequest)
        # self.canvas.editShapeSignal.connect(self.editLabel)
        # self.canvas.scrollRequest.connect(self.scrollRequest)
        # self.canvas.newShape.connect(self.newShape)  # 创建点形状时，会调用. 连接到函数，弹出并为标签编辑器提供焦点
        # self.canvas.shapeMoved.connect(self.setDirty)  # 改标题啥的
        # self.canvas.selectionChanged.connect(self.shapeSelectionChanged)  # 选择的形状变化
        # self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)  # 绘制多边形：创建矩形/多边形等的第一个点后会触发,参数为True，
        self.layout.addWidget(self.scrollArea)
        # self.layout.addWidget(self.canvas)

        self.zoomWidget = ZoomWidget()  # 输入和显示整数的组件
        # 包括缩小，放大，原始大小，保持上一帧尺寸
        zoom = QtWidgets.QWidgetAction(self)  # 应该是工具栏
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setEnabled(False)
        self.zoomWidget.valueChanged.connect(self.paintCanvas)
        self.setAcceptDrops(True)  # 可接收拖动

    def load_img(self, img):
        if isinstance(img, str):
            assert os.path.exists(img), f'img path not exists: {img}'
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = general.img2pixmap(img)
        self._image = img
        # self.canvas.setEnabled(False)
        print('load img')
        self.canvas.loadPixmap(img)
        self.paintCanvas()

        print(img.width(), img.height())
        print(self.canvas.width(), self.canvas.height())
        print(self.scrollArea.width(), self.scrollArea.height())
        print(self.width(), self.height())
        # self.canvas.setEnabled(True)

    def paintCanvas(self):
        assert self._image is not None, 'image is None'

        self.canvas.scale = 0.01 * self.zoomWidget.value()
        self.canvas.adjustSize()
        self.canvas.update()
        # self.canvas.repaint()

    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        value = int(100 * value)
        self.zoomWidget.setValue(value)
        self.zoom_values[self.filename] = (self.zoomMode, value)
