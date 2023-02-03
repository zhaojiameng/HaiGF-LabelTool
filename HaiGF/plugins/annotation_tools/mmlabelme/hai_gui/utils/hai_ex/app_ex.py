"""
extension of the mainwindow
"""
import functools
from math import frexp

from hai_gui import ai
from hai_gui import mm
from hai_gui.mm_label_file import MMLabelFile as LabelFile
from hai_gui.translate import build_language_config
from hai_gui.config import get_config
from hai_gui.shape import Shape
# from qtpy import QtGui
# from qtpy import QtWidgets
from PySide2 import QtGui, QtWidgets
from .. import fmtShortcut
# from hai_gui.hai import hai_client
from .manager_dock import ManagerDock
import damei as dm

logger = dm.get_logger('app_ex')


class AppEx(ManagerDock):

    def first_init(self, config):
        """some init"""

        # see labelme/config/default_config.yaml for valid configuration
        if config is None:
            config = get_config()
        self._config = config
        # 语言
        lngg = build_language_config(self._config['language'])
        self.lngg = lngg
        if self._config['mm']['mm']:  # 区分mmlabelme和普通的labelme, True False
            self.mm = True
            self.mm_cfg = self._config['mm']
            self.mm_names = self.mm_cfg['names']
            self.mm_data = None  # 扫描时更新所有的数据
            LabelFile.mm = True
            LabelFile.mm_names = self.mm_names
            self.modals = None  # 当前的模态
            self.img_layout = [[0, 0]]  # 当前画布的布局
        else:
            self.mm = False
            self.mm_cfg = None
            self.mm_names = None
            self.mm_data = None
            LabelFile.mm = False
        self.ai_enabled = self._config['ai']['enabled']
        if self.ai_enabled:
            self.ai = ai.MMAi()
            # from center_fusion import draw_predict
        else:
            self.ai = None
        
        self.hai_ip = config['ip']
        self.hai_port = config['port']


    def shape_init(self):

        # set default shape colors, 默认形状的颜色
        Shape.line_color = QtGui.QColor(*self._config["shape"]["line_color"])
        Shape.fill_color = QtGui.QColor(*self._config["shape"]["fill_color"])
        Shape.select_line_color = QtGui.QColor(
            *self._config["shape"]["select_line_color"]
        )
        Shape.select_fill_color = QtGui.QColor(
            *self._config["shape"]["select_fill_color"]
        )
        Shape.vertex_fill_color = QtGui.QColor(
            *self._config["shape"]["vertex_fill_color"]
        )
        Shape.hvertex_fill_color = QtGui.QColor(
            *self._config["shape"]["hvertex_fill_color"]
        )

        # Set point size from config file
        Shape.point_size = self._config["shape"]["point_size"]

    def set_labels(self):
        for label in self._config["labels"]:  # 设置标注
                item = self.uniqLabelList.createItemFromLabel(label)
                self.uniqLabelList.addItem(item)
                rgb = self._get_rgb_by_label(label)
                self.uniqLabelList.setItemLabel(item, label, rgb)

    def set_dock_features(self, docks):
        # dock features
        features = QtWidgets.QDockWidget.DockWidgetFeatures()  
        for dock in docks:
            if self._config[dock]["closable"]:
                features = features | QtWidgets.QDockWidget.DockWidgetClosable
            if self._config[dock]["floatable"]:
                features = features | QtWidgets.QDockWidget.DockWidgetFloatable
            if self._config[dock]["movable"]:
                features = features | QtWidgets.QDockWidget.DockWidgetMovable
            getattr(self, dock).setFeatures(features)
            if self._config[dock]["show"] is False:
                getattr(self, dock).setVisible(False)


    def set_zoom_widget(self):
        self.zoomWidget.setWhatsThis(
            str(
                self.tr(
                    "Zoom in or out of the image. Also accessible with "
                    "{} and {} from the canvas."
                )
            ).format(
                fmtShortcut(
                    "{},{}".format(self._config["shortcuts"]["zoom_in"], self._config["shortcuts"]["zoom_out"])
                ),
                fmtShortcut(self.tr("Ctrl+Wheel")),
            )
        )

    def set_menu(self, utils, labelMenu):
        lngg = self.lngg
        a = self.actions

        self.menus = utils.struct(
            file=self.menu(self.tr(lngg.menu_file)),
            edit=self.menu(self.tr(lngg.menu_edit)),
            view=self.menu(self.tr(lngg.menu_view)),
            ai=self.menu(self.tr(lngg.menu_ai)),
            help=self.menu(self.tr(lngg.menu_help)),
            recentFiles=QtWidgets.QMenu(self.tr(lngg.open_recent)),
            labelList=labelMenu,
        )

        utils.addActions(
            self.menus.file,  # 文件
            (
                a.open,
                a.openNextImg,
                a.openPrevImg,
                a.opendir,
                self.menus.recentFiles,
                a.save,
                a.saveAs,
                a.saveAuto,
                a.changeOutputDir,
                a.saveWithImageData,
                a.close,
                a.deleteFile,
                None,
                a.quit,
            ),
        )

        utils.addActions(
            self.menus.view,  # 视图
            (
                self.flag_dock.toggleViewAction(),
                self.label_dock.toggleViewAction(),
                self.shape_dock.toggleViewAction(),
                self.file_dock.toggleViewAction(),
                self.mm_dock.toggleViewAction(),
                None,
                a.fill_drawing,
                None,
                a.hideAll,
                a.showAll,
                None,
                a.zoomIn,
                a.zoomOut,
                a.zoomOrg,
                a.keepPrevScale,
                None,
                a.fitWindow,
                a.fitWidth,
                None,
                a.brightnessContrast,
            ),
        )
        utils.addActions(
            self.menus.ai,  # AI
            (
                a.run_ai,
                a.stop_ai,
                a.configure_ai,
                a.auto_ai,
                a.fusion_label,
            )
        )

        utils.addActions(
            self.menus.help,   # 帮助
            (
                a.help, 
                a.license,
            ))

        return self.menus

    def set_tool_bars(self):
        """设置工具栏"""
        a = self.actions

        self.tools = self.toolbar("Tools")  # ToolBar(title)
        self.actions.tool = (
            a.open,
            a.opendir,
            a.openNextImg,
            a.openPrevImg,
            a.save,
            a.deleteFile,
            None,
            a.createMode,
            a.editMode,
            a.duplicate,
            a.copy,
            a.paste,
            a.delete,
            a.undo,
            a.brightnessContrast,
            None,
            a.zoom,
            a.fitWidth,
        )

        self.ai_tools = self.toolbar("AI Tools")
        self.actions.ai_tools = (
            a.run_ai,
            a.stop_ai,
            a.configure_ai,
            a.auto_ai,
            a.fusion_label,)

        self.side_bar = self.toolbar("Side Bar")   # 界面上显示的工具栏
        # self.actions.side_bar = a.side_bar  # 在创建actions时，已经定义过了

        self.edit_tools = self.toolbar("Edit Tools")

    def set_canvas_context_menu(self, utils):
        """设置在画布中右击和移动时的菜单"""
        self.canvas.vertexSelected.connect(self.actions.removePoint.setEnabled)
        action = functools.partial(utils.newAction, self) 
        utils.addActions(self.canvas.menus[0], self.actions.menu)
        utils.addActions(
            self.canvas.menus[1],
            (
                action("&Copy here", self.copyShape),
                action("&Move here", self.moveShape),
            ),
        )

    def populateModeActions(self, utils):
        """填充模式动作，真正的指定各菜单的动作"""
        tool, menu = self.actions.tool, self.actions.menu
        self.tools.clear()
        utils.addActions(self.tools, tool)
        self.canvas.menus[0].clear()
        utils.addActions(self.canvas.menus[0], menu)
        self.menus.edit.clear()
        actions = (  # 用于编辑菜单的动作
            self.actions.magic_wand,
            self.actions.createMode,
            self.actions.createRectangleMode,
            self.actions.createCircleMode,
            self.actions.createLineMode,
            self.actions.createPointMode,
            self.actions.createLineStripMode,
            self.actions.editMode,  # 编辑形状
        )
        utils.addActions(self.menus.edit, actions + (None,) + self.actions.editMenu)  
        # 添加ai按钮
        # utils.addActions(self.tools, [None])  # 分割线
        # utils.addActions(self.tools, self.actions.ai_tools)  # 添加AI相关工具
        utils.addActions(self.ai_tools, self.actions.ai_tools)
        utils.addActions(self.side_bar, self.actions.side_bar)  # 分割线
        utils.addActions(self.edit_tools, self.actions.edit_tools)

    def set_style(self):
        # style
        self.mmstyle = mm.Style()

        self.mmstyle.set_scheme(self, 'photoshop')
        # self.mmstyle.set_scheme(self, 'rainbow')
        # self.mmstyle.frameless(self)

        
    


        



