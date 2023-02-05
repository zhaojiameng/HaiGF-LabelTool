"""
The cw page
It's a canvas
"""
import os
import cv2
# import PIL
import numpy as np
import math

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt
from HaiGF import HPage, HGF
from HaiGF.utils import general

from ..mmlabelme import load_Canvas, Canvas
from ..mmlabelme import ZoomWidget

import damei as dm

logger = dm.get_logger('cw_page')

class CanvasPage(HPage):
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = 0, 1, 2

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('annotate'))
        self.set_icon(HGF.ICONS('anno'))
        self.setup_ui()

        self.image = None
        self.zoom_values = {}  # {filename: (zoom mode, zoom value)}
        self.filename = None
        self.scroll_values = {  # 滚动值
            Qt.Horizontal: {},
            Qt.Vertical: {},
        }  # key=filename, value=scroll_value
        self.zoomMode = self.FIT_WINDOW

        self.setStyleSheet(f"background-color: {HGF.COLORS.DarkBlack};")

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
        self.canvas.zoomRequest.connect(self.zoomRequest)
        # self.canvas.editShapeSignal.connect(self.editLabel)
        self.canvas.scrollRequest.connect(self.scrollRequest)
        # self.canvas.newShape.connect(self.newShape)  # 创建点形状时，会调用. 连接到函数，弹出并为标签编辑器提供焦点
        # self.canvas.shapeMoved.connect(self.setDirty)  # 改标题啥的
        # self.canvas.selectionChanged.connect(self.shapeSelectionChanged)  # 选择的形状变化
        # self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)  # 绘制多边形：创建矩形/多边形等的第一个点后会触发,参数为True，
        self.layout.addWidget(self.scrollArea)

        # self.scrollArea.setStyleSheet('background-color: (255, 0,, 0)')
        # self.canvas.setStyleSheet('background-color: (255, 0,, 0)')
        # self.layout.addWidget(self.canvas)

        self.zoomWidget = ZoomWidget()  # 输入和显示整数的组件
        # 包括缩小，放大，原始大小，保持上一帧尺寸
        zoom = QtWidgets.QWidgetAction(self)  # 应该是工具栏
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setEnabled(False)
        self.zoomWidget.valueChanged.connect(self.paintCanvas)
        self.setAcceptDrops(True)  # 可接收拖动

    def load_img(self, img_path):
        assert isinstance(img_path, str)
        # if isinstance(img, str):
        assert os.path.exists(img_path), f'img path not exists: {img_path}'
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = general.img2pixmap(img)
        self.image = img  # Qpixmap
        self.filename = img
        # self.canvas.setEnabled(False)

        self.canvas.loadPixmap(img)
        # self.paintCanvas(initial=True)
        
        # print(img.width(), img.height())
        # print(self.canvas.width(), self.canvas.height())
        # print(self.scrollArea.width(), self.scrollArea.height())
        # print(self.width(), self.height())
        # print(self.p.width(), self.p.height())
        # tabw = self.p.current_tab_widget()
        # print(tabw.width(), tabw.height())
        # self.canvas.setEnabled(True)
        self.adjustScale()

    def paintCanvas(self):
        assert self.image is not None, 'image is None'

        val = self.zoomWidget.value()
        # print('zoom value:', val)

        self.canvas.scale = 0.01 * self.zoomWidget.value()  # 缩放比例, 100*0.1=1
        self.canvas.adjustSize()
        self.canvas.update()
        # self.canvas.repaint()

    def adjustScale(self, initial=False):
        zoom_mode = self.FIT_WINDOW if initial else self.zoomMode
        # value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        if zoom_mode == self.FIT_WINDOW:
            value = self.scaleFitWindow()
        elif zoom_mode == self.FIT_WIDTH:
            value = self.scaleFitWidth()
        else:
            try:
                value = self.zoom_values[self.filename]
            except KeyError:
                value = self.scaleFitWindow()
        # print('adjust scale:', value)
        value = int(100 * value)
        self.zoomWidget.setValue(value)
        # self.zoom_values[self.filename] = (self.zoomMode, value)
    
    def centralWidget(self):
        return self.p

    def scaleFitWindow(self):
        """Figure out the size of the pixmap to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

    def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.centralWidget().width() - 2.0
        return w / self.canvas.pixmap.width()

    def zoomRequest(self, delta, pos):
        # logger.info(f'zoom request: {delta} {pos}')
        canvas_width_old = self.canvas.width()
        units = 1.1  # zoom in
        if delta < 0:  # zoom out
            units = 0.9
        self.addZoom(units)

        canvas_width_new = self.canvas.width()
        if canvas_width_old != canvas_width_new:
            canvas_scale_factor = canvas_width_new / canvas_width_old

            x_shift = round(pos.x() * canvas_scale_factor) - pos.x()
            y_shift = round(pos.y() * canvas_scale_factor) - pos.y()

            self.setScroll(
                Qt.Horizontal,
                self.scrollBars[Qt.Horizontal].value() + x_shift,
            )
            self.setScroll(
                Qt.Vertical,
                self.scrollBars[Qt.Vertical].value() + y_shift,
            )

    def addZoom(self, increment=1.1):
        zoom_value = self.zoomWidget.value() * increment
        if increment > 1:
            zoom_value = math.ceil(zoom_value)
        else:
            zoom_value = math.floor(zoom_value)
        self.setZoom(zoom_value)

    def setZoom(self, value):
        # self.actions.fitWidth.setChecked(False)
        # self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        # logger.info(f'setZoom: {value}')
        self.zoomWidget.setValue(value)
        self.zoom_values[self.filename] = (self.zoomMode, value)

    def scrollRequest(self, delta, orientation):
        # logger.info(f'scrollRequest: {delta}, {orientation}')
        units = -delta * 0.1  # natural scroll
        bar = self.scrollBars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)

    def setScroll(self, orientation, value):
        self.scrollBars[orientation].setValue(value)
        self.scroll_values[orientation][self.filename] = value
    
