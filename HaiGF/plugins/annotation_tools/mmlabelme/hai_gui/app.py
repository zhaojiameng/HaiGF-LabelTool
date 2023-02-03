# -*- coding: utf-8 -*-

import functools
import math
import os
import os.path as osp
import re
from tkinter import N
import webbrowser
from pathlib import Path

import imgviz
# from qtpy import QtCore
# from qtpy.QtCore import Qt
# from qtpy import QtGui
# from qtpy import QtWidgets
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt

from hai_gui import __appname__
from hai_gui import PY2

from . import utils
from hai_gui.config import get_config
# from mmlabelme.label_file import LabelFile
# from mmlabelme.label_file import LabelFileError
from hai_gui.logger import logger
from hai_gui.shape import Shape
from hai_gui.widgets import BrightnessContrastDialog
from hai_gui.widgets import Canvas, load_Canvas
from hai_gui.widgets import FileDialogPreview
# from mmlabelme.widgets import LabelDialog
from hai_gui.widgets import LabelListWidget
from hai_gui.widgets import LabelListWidgetItem
from hai_gui.widgets import ToolBar
from hai_gui.widgets import UniqueLabelQListWidget
from hai_gui.widgets import ZoomWidget

from hai_gui import mm
from hai_gui.license import license_dialog
from hai_gui.mm import mm_quadrant_decide, mm_modal_update
from hai_gui.mm_label_file import MMLabelFile as LabelFile
from hai_gui.mm_label_file import MMLabelFileError as LabelFileError
from hai_gui import ai
from hai_gui.translate import build_language_config

import cv2

# hai
from .utils import hai_ex
from .utils.hai_ex.app_ex import AppEx

# FIXME
# - [medium] Set max zoom value to something big enough for FitWidth/Window

# TODO(unknown):
# - Zoom is too "steppy".f


LABEL_COLORMAP = imgviz.label_colormap()


class MainWindow(QtWidgets.QMainWindow, AppEx):  # double inheritance
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = 0, 1, 2

    def __init__(
            self,
            config=None,
            filename=None,
            output=None,
            output_file=None,
            output_dir=None,
    ):
        
        self.modal_size_real = None
        if output is not None:
            logger.warning("argument output is deprecated, use output_file instead")
            if output_file is None:
                output_file = output
        self.config = config
        self.first_init(config=config)
        lngg = self.lngg

        super(MainWindow, self).__init__()
        self.setWindowTitle(self.lngg.__appname__)
        self.dirty = False  # Whether we need to save or not.
        self._noSelectionSlot = False
        self._copied_shapes = None
        self.modals_size=[]
        self.lastOpenDir = None

        # 0. Main widgets and related state.
        self.labelDialog = mm.load_LabelDialog(self=self)
        self.licenseDialog = license_dialog.load_LicenseDialog(self=self)

        # 1. Flags坞, 包含列表widget
        self.flag_dock = self.flag_widget = None
        self.flag_dock = QtWidgets.QDockWidget(self.tr(lngg.dock_flags), self)
        self.flag_dock.setObjectName("Flags")
        self.flag_widget = QtWidgets.QListWidget()
        self.loadFlags({k: False for k in config["flags"]}) if config["flags"] else None
        self.flag_dock.setWidget(self.flag_widget)
        self.flag_widget.itemChanged.connect(self.setDirty)

        # 2. Polygon Labels坞，
        self.shape_dock = QtWidgets.QDockWidget(self.tr(lngg.dock_polygon_labels), self)
        self.labelList = LabelListWidget()  # 继承了QtWidgets.QListView
        self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)  # 列表元素被选中的槽
        self.labelList.itemDoubleClicked.connect(self.editLabel)  # 列表元素被双击的槽
        self.labelList.itemChanged.connect(self.labelItemChanged)  # 列表元素发生变化槽
        self.labelList.itemDropped.connect(self.labelOrderChanged)  # 列表元素被删除的槽
        self.shape_dock.setObjectName("Labels")
        self.shape_dock.setWidget(self.labelList)

        # 3.Label List坞, 包含uniqLabelList
        self.label_dock = QtWidgets.QDockWidget(self.tr(lngg.dock_label_list), self)
        self.uniqLabelList = UniqueLabelQListWidget()
        self.uniqLabelList.setToolTip(self.tr("Select label to start annotating for it. Press 'Esc' to deselect."))  # 这里就是设置右侧LabelList控件鼠标在空白区域时的图示字符串
        self.set_labels(self=self) if self._config["labels"] else None
        self.label_dock.setObjectName(lngg.dock_label_list)
        self.label_dock.setWidget(self.uniqLabelList)

        # 4.File List坞
        self.file_dock = QtWidgets.QDockWidget(self.tr(lngg.dock_file_list), self)
        self.fileSearch = QtWidgets.QLineEdit()  # File List里的输入文本框控件
        self.fileSearch.setPlaceholderText(self.tr(lngg.search_filename))
        self.fileSearch.textChanged.connect(self.fileSearchChanged)
        self.fileListWidget = QtWidgets.QListWidget()
        self.fileListWidget.itemSelectionChanged.connect(self.fileSelectionChanged)
        fileListLayout = QtWidgets.QVBoxLayout()
        fileListLayout.setContentsMargins(0, 0, 0, 0)
        fileListLayout.setSpacing(0)
        fileListLayout.addWidget(self.fileSearch)
        fileListLayout.addWidget(self.fileListWidget)
        self.file_dock.setObjectName(u"Files")
        fileListWidget = QtWidgets.QWidget()
        fileListWidget.setLayout(fileListLayout)
        self.file_dock.setWidget(fileListWidget)

        # 5.MM List坞
        self.mm_dock = mm.load_MMDock(self, self._config['mm'], dock_name=lngg.dock_mm_list)
        self.mmList = mm.MMListWidget(parent=self)
        self.mm_dock.setObjectName('mm')
        self.mm_dock.setWidget(self.mmList)
        self.mmList.iconlist.itemDoubleClicked.connect(self.slot_mm_item_double_cliked)
        self.mmList.itemCheckStateChanged.connect(self.slot_mm_item_check_state_changed)
        self.mmList.iconlist.itemChanged.connect(self.slot_mm_item_check_state_changed)

        # 6. hai manager坞
        self.manager_dock = QtWidgets.QDockWidget(self.tr(lngg.manager_dock), self)
        self.manager_list = mm.MMListWidget(parent=self)
        self.set_manager_dock()


        # 6. zoomeWidget
        self.zoomWidget = ZoomWidget()  # 输入和显示整数的组件
        # 包括缩小，放大，原始大小，保持上一帧尺寸
        zoom = QtWidgets.QWidgetAction(self)  # 应该是工具栏
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setEnabled(False)
        self.zoomWidget.valueChanged.connect(self.paintCanvas)
        self.setAcceptDrops(True)  # 可接收拖动
        
        # 7. scrollArea: Canvas, scrollBars, 
        self.scrollArea = QtWidgets.QScrollArea()  # 自动滚动区
        self.canvas = load_Canvas(self=self)  # 画布
        self.scrollArea.setWidget(self.canvas)
        self.scrollArea.setWidgetResizable(True)
        self.scrollBars = {Qt.Vertical: self.scrollArea.verticalScrollBar(), Qt.Horizontal: self.scrollArea.horizontalScrollBar()}
        self.canvas.zoomRequest.connect(self.zoomRequest)
        self.canvas.editShapeSignal.connect(self.editLabel)
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.newShape.connect(self.newShape)  # 创建点形状时，会调用. 连接到函数，弹出并为标签编辑器提供焦点
        self.canvas.shapeMoved.connect(self.setDirty)  # 改标题啥的
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)  # 选择的形状变化
        self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)  # 绘制多边形：创建矩形/多边形等的第一个点后会触发,参数为True，

        self.setCentralWidget(self.scrollArea)  # 中心窗口组件
        self.set_dock_features(docks=["flag_dock", "label_dock", "shape_dock", "file_dock", "mm_dock"])  # 设置窗口特性，可以关闭，可移动，停靠窗口可与主窗口分离等
        self.addDockWidget(Qt.RightDockWidgetArea, self.flag_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.label_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.shape_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.file_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.mm_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.manager_dock)


        self.actions = hai_ex.create_actions(self, zoom)  # 创建动作

        # Lavel list context menu.
        labelMenu = QtWidgets.QMenu()  # 标签菜单
        utils.addActions(labelMenu, (self.actions.edit, self.actions.delete))  # 给控件添加action，None是分割线，还可以添加菜单或动作
        self.labelList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.labelList.customContextMenuRequested.connect(
            self.popLabelListMenu)

        # 8. 菜单栏
        self.menus = self.set_menu(utils=utils, labelMenu=labelMenu)  # 设置菜单栏
        self.menus.file.aboutToShow.connect(self.updateFileMenu)
        self.set_canvas_context_menu(utils=utils)  # 设置画布上的右键菜单

        self.set_tool_bars()  # 设置工具栏
        # self.addToolBar(Qt.RightToolBarArea, self.ai_tools)

        self.statusBar().showMessage(str(self.tr("%s started.")) % self.lngg.__appname__)
        self.statusBar().show()

        if output_file is not None and self._config["auto_save"]:
            logger.warn(
                "If `auto_save` argument is True, `output_file` argument "
                "is ignored and output filename is automatically "
                "set as IMAGE_BASENAME.json."
            )
        self.output_file = output_file
        self.output_dir = output_dir

        # 应用状态Application state.
        self.image = QtGui.QImage()  # 图像
        self.imagePath = None  # 图像路径
        self.recentFiles = []  # 最近文件
        self.maxRecent = 7  # 最大存储最近文件数
        self.otherData = None
        self.zoom_level = 100  # 缩放级别
        self.fit_window = False  # 是否适应窗口
        self.zoom_values = {}  # key=filename, value=(zoom_mode, zoom_value)， 缩放值
        self.brightnessContrast_values = {}  # 亮度对比度
        self.scroll_values = {  # 滚动值
            Qt.Horizontal: {},
            Qt.Vertical: {},
        }  # key=filename, value=scroll_value

        if filename is not None and osp.isdir(filename):  # 初始导入图像
            self.importDirImages(filename, load=False)  # load为False只加载图像
        else:
            self.filename = filename

        if config["file_search"]:
            self.fileSearch.setText(config["file_search"])
            self.fileSearchChanged()

        # XXX: Could be completely declarative.
        # Restore application settings.
        self.settings = QtCore.QSettings(__appname__, __appname__) 
        self.recentFiles = self.settings.value("recentFiles", []) or []
        size = self.settings.value("window/size", QtCore.QSize(2000, 1000))  # 读取设置
        position = self.settings.value("window/position", QtCore.QPoint(0, 0))
        state = self.settings.value("window/state", QtCore.QByteArray())
        # PyQt4 cannot handle QVariant
        if isinstance(self.recentFiles, QtCore.QVariant):
            self.recentFiles = self.recentFiles.toList()
        if isinstance(size, QtCore.QVariant):
            size = size.toSize()
        if isinstance(position, QtCore.QVariant):
            position = position.toPoint()
        if isinstance(state, QtCore.QVariant):
            state = state.toByteArray()
        self.resize(size)
        self.move(position)
        # or simply:
        # self.restoreGeometry(settings['window/geometry']
        self.restoreState(state)

        # Populate the File menu dynamically.
        self.updateFileMenu()
        # Since loading the file may take some time,
        # make sure it runs in the background.
        # 加载文件需要时间，为了那啥更快显示出界面，把加载放在后台

        # 延迟启动
        self.queueEvent(self.check_license)
        if self.filename is not None:
            self.queueEvent(functools.partial(self.loadFile, self.filename), delay=200)
        if self._config['ai']['init_while_load']:
            self.queueEvent(self.ai.check_and_init, delay=700)  # 延迟启动ai

        # Callbacks:
        
        self.populateModeActions(utils=utils)  # 填充模式动作

        self.modals_new = None

        # 开启和关闭ai功能
        if self.ai_enabled:
            self.actions.run_ai.setEnabled(True)
            self.actions.stop_ai.setEnabled(False)
            self.actions.configure_ai.setEnabled(True)
            # self.actions.auto_ai.setChecked(True)
        else:      
            self.actions.run_ai.setEnabled(False)
            self.actions.stop_ai.setEnabled(False)
            self.actions.configure_ai.setEnabled(False)
            self.actions.auto_ai.setChecked(False)
            self.actions.auto_ai.setEnabled(False)

        # self.firstStart = True
        # if self.firstStart:
        #    QWhatsThis.enterWhatsThisMode()
        # self.set_style()
        

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            utils.addActions(menu, actions)
        return menu

    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName("%sToolBar" % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            utils.addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar

    # Support Functions

    def noShapes(self):
        return not len(self.labelList)

    def setDirty(self):
        # Even if we autosave the file, we keep the ability to undo
        self.actions.undo.setEnabled(self.canvas.isShapeRestorable)

        if self._config["auto_save"] or self.actions.saveAuto.isChecked():
            label_file = osp.splitext(self.imagePath)[0] + ".json"
            if self.output_dir:
                label_file_without_path = osp.basename(label_file)
                label_file = osp.join(self.output_dir, label_file_without_path)
            self.saveLabels(label_file)
            return
        self.dirty = True
        self.actions.save.setEnabled(True)
        title = self.lngg.__appname__
        if self.filename is not None:
            title = "{} - {}*".format(title, self.filename)
        self.setWindowTitle(title)

    def setClean(self):
        self.dirty = False
        self.actions.save.setEnabled(False)
        self.actions.createMode.setEnabled(True)
        self.actions.createRectangleMode.setEnabled(True)
        self.actions.createCircleMode.setEnabled(True)
        self.actions.createLineMode.setEnabled(True)
        self.actions.createPointMode.setEnabled(True)
        self.actions.createLineStripMode.setEnabled(True)

        title = self.lngg.__appname__
        if self.filename is not None:
            title = "{} - {}".format(title, self.filename)
        self.setWindowTitle(title)

        if self.hasLabelFile():
            self.actions.deleteFile.setEnabled(True)
        else:
            self.actions.deleteFile.setEnabled(False)

    def toggleActions(self, value=True):
        """Enable/Disable widgets which depend on an opened image."""
        for z in self.actions.zoomActions:
            z.setEnabled(value)
        for action in self.actions.onLoadActive:
            action.setEnabled(value)

    def queueEvent(self, function, delay=0):
        """只执行一次，定时器达到时执行，定时器单位ms，"""
        QtCore.QTimer.singleShot(delay, function)

    def status(self, message, delay=5000):
        self.statusBar().showMessage(message, delay)

    def resetState(self):
        """把标注清空，文件名设置为None, 画布重置状态"""
        self.labelList.clear()  # 把多边形标注清空

        self.filename = None  #
        self.imagePath = None
        self.imageData = None
        self.labelFile = None
        self.otherData = None
        self.canvas.resetState()  # 删除图像啥的，刷新

    def currentItem(self):
        items = self.labelList.selectedItems()
        if items:
            return items[0]
        return None

    def addRecentFile(self, filename):
        if filename in self.recentFiles:
            self.recentFiles.remove(filename)
        elif len(self.recentFiles) >= self.maxRecent:
            self.recentFiles.pop()
        self.recentFiles.insert(0, filename)

    # Callbacks

    def undoShapeEdit(self):
        self.canvas.restoreShape()
        self.labelList.clear()
        self.loadShapes(self.canvas.shapes)
        self.actions.undo.setEnabled(self.canvas.isShapeRestorable)

    def tutorial(self):
        url = "https://github.com/zhangzhengde0225"
        webbrowser.open(url)


    def toggleDrawingSensitive(self, drawing=True):
        """Toggle drawing sensitive.
        绘制模式的按钮设置
        In the middle of drawing, toggling between modes should be disabled.
        """
        self.actions.editMode.setEnabled(not drawing)  # 编辑模式不可用
        self.actions.undoLastPoint.setEnabled(drawing)  # 撤销上个点可用
        self.actions.undo.setEnabled(not drawing)  # 撤销不可用
        self.actions.delete.setEnabled(not drawing)  # 删除不可用

    def toggleDrawMode(self, edit=True, createMode="polygon"):
        """
        切换绘制模式，魔棒、新建多边形、新建矩形、新建圆、新建线、新建点、新建线条等的槽
        编辑和新建都归这个管"""
        create_mode_names = [
            'magic_wand', 'polygon', 'rectangle', 'circle', 'line', 'point', 'linestrip']
        a = self.actions
        create_modes = [
            a.magic_wand, a.createMode, a.createRectangleMode, a.createCircleMode,
            a.createLineMode, a.createPointMode, a.createLineStripMode,
        ]
        assert len(create_mode_names) == len(create_modes)
        assert createMode in create_mode_names, f'CreateMode {createMode} not supprted'

        self.canvas.setEditing(edit)
        self.canvas.createMode = createMode  # 设置创建模式, 7种
        if edit:  # 编辑模式
            # 设置所有可用
            for i, m in enumerate(create_mode_names):
                create_modes[i].setEnabled(True)
            # self.actions.createMode.setEnabled(True)
            # self.actions.createRectangleMode.setEnabled(True)
            # self.actions.createCircleMode.setEnabled(True)
            # self.actions.createLineMode.setEnabled(True)
            # self.actions.createPointMode.setEnabled(True)
            # self.actions.createLineStripMode.setEnabled(True)
        else:
            # 设置选择的不再可用
            for i, m in enumerate(create_mode_names):
                if m == createMode:
                    create_modes[i].setEnabled(False)
                else:
                    create_modes[i].setEnabled(True)

            # if createMode == "polygon":
            #     self.actions.createMode.setEnabled(False)
            #     self.actions.createRectangleMode.setEnabled(True)
            #     self.actions.createCircleMode.setEnabled(True)
            #     self.actions.createLineMode.setEnabled(True)
            #     self.actions.createPointMode.setEnabled(True)
            #     self.actions.createLineStripMode.setEnabled(True)
            # elif createMode == "rectangle":
            #     self.actions.createMode.setEnabled(True)
            #     self.actions.createRectangleMode.setEnabled(False)
            #     self.actions.createCircleMode.setEnabled(True)
            #     self.actions.createLineMode.setEnabled(True)
            #     self.actions.createPointMode.setEnabled(True)
            #     self.actions.createLineStripMode.setEnabled(True)
            # elif createMode == "line":
            #     self.actions.createMode.setEnabled(True)
            #     self.actions.createRectangleMode.setEnabled(True)
            #     self.actions.createCircleMode.setEnabled(True)
            #     self.actions.createLineMode.setEnabled(False)
            #     self.actions.createPointMode.setEnabled(True)
            #     self.actions.createLineStripMode.setEnabled(True)
            # elif createMode == "point":
            #     self.actions.createMode.setEnabled(True)
            #     self.actions.createRectangleMode.setEnabled(True)
            #     self.actions.createCircleMode.setEnabled(True)
            #     self.actions.createLineMode.setEnabled(True)
            #     self.actions.createPointMode.setEnabled(False)
            #     self.actions.createLineStripMode.setEnabled(True)
            # elif createMode == "circle":
            #     self.actions.createMode.setEnabled(True)
            #     self.actions.createRectangleMode.setEnabled(True)
            #     self.actions.createCircleMode.setEnabled(False)
            #     self.actions.createLineMode.setEnabled(True)
            #     self.actions.createPointMode.setEnabled(True)
            #     self.actions.createLineStripMode.setEnabled(True)
            # elif createMode == "linestrip":
            #     self.actions.createMode.setEnabled(True)
            #     self.actions.createRectangleMode.setEnabled(True)
            #     self.actions.createCircleMode.setEnabled(True)
            #     self.actions.createLineMode.setEnabled(True)
            #     self.actions.createPointMode.setEnabled(True)
            #     self.actions.createLineStripMode.setEnabled(False)
            # else:
            #     raise ValueError("Unsupported createMode: %s" % createMode)
        # print(f'edit: {edit} creatmode: {createMode}')
        self.actions.editMode.setEnabled(not edit)

    def setEditMode(self):
        self.toggleDrawMode(True)

    def updateFileMenu(self):
        current = self.filename

        def exists(filename):
            return osp.exists(str(filename))

        menu = self.menus.recentFiles
        menu.clear()
        files = [f for f in self.recentFiles if f != current and exists(f)]
        for i, f in enumerate(files):
            icon = utils.newIcon("labels")
            action = QtWidgets.QAction(
                icon, "&%d %s" % (i + 1, QtCore.QFileInfo(f).fileName()), self
            )
            action.triggered.connect(functools.partial(self.loadRecent, f))
            menu.addAction(action)

    def popLabelListMenu(self, point):
        self.menus.labelList.exec_(self.labelList.mapToGlobal(point))

    def validateLabel(self, label):
        # no validation
        if self._config["validate_label"] is None:
            return True

        for i in range(self.uniqLabelList.count()):
            label_i = self.uniqLabelList.item(i).data(Qt.UserRole)
            if self._config["validate_label"] in ["exact"]:
                if label_i == label:
                    return True
        return False

    def editLabel(self, item=None):
        if item and not isinstance(item, LabelListWidgetItem):
            raise TypeError("item must be LabelListWidgetItem type")
        if not self.canvas.editing():
            return
        if not item:
            item = self.currentItem()
        if item is None:
            return
        shape = item.shape()
        if shape is None:
            return
        if self.actions.fusion_label.isChecked():
            decide_point = [self.img_layout[1][0], self.img_layout[2][1]] if len(self.img_layout) == 3 else self.img_layout[-1]
            fusion_points = shape.points
            fp_x = []
            fp_y = []
            for fp in fusion_points:
                fp_x.append(fp.x())
                fp_y.append(fp.y())
                quad = mm_quadrant_decide.quad_decide(decide_point, fp_x, fp_y)
            shape.modal = mm_modal_update.modal_update(self.modals, self.modals_new, decide_point, fp_x, fp_y)
            if shape.modal != 'radar76':
                return
            else:
                fp_new = []
                for i in range(len(fp_x)):
                    fp_new.append([(fp_x[i] - self.img_layout[quad][0]) / self.scale_percent[quad],
                                   (fp_y[i] - self.img_layout[quad][1]) / self.scale_percent[quad]])
                self.fusion_label(self.imagePath, fp_new)
        else:
            print(shape.points)
            text, flags, group_id, tid, status, sgid = self.labelDialog.popUp(
                text=shape.label, flags=shape.flags, group_id=shape.group_id,
                tid_text=shape.tid, status_text=shape.status, status_group_id=shape.status_group_id)
            if text is None:
                return
            if not self.validateLabel(text):
                self.errorMessage(
                    self.tr("Invalid label"),
                    self.tr("Invalid label '{}' with validation type '{}'").format(
                        text, self._config["validate_label"]
                    ),
                )
                return
            shape.label = text
            shape.flags = flags
            shape.group_id = group_id
            shape.tid = tid
            shape.status = status
            shape.status_group_id = sgid

            self._update_shape_color(shape)

            if shape.group_id is None:
                text = shape.label
            else:
                # text = "{} ({})".format(shape.label, shape.group_id)
                text = f"{shape.label} ({shape.group_id})"
            if shape.tid is not None:
                text += f" {shape.tid}"
            if shape.status is not None:
                text += f" {shape.status}"

            """
            if shape.group_id is None:
                item.setText(
                    '{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(
                        shape.label, *shape.fill_color.getRgb()[:3]
                    )
                )
            else:
                item.setText("{} ({})".format(shape.label, shape.group_id))
            """

            item.setText('{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(
                text, *shape.fill_color.getRgb()[:3]))

            self.setDirty()
            if not self.uniqLabelList.findItemsByLabel(shape.label):
                item = QtWidgets.QListWidgetItem()
                item.setData(Qt.UserRole, shape.label)
                self.uniqLabelList.addItem(item)

    def fileSearchChanged(self):
        self.importDirImages(
            self.lastOpenDir,
            pattern=self.fileSearch.text(),
            load=False,
        )

    def fileSelectionChanged(self):
        items = self.fileListWidget.selectedItems()
        if not items:
            return
        item = items[0]

        if not self.mayContinue():
            return

        currIndex = self.imageList.index(str(item.text()))
        if currIndex < len(self.imageList):
            filename = self.imageList[currIndex]
            if filename:
                self.loadFile(filename)

    # React to canvas signals.
    def shapeSelectionChanged(self, selected_shapes):
        self._noSelectionSlot = True
        for shape in self.canvas.selectedShapes:
            shape.selected = False
        self.labelList.clearSelection()
        self.canvas.selectedShapes = selected_shapes
        for shape in self.canvas.selectedShapes:
            shape.selected = True
            item = self.labelList.findItemByShape(shape)
            self.labelList.selectItem(item)
            self.labelList.scrollToItem(item)
        self._noSelectionSlot = False
        n_selected = len(selected_shapes)
        self.actions.delete.setEnabled(n_selected)
        self.actions.duplicate.setEnabled(n_selected)
        self.actions.copy.setEnabled(n_selected)
        self.actions.edit.setEnabled(n_selected == 1)

    def addLabel(self, shape):
        """加载shapes的信息，加载到labelList, uniqLabelList和Properties里"""

        if shape.group_id is None:
            text = shape.label
        else:
            # text = "{} ({})".format(shape.label, shape.group_id)
            text = f"{shape.label} ({shape.group_id})"
        # 多写些东西
        if shape.tid is not None:
            text += f" {shape.tid}"
        if shape.status is not None:
            text += f" {shape.status}"

        label_list_item = LabelListWidgetItem(text, shape)  # 把shape作为这个item的data保存起来
        self.labelList.addItem(label_list_item)
        if not self.uniqLabelList.findItemsByLabel(shape.label):
            item = self.uniqLabelList.createItemFromLabel(shape.label)
            self.uniqLabelList.addItem(item)
            rgb = self._get_rgb_by_label(shape.label)
            self.uniqLabelList.setItemLabel(item, shape.label, rgb)
        self.labelDialog.addLabelHistory(shape.label)  # 对话的两个列表的设置
        self.labelDialog.addStatusHistory(shape.status)
        for action in self.actions.onShapesPresent:
            action.setEnabled(True)

        self._update_shape_color(shape)
        label_list_item.setText(
            '{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(
                text, *shape.fill_color.getRgb()[:3]
            )
        )
        # ●

    def _update_shape_color(self, shape):
        r, g, b = self._get_rgb_by_label(shape.label)
        shape.line_color = QtGui.QColor(r, g, b)
        shape.vertex_fill_color = QtGui.QColor(r, g, b)
        shape.hvertex_fill_color = QtGui.QColor(255, 255, 255)
        shape.fill_color = QtGui.QColor(r, g, b, 128)
        shape.select_line_color = QtGui.QColor(255, 255, 255)
        shape.select_fill_color = QtGui.QColor(r, g, b, 155)

    def _get_rgb_by_label(self, label):
        if self._config["shape_color"] == "auto":
            item = self.uniqLabelList.findItemsByLabel(label)[0]
            label_id = self.uniqLabelList.indexFromItem(item).row() + 1
            label_id += self._config["shift_auto_shape_color"]
            return LABEL_COLORMAP[label_id % len(LABEL_COLORMAP)]
        elif (
                self._config["shape_color"] == "manual"
                and self._config["label_colors"]
                and label in self._config["label_colors"]
        ):
            return self._config["label_colors"][label]
        elif self._config["default_shape_color"]:
            return self._config["default_shape_color"]
        return (0, 255, 0)

    def remLabels(self, shapes):
        for shape in shapes:
            item = self.labelList.findItemByShape(shape)
            self.labelList.removeItem(item)

    def loadShapes(self, shapes, shapes_show, replace=True):
        self._noSelectionSlot = True
        for shape in shapes:
            self.addLabel(shape)
        self.labelList.clearSelection()
        self._noSelectionSlot = False
        self.canvas.loadShapes(shapes_show, replace=replace)

    def loadLabels(self, shapes):
        s = []
        s_show = []
        for shape in shapes:
            modal = shape["modal"]
            label = shape["label"]
            points = shape["points"]
            shape_type = shape["shape_type"]
            flags = shape["flags"]
            group_id = shape["group_id"]
            other_data = shape["other_data"]
            tid = shape['tid']
            status = shape['status']
            status_group_id = shape['status_group_id']

            if not points:
                # skip point-empty shape
                continue

            shape = Shape(
                modal=modal,
                label=label,
                shape_type=shape_type,
                group_id=group_id,
                tid=tid,
                status=status,
                status_group_id=status_group_id,
            )
            for x, y in points:
                shape.addPoint(QtCore.QPointF(x, y))
            shape.close()

            default_flags = {}
            if self._config["label_flags"]:
                for pattern, keys in self._config["label_flags"].items():
                    if re.match(pattern, label):
                        for key in keys:
                            default_flags[key] = False
            shape.flags = default_flags
            shape.flags.update(flags)
            shape.other_data = other_data

            s.append(shape)
            if self.modals_new is None:
                s_show = s
            else:
                if shape.modal in self.modals_new:
                    s_show.append(shape)
                else:
                    continue

        self.loadShapes(s, s_show)

    def loadFlags(self, flags):
        self.flag_widget.clear()
        for key, flag in flags.items():
            item = QtWidgets.QListWidgetItem(key)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if flag else Qt.Unchecked)
            self.flag_widget.addItem(item)

    def saveLabels(self, filename):
        lf = LabelFile()

        # def modal_decide(shape):
        #     decide_point = [self.img_layout[1][0], self.img_layout[2][1]] if len(self.img_layout) == 3 else \
        #     self.img_layout[-1]
        #     p_x = []
        #     p_y = []
        #     for p in shape.points:
        #         p_x.append(p.x())
        #         p_y.append(p.y())
        #     if shape.modal is None:
        #         if self.modals_new is None:
        #             quad = mm_quadrant_decide.quad_decide(decide_point, p_x, p_y)
        #             shape.modal = self.modals[quad]
        #         else:
        #             if len(self.modals_new) == 1:
        #                 shape.modal = self.modals_new[0]
        #             elif len(self.modals_new) == 2:
        #                 if max(p_x) < decide_point[0]:
        #                     shape.modal = self.modals_new[0]
        #                 else:
        #                     shape.modal = self.modals_new[1]
        #             else:
        #                 quad = mm_quadrant_decide.quad_decide(decide_point, p_x, p_y)
        #                 shape.modal = self.modals_new[quad]
        #     else:
        #         shape.modal = shape.modal
        #     return shape.modal

        def format_shape(self, s):
            # PyQt4 cannot handle QVariant
            if isinstance(s, QtCore.QVariant):
                s = s.toPyObject()

            data = s.other_data.copy()  # 好像是个空字典
            # 这里改的太早了  放到后边
            # print((p.x(), p.y()) for p in s.points)

            decide_point = [self.img_layout[1][0], self.img_layout[2][1]] if len(self.img_layout) == 3 else self.img_layout[-1]
            p_x = []
            p_y = []
            for p in s.points:
                p_x.append(p.x())
                p_y.append(p.y())

            if self.modals_new is not None and s.modal not in self.modals_new:
                pass
            else:
                s.modal = mm_modal_update.modal_update(self.modals, self.modals_new, decide_point, p_x, p_y)

            data.update(  # 要添加一个目标的其他标注就在这里添加  !!!
                dict(
                    modal=s.modal,
                    label=s.label.encode("utf-8") if PY2 else s.label,
                    points=[(p.x(), p.y()) for p in s.points],
                    group_id=s.group_id,
                    shape_type=s.shape_type,
                    flags=s.flags,
                    tid=s.tid,
                    status=s.status,
                    status_group_id=s.status_group_id,
                )
            )
            return data

        shapes = [format_shape(self, item.shape()) for item in self.labelList]
        # 读取flag_widget里的项，那些项的text为键，项是否Checked为值，更新flags,
        flags = {}
        for i in range(self.flag_widget.count()):
            item = self.flag_widget.item(i)
            key = item.text()
            flag = item.checkState() == Qt.Checked
            flags[key] = flag  # flag 对应的是否check的状态
        try:
            imagePath = osp.relpath(self.imagePath, osp.dirname(filename))
            imageData = self.imageData if self._config["store_data"] else None
            if osp.dirname(filename) and not osp.exists(osp.dirname(filename)):
                os.makedirs(osp.dirname(filename))
            lf.save(
                filename=filename,
                modals_list=self.modals,
                modals_size=self.modals_size,
                shapes=shapes,
                imagePath=imagePath,
                imageData=imageData,
                imageHeight=self.image.height(),
                imageWidth=self.image.width(),
                otherData=self.otherData,
                flags=flags,
                modals_new=self.modals_new,
                layout=self.img_layout,
                scale_percent_list=self.scale_percent,
            )
            self.labelFile = lf
            items = self.fileListWidget.findItems(
                self.imagePath, Qt.MatchExactly
            )
            if len(items) > 0:
                if len(items) != 1:
                    raise RuntimeError("There are duplicate files.")
                items[0].setCheckState(Qt.Checked)
            # disable allows next and previous image to proceed
            # self.filename = filename
            return True
        except LabelFileError as e:
            self.errorMessage(
                self.tr("Error saving label data"), self.tr("<b>%s</b>") % e
            )
            return False

    def duplicateSelectedShape(self):
        added_shapes = self.canvas.duplicateSelectedShapes()
        self.labelList.clearSelection()
        for shape in added_shapes:
            self.addLabel(shape)
        self.setDirty()

    def pasteSelectedShape(self):
        self.loadShapes(self._copied_shapes, replace=False)
        self.setDirty()

    def copySelectedShape(self):
        self._copied_shapes = [s.copy() for s in self.canvas.selectedShapes]
        self.actions.paste.setEnabled(len(self._copied_shapes) > 0)

    def labelSelectionChanged(self):
        if self._noSelectionSlot:
            return
        if self.canvas.editing():
            selected_shapes = []
            for item in self.labelList.selectedItems():
                selected_shapes.append(item.shape())
            if selected_shapes:
                self.canvas.selectShapes(selected_shapes)
            else:
                self.canvas.deSelectShape()

    def labelItemChanged(self, item):
        shape = item.shape()
        self.canvas.setShapeVisible(shape, item.checkState() == Qt.Checked)

    def labelOrderChanged(self):
        self.setDirty()
        self.canvas.loadShapes([item.shape() for item in self.labelList])

    # Callback functions:

    def newShape(self):
        """Pop-up and give focus to the label editor.

        position MUST be in global coordinates.
        """
        items = self.uniqLabelList.selectedItems()
        text = None
        if items:
            text = items[0].data(Qt.UserRole)
        flags = {}
        group_id = None
        tid = None
        status = None
        sgid = None
        if self._config["display_label_popup"] or not text:
            previous_text = self.labelDialog.edit.text()
            previous_tid = self.labelDialog.tid_edit.text()
            previous_status = self.labelDialog.status_edit.text()
            text, flags, group_id, tid, status, sgid = self.labelDialog.popUp(
                text)  # 弹出对话框啦
            # print(f'text: {text} {flags} {group_id} tid: {tid} {status} {sgid}')
            if not text:
                self.labelDialog.edit.setText(previous_text)
                self.labelDialog.tid_edit.setText(previous_tid)
                self.labelDialog.status_edit.setText(previous_status)

        # 验证，跳过
        if text and not self.validateLabel(text):
            self.errorMessage(
                self.tr("Invalid label"),
                self.tr("Invalid label '{}' with validation type '{}'").format(
                    text, self._config["validate_label"]
                ),
            )
            text = ""

        if text:
            self.labelList.clearSelection()
            shape = self.canvas.setLastLabel(text, flags, tid, status, sgid)  # 返回添加信息后的形状
            shape.group_id = group_id

            decide_point = [self.img_layout[1][0], self.img_layout[2][1]] if len(self.img_layout) == 3 else self.img_layout[-1]
            p_x = []
            p_y = []
            for p in shape.points:
                p_x.append(p.x())
                p_y.append(p.y())
            shape.modal = mm_modal_update.modal_update(self.modals, self.modals_new, decide_point, p_x, p_y)

            self.addLabel(shape)
            self.actions.editMode.setEnabled(True)
            self.actions.undoLastPoint.setEnabled(False)
            self.actions.undo.setEnabled(True)
            self.setDirty()
        else:
            self.canvas.undoLastLine()
            self.canvas.shapesBackups.pop()

    def scrollRequest(self, delta, orientation):
        units = -delta * 0.1  # natural scroll
        bar = self.scrollBars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)

    def setScroll(self, orientation, value):
        self.scrollBars[orientation].setValue(value)
        self.scroll_values[orientation][self.filename] = value

    def setZoom(self, value):
        self.actions.fitWidth.setChecked(False)
        self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)
        self.zoom_values[self.filename] = (self.zoomMode, value)

    def addZoom(self, increment=1.1):
        zoom_value = self.zoomWidget.value() * increment
        if increment > 1:
            zoom_value = math.ceil(zoom_value)
        else:
            zoom_value = math.floor(zoom_value)
        self.setZoom(zoom_value)

    def zoomRequest(self, delta, pos):
        canvas_width_old = self.canvas.width()
        units = 1.1
        if delta < 0:
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

    def setFitWindow(self, value=True):
        if value:
            self.actions.fitWidth.setChecked(False)
        self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
        self.adjustScale()

    def setFitWidth(self, value=True):
        if value:
            self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
        self.adjustScale()

    def enableKeepPrevScale(self, enabled):
        self._config["keep_prev_scale"] = enabled
        self.actions.keepPrevScale.setChecked(enabled)

    def enableAutoAI(self, enabled):
        self._config["ai"]["auto_ai"] = enabled
        self.actions.auto_ai.setChecked(enabled)

    def fusion_label(self, file, points):
        fusion_img, fusion_points = draw_predict.fusion(file, points)
        line_color = (0, 0, 255)
        line_width = 5
        cv2.line(fusion_img, fusion_points[0], fusion_points[1], line_color, line_width)
        cv2.line(fusion_img, fusion_points[0], fusion_points[2], line_color, line_width)
        cv2.line(fusion_img, fusion_points[2], fusion_points[3], line_color, line_width)
        cv2.line(fusion_img, fusion_points[1], fusion_points[3], line_color, line_width)
        cv2.namedWindow('result', 0)
        cv2.resizeWindow('result', 500, 500)
        cv2.imshow('result', fusion_img)


    def onNewBrightnessContrast(self, qimage):
        self.canvas.loadPixmap(
            QtGui.QPixmap.fromImage(qimage), clear_shapes=False
        )

    def brightnessContrast(self, value):
        dialog = BrightnessContrastDialog(
            utils.img_data_to_pil(self.imageData),
            self.onNewBrightnessContrast,
            parent=self,
        )
        brightness, contrast = self.brightnessContrast_values.get(
            self.filename, (None, None)
        )
        if brightness is not None:
            dialog.slider_brightness.setValue(brightness)
        if contrast is not None:
            dialog.slider_contrast.setValue(contrast)
        dialog.exec_()

        brightness = dialog.slider_brightness.value()
        contrast = dialog.slider_contrast.value()
        self.brightnessContrast_values[self.filename] = (brightness, contrast)

    def togglePolygons(self, value):
        for item in self.labelList:
            item.setCheckState(Qt.Checked if value else Qt.Unchecked)

    def loadFile(self, filename=None, modals_new=None):
        """Load the specified file, or the last opened file if None.
        :param modals_new:
        """
        # changing fileListWidget loads file
        # print(f'{self.imageList}')
        if filename in self.imageList and (
                self.fileListWidget.currentRow() != self.imageList.index(filename)
        ):
            self.fileListWidget.setCurrentRow(self.imageList.index(filename))  # 更新行
            self.fileListWidget.repaint()  # 刷新
            return

        self.resetState()  # 清空self.filename，
        self.canvas.setEnabled(False)  # 禁用控件，不相应鼠标和键盘事件
        if filename is None:
            filename = self.settings.value("filename", "")
        filename = str(filename)

        if self.mm:
            mm_files = mm.utils.get_mm_files_from_filename(self.mm_data, filename)  # 字典，模态名是键
            files = mm_files
        else:
            files = filename

        # 检查单/多模态文件是否存在
        if not mm.mm_load_file.check_file_exists(self, files=files):
            return False
        # 状态栏显示加载信息
        self.status(str(self.tr("Loading %s...")) % osp.basename(str(filename)))
        # 读取单/多模态数据
        load_ret = mm.mm_load_file.load_json(self, files=files, mm_modals_new=modals_new)  # 返回的是路径
        # print(f'loadret: {load_ret}')
        if not load_ret:
            return False
        self.imageData, self.imagePath, self.labelFile, self.modals, self.modal_imgs, self.img_layout, self.modals_size_org, self.scale_percent = load_ret
        if len(self.scale_percent) == len(self.modals):
            self.modals_size = []
            for i in range(len(self.scale_percent)):
                modal_size_x = int(self.modals_size_org[i][0]/self.scale_percent[i])
                modal_size_y = int(self.modals_size_org[i][1]/self.scale_percent[i])
                self.modals_size.append((modal_size_x, modal_size_y, 3))
        else:
            pass
        # 加载，把二进制ImageData转为QT格式用于在画布上显示
        image = mm.utils.imgdata2qt(self, self.imageData, filename)
        self.image = image
        self.filename = filename
        if self._config["keep_prev"]:
            prev_shapes = self.canvas.shapes
        self.canvas.loadPixmap(QtGui.QPixmap.fromImage(image))  # 加载图像

        # 加载mmlist
        # self.mmList
        self.mmList.updateModals(self.modals, self.modal_imgs, modals_new)

        # 加载标注形状
        flags = {k: False for k in self._config["flags"] or []}
        if self.labelFile:  # 如果存在标注文件
            self.loadLabels(self.labelFile.shapes)  # 加载形状
            if self.labelFile.flags is not None:
                flags.update(self.labelFile.flags)

        # 加载标记
        self.loadFlags(flags)  # 加载flag
        # 无形状且保留前面的形状，加载前面的形状
        if self._config["keep_prev"] and self.noShapes():
            self.loadShapes(prev_shapes, replace=False)
            self.setDirty()
        else:
            self.setClean()
        self.canvas.setEnabled(True)
        # set zoom values
        is_initial_load = not self.zoom_values
        if self.filename in self.zoom_values:
            self.zoomMode = self.zoom_values[self.filename][0]
            self.setZoom(self.zoom_values[self.filename][1])
        elif is_initial_load or not self._config["keep_prev_scale"]:
            self.adjustScale(initial=True)
        # set scroll values
        for orientation in self.scroll_values:
            if self.filename in self.scroll_values[orientation]:
                self.setScroll(
                    orientation, self.scroll_values[orientation][self.filename]
                )
        # set brightness contrast values
        dialog = BrightnessContrastDialog(
            utils.img_data_to_pil(self.imageData),
            self.onNewBrightnessContrast,
            parent=self,
        )
        brightness, contrast = self.brightnessContrast_values.get(
            self.filename, (None, None)
        )
        if self._config["keep_prev_brightness"] and self.recentFiles:
            brightness, _ = self.brightnessContrast_values.get(
                self.recentFiles[0], (None, None)
            )
        if self._config["keep_prev_contrast"] and self.recentFiles:
            _, contrast = self.brightnessContrast_values.get(
                self.recentFiles[0], (None, None)
            )
        if brightness is not None:
            dialog.slider_brightness.setValue(brightness)
        if contrast is not None:
            dialog.slider_contrast.setValue(contrast)
        self.brightnessContrast_values[self.filename] = (brightness, contrast)
        if brightness is not None or contrast is not None:
            dialog.onNewValue(None)
        self.paintCanvas()
        self.addRecentFile(self.filename)
        self.toggleActions(True)
        self.canvas.setFocus()
        self.status(str(self.tr("Loaded %s")) % osp.basename(str(filename)))
        return True

    def resizeEvent(self, event):
        if (
                self.canvas
                and not self.image.isNull()
                and self.zoomMode != self.MANUAL_ZOOM
        ):
            self.adjustScale()
        super(MainWindow, self).resizeEvent(event)

    def paintCanvas(self):
        assert not self.image.isNull(), "cannot paint null image"
        self.canvas.scale = 0.01 * self.zoomWidget.value()
        self.canvas.adjustSize()
        self.canvas.update()

    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        value = int(100 * value)
        self.zoomWidget.setValue(value)
        self.zoom_values[self.filename] = (self.zoomMode, value)

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

    def enableSaveImageWithData(self, enabled):
        self._config["store_data"] = enabled
        self.actions.saveWithImageData.setChecked(enabled)

    def closeEvent(self, event):
        if not self.mayContinue():
            event.ignore()
        self.settings.setValue(
            "filename", self.filename if self.filename else ""
        )
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.saveState())
        self.settings.setValue("recentFiles", self.recentFiles)
        # ask the use for where to save the labels
        # self.settings.setValue('window/geometry', self.saveGeometry())

    def dragEnterEvent(self, event):
        extensions = [
            ".%s" % fmt.data().decode().lower()
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]
        if event.mimeData().hasUrls():
            items = [i.toLocalFile() for i in event.mimeData().urls()]
            if any([i.lower().endswith(tuple(extensions)) for i in items]):
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not self.mayContinue():
            event.ignore()
            return
        items = [i.toLocalFile() for i in event.mimeData().urls()]
        self.importDroppedImageFiles(items)

    # User Dialogs #

    def loadRecent(self, filename):
        if self.mayContinue():
            self.loadFile(filename)

    def openPrevImg(self, _value=False):
        keep_prev = self._config["keep_prev"]
        if QtWidgets.QApplication.keyboardModifiers() == (
                Qt.ControlModifier | Qt.ShiftModifier
        ):
            self._config["keep_prev"] = True

        if not self.mayContinue():
            return

        if len(self.imageList) <= 0:
            return

        if self.filename is None:
            return

        currIndex = self.imageList.index(self.filename)
        if currIndex - 1 >= 0:
            filename = self.imageList[currIndex - 1]
            if filename:
                self.loadFile(filename)

        self._config["keep_prev"] = keep_prev

    def openNextImg(self, _value=False, load=True):
        keep_prev = self._config["keep_prev"]  # 配置文件，保持前一个
        if QtWidgets.QApplication.keyboardModifiers() == (
                Qt.ControlModifier | Qt.ShiftModifier):  # 如果此时Control或Shift被按下
            self._config["keep_prev"] = True

        if not self.mayContinue():  # 如果存在要清除的状态
            return

        if len(self.imageList) <= 0:  # 没有图像
            return

        filename = None
        if self.filename is None:  # 传入文件名为空，取列表的第0个
            filename = self.imageList[0]  #
        else:  # 根据名字去索引，然后取下一个
            currIndex = self.imageList.index(self.filename)
            if currIndex + 1 < len(self.imageList):  #
                filename = self.imageList[currIndex + 1]
            else:  # 如果当前已经是最后一个，取最后一个
                filename = self.imageList[-1]
        self.filename = filename  # 赋值

        if self.actions.auto_ai.isChecked() and load:
            self.run_ai()

        if self.filename and load:
            self.loadFile(self.filename)

        self._config["keep_prev"] = keep_prev  # 又赋值回去，所以keep_prev是由键盘控制的，是暂时的

    def openFile(self, _value=False):
        # print(f'open_file: {_value}')
        if not self.mayContinue():
            return
        path = osp.dirname(str(self.filename)) if self.filename else "."
        formats = [
            "*.{}".format(fmt.data().decode())
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]
        filters = self.tr("Image & Label files (%s)") % " ".join(
            formats + ["*%s" % LabelFile.suffix]
        )
        fileDialog = FileDialogPreview(self)  # 开一个文件对话框
        fileDialog.setFileMode(FileDialogPreview.ExistingFile)
        fileDialog.setNameFilter(filters)  # 设置支持的文件类型
        fileDialog.setWindowTitle(
            self.tr("%s - Choose Image or Label file") % self.lngg.__appname__, )  # 设置对话框名字
        fileDialog.setWindowFilePath(path)  # 设置路径
        fileDialog.setViewMode(FileDialogPreview.Detail)  # 详细
        if fileDialog.exec_():
            fileName = fileDialog.selectedFiles()[0]
            # print(f'filename: {fileName}')
            if fileName:
                self.loadFile(fileName)

    def changeOutputDirDialog(self, _value=False):
        default_output_dir = self.output_dir
        if default_output_dir is None and self.filename:
            default_output_dir = osp.dirname(self.filename)
        if default_output_dir is None:
            default_output_dir = self.currentPath()

        output_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            self.tr("%s - Save/Load Annotations in Directory") % self.lngg.__appname__,
            default_output_dir,
            QtWidgets.QFileDialog.ShowDirsOnly
            | QtWidgets.QFileDialog.DontResolveSymlinks,
        )
        output_dir = str(output_dir)

        if not output_dir:
            return

        self.output_dir = output_dir

        self.statusBar().showMessage(
            self.tr("%s . Annotations will be saved/loaded in %s")
            % ("Change Annotations Dir", self.output_dir)
        )
        self.statusBar().show()

        current_filename = self.filename
        self.importDirImages(self.lastOpenDir, load=False)

        if current_filename in self.imageList:
            # retain currently selected file
            self.fileListWidget.setCurrentRow(
                self.imageList.index(current_filename)
            )
            self.fileListWidget.repaint()

    def saveFile(self, _value=False):
        assert not self.image.isNull(), "cannot save empty image"
        if self.labelFile:
            # DL20180323 - overwrite when in directory
            self._saveFile(self.labelFile.filename)
        elif self.output_file:
            self._saveFile(self.output_file)
            self.close()
        else:
            self._saveFile(self.saveFileDialog())

    def saveFileAs(self, _value=False):
        assert not self.image.isNull(), "cannot save empty image"
        self._saveFile(self.saveFileDialog())

    def saveFileDialog(self):
        caption = self.tr("%s - Choose File") % self.lngg.__appname__
        filters = self.tr("Label files (*%s)") % LabelFile.suffix
        if self.output_dir:
            dlg = QtWidgets.QFileDialog(
                self, caption, self.output_dir, filters
            )
        else:
            dlg = QtWidgets.QFileDialog(
                self, caption, self.currentPath(), filters
            )
        dlg.setDefaultSuffix(LabelFile.suffix[1:])
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setOption(QtWidgets.QFileDialog.DontConfirmOverwrite, False)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        basename = osp.basename(osp.splitext(self.filename)[0])
        if self.output_dir:
            default_labelfile_name = osp.join(
                self.output_dir, basename + LabelFile.suffix
            )
        else:
            default_labelfile_name = osp.join(
                self.currentPath(), basename + LabelFile.suffix
            )
        filename = dlg.getSaveFileName(
            self,
            self.tr("Choose File"),
            default_labelfile_name,
            self.tr("Label files (*%s)") % LabelFile.suffix,
        )
        if isinstance(filename, tuple):
            filename, _ = filename
        return filename

    def _saveFile(self, filename):
        if filename and self.saveLabels(filename):
            self.addRecentFile(filename)
            self.setClean()

    def closeFile(self, _value=False):
        if not self.mayContinue():
            return
        self.resetState()
        self.setClean()
        self.toggleActions(False)
        self.canvas.setEnabled(False)
        self.actions.saveAs.setEnabled(False)

    def getLabelFile(self):
        if self.filename.lower().endswith(".json"):
            label_file = self.filename
        else:
            label_file = osp.splitext(self.filename)[0] + ".json"

        return label_file

    def deleteFile(self):
        mb = QtWidgets.QMessageBox
        msg = self.tr(
            "You are about to permanently delete this label file, "
            "proceed anyway?"
        )
        answer = mb.warning(self, self.tr("Attention"), msg, mb.Yes | mb.No)
        if answer != mb.Yes:
            return

        label_file = self.getLabelFile()
        if osp.exists(label_file):
            os.remove(label_file)
            logger.info("Label file is removed: {}".format(label_file))

            item = self.fileListWidget.currentItem()
            item.setCheckState(Qt.Unchecked)

            self.resetState()

    # Message Dialogs. #
    def hasLabels(self):
        if self.noShapes():
            self.errorMessage(
                "No objects labeled",
                "You must label at least one object to save the file.",
            )
            return False
        return True

    def hasLabelFile(self):
        if self.filename is None:
            return False

        label_file = self.getLabelFile()
        return osp.exists(label_file)

    def mayContinue(self):
        """看看是否有标注修改过，需要保存的，有就返回True"""
        if not self.dirty:  # True or False,
            return True
        mb = QtWidgets.QMessageBox
        msg = self.tr('Save annotations to "{}" before closing?').format(
            self.filename
        )
        answer = mb.question(
            self,
            self.tr("Save annotations?"),
            msg,
            mb.Save | mb.Discard | mb.Cancel,
            mb.Save,
        )
        if answer == mb.Discard:
            return True
        elif answer == mb.Save:
            self.saveFile()
            return True
        else:  # answer == mb.Cancel
            return False

    def errorMessage(self, title, message):
        return QtWidgets.QMessageBox.critical(
            self, title, "<p><b>%s</b></p>%s" % (title, message)
        )

    def currentPath(self):
        return osp.dirname(str(self.filename)) if self.filename else "."

    def toggleKeepPrevMode(self):
        self._config["keep_prev"] = not self._config["keep_prev"]

    def removeSelectedPoint(self):
        self.canvas.removeSelectedPoint()
        self.canvas.update()
        if not self.canvas.hShape.points:
            self.canvas.deleteShape(self.canvas.hShape)
            self.remLabels([self.canvas.hShape])
            self.setDirty()
            if self.noShapes():
                for action in self.actions.onShapesPresent:
                    action.setEnabled(False)

    def deleteSelectedShape(self):
        yes, no = QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        msg = self.tr(
            "You are about to permanently delete {} polygons, "
            "proceed anyway?"
        ).format(len(self.canvas.selectedShapes))
        if yes == QtWidgets.QMessageBox.warning(
                self, self.tr("Attention"), msg, yes | no, yes
        ):
            self.remLabels(self.canvas.deleteSelected())
            self.setDirty()
            if self.noShapes():
                for action in self.actions.onShapesPresent:
                    action.setEnabled(False)

    def copyShape(self):
        self.canvas.endMove(copy=True)
        for shape in self.canvas.selectedShapes:
            self.addLabel(shape)
        self.labelList.clearSelection()
        self.setDirty()

    def moveShape(self):
        self.canvas.endMove(copy=False)
        self.setDirty()

    def openDirDialog(self, _value=False, dirpath=None):
        if not self.mayContinue():
            return

        defaultOpenDirPath = dirpath if dirpath else "."
        if self.lastOpenDir and osp.exists(self.lastOpenDir):  # 默认位置
            defaultOpenDirPath = self.lastOpenDir
        else:
            defaultOpenDirPath = (
                osp.dirname(self.filename) if self.filename else "."
            )

        targetDirPath = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self,
                self.tr("%s - Open Directory") % self.lngg.__appname__,
                defaultOpenDirPath,
                QtWidgets.QFileDialog.ShowDirsOnly
                | QtWidgets.QFileDialog.DontResolveSymlinks,
            )
        )
        # print(f'target_dir_path: {targetDirPath}')  # 字符串，用File对话框打开的路径嘛
        self.importDirImages(targetDirPath)

    @property
    def imageList(self):
        lst = []
        for i in range(self.fileListWidget.count()):
            item = self.fileListWidget.item(i)
            lst.append(item.text())
        return lst

    def importDroppedImageFiles(self, imageFiles):
        extensions = [
            ".%s" % fmt.data().decode().lower()
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]

        self.filename = None
        for file in imageFiles:
            if file in self.imageList or not file.lower().endswith(
                    tuple(extensions)
            ):
                continue
            label_file = osp.splitext(file)[0] + ".json"
            if self.output_dir:
                label_file_without_path = osp.basename(label_file)
                label_file = osp.join(self.output_dir, label_file_without_path)
            item = QtWidgets.QListWidgetItem(file)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.fileListWidget.addItem(item)

        if len(self.imageList) > 1:
            self.actions.openNextImg.setEnabled(True)
            self.actions.openPrevImg.setEnabled(True)

        self.openNextImg()

    def importDirImages(self, dirpath, pattern=None, load=True):
        self.actions.openNextImg.setEnabled(True)
        self.actions.openPrevImg.setEnabled(True)

        if not self.mayContinue() or not dirpath:
            return

        self.lastOpenDir = dirpath
        self.filename = None
        self.fileListWidget.clear()
        for filename in self.scanAllImages(dirpath):
            if pattern and pattern not in filename:
                continue
            label_file = osp.splitext(filename)[0] + ".json"
            if self.output_dir:
                label_file_without_path = osp.basename(label_file)  # name
                label_file = osp.join(self.output_dir, label_file_without_path)
            item = QtWidgets.QListWidgetItem(filename)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
                item.setCheckState(Qt.Checked)  # 就是前面的勾
            else:
                item.setCheckState(Qt.Unchecked)
            self.fileListWidget.addItem(item)
        self.openNextImg(load=load)

    def scanAllImages(self, folderPath):
        if self.mm:  # 加载多模态数据
            mm_data = mm.utils.scanMMImages(folderPath, self.mm_names, self.mm_cfg['suffix'])
            self.mm_data = mm_data  # list长度是条目数，每个条目是一个字典，每个字典有n个模态名作为键，值是路径，至少有1个模态是有值的
            images = []
            for i, data in enumerate(self.mm_data):
                paths = [data[x] for x in self.mm_names if data[x] is not None]
                assert len(paths) >= 1, f'有一个条目任何一个模态的都没有数据：{data}'
                images.append(paths[0])
            assert len(images) == len(self.mm_data)
        else:
            extensions = [
                ".%s" % fmt.data().decode().lower()
                for fmt in QtGui.QImageReader.supportedImageFormats()
            ]

            # print(extensions)  # QtGui.QImageReader支持的格式，'.bmp, .gif, .jpg 等等'
            images = []
            for root, dirs, files in os.walk(folderPath):
                for file in files:
                    if file.lower().endswith(tuple(extensions)):
                        relativePath = osp.join(root, file)
                        images.append(relativePath)
            images.sort(key=lambda x: x.lower())

        return images

    def run_ai(self):
        """run ai的槽"""

        # 1.清空状态
        if not self.mayContinue():
            return
        self.canvas.setEnabled(False)
        self.status(str(self.tr(f"Running AI...")))
        self.actions.stop_ai.setEnabled(True)
        self.actions.run_ai.setEnabled(False)

        # 2.读取图像，
        idx = self.imageList.index(self.filename)
        # print(f'idx: {idx} {self.imagePath} {self.filename}')
        idxes = reversed([idx - x for x in range(2) if idx - x >= 0])  # 0: [0], 1:[1, 0] 2: [2, 1]
        files = [self.imageList[x] for x in idxes]  # 从前到后排序，2个图像，最后一个是当前图像

        ai_ret, im0 = self.ai.run(files)  # 某种格式，其实返回的只是最后一张图的检测结果，传多张的为了调用跟踪，即当前图的结果

        # 合并到当前标注里，并保存
        json_path = self.getLabelFile()
        if os.path.exists(json_path):
            lf = LabelFile(json_path)
        else:
            lf = LabelFile()
            lf.filename = json_path
            lf.imagePath = str(Path(files[-1]).name)
            lf.otherData = None
        lf.merge_shapes(ai_ret)  # 合并图形，保存在lf.shapes里
        # 保存
        flags = self.flags if hasattr(self, 'flags') else None
        imageData = lf.imageData if self._config["store_data"] else None
        filename = json_path
        lf.save(
            filename=filename,
            modals_list=self.modals,
            modals_size=self.modals_size,
            shapes=lf.shapes,
            imagePath=lf.imagePath,
            imageData=imageData,
            imageHeight=self.image.height(),
            imageWidth=self.image.width(),
            otherData=self.otherData,
            flags=flags,
            modals_new=self.modals_new,
            layout=self.img_layout,
        )
        # fileList的item打勾
        items = self.fileListWidget.findItems(files[-1], Qt.MatchExactly)
        if len(items) != 1:
            logger.warn(
                f'Found items more than 1 in fileListWidget by name: {files[-1]}, setChecked of the first one.'
            )
        items[0].setCheckState(Qt.Checked)

        # 重新加载
        self.loadFile(files[-1])

        self.actions.run_ai.setEnabled(True)
        self.actions.stop_ai.setEnabled(False)
        # self.canvas.setEnabled(True)
        # self.canvas.setFocus()
        self.status(str(self.tr(f"Run AI Finished.")))

    def stop_ai(self):
        pass

    def slot_mm_item_double_cliked(self):
        for item in self.labelList:
            print(item.shape())

    def slot_mm_item_check_state_changed(self):
        state_list = []
        for it in self.mmList.items:
            state_list.append(it.checkState())
        self.modals_new = self.mmList.slot_checkstate_changed(state_list)
        print(self.modals_new)
        self.loadFile(self.filename, modals_new=self.modals_new)
        # 多模态修改 信号传递

        # 根据当前模态，读取数据，合并图像，shengcheng layout
        # hebinghoud tuxiang -->> canvas
        # hebinghou shapes -->> convas.shape
    

    def test_print(self):
        print(self.actions.fusion_label.isChecked())

    # 关于证书
    def license(self):
        self.licenseDialog.update_activate_info()
        self.licenseDialog.popUp()

    def check_license(self):
        # print('check license')
        passed = self.licenseDialog.check_license()
        # TODO linux激活读取uuid有问题
        passed = True
        if passed:
            pass
        else:
            self.licenseDialog.update_activate_info()
            activated = self.licenseDialog.popUp()
            if not activated:
                self.check_license()



