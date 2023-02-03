import functools
# from qtpy.QtCore import Qt
from PySide2.QtCore import Qt
from .. import newAction

class struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def create_actions(self, zoom):
    # Actions
    lngg = self.lngg
    action = functools.partial(newAction, self)  # 一个函数，函数先创建Qaction类，再进行设置
    shortcuts = self._config["shortcuts"]
    
    # <1> File
    quit = action(  # 返回退出动作，这个类, 1
        self.tr(lngg.quit),  # text名字
        self.close,  # 槽slot, 这里直接就绑定槽了
        shortcuts["quit"],  # 快捷键 Ctrl+Q
        "quit",  # 图标icon
        self.tr(lngg.quit_tip), )  # tip提示
    open_ = action( # 2
        self.tr(lngg.open_),
        self.openFile,
        shortcuts["open"],
        "open",
        self.tr(lngg.open_tip),
    )
    opendir = action( # 3
        self.tr(lngg.open_dir),
        self.openDirDialog,
        shortcuts["open_dir"],
        "open",
        self.tr(lngg.open_dir_tip),
    )
    openNextImg = action( # 4
        self.tr(lngg.next_img),
        self.openNextImg,
        shortcuts["open_next"],
        "next",
        self.tr(lngg.next_img_tip),
        enabled=False,
    )
    openPrevImg = action( # 5
        self.tr(lngg.prev_img),
        self.openPrevImg,
        shortcuts["open_prev"],
        "prev",
        self.tr(lngg.prev_img_tip),
        enabled=False,
    )
    save = action( # 6
        self.tr(lngg.save),
        self.saveFile,
        shortcuts["save"],
        "save",
        self.tr(lngg.save_tip),
        enabled=False,
    )
    saveAs = action( # 7
        self.tr(lngg.save_as),
        self.saveFileAs,
        shortcuts["save_as"],
        "save-as",
        self.tr(lngg.save_as_tip),
        enabled=False,
    )

    deleteFile = action( # 8
        self.tr(lngg.delete_file),
        self.deleteFile,
        shortcuts["delete_file"],
        "delete",
        self.tr(lngg.delete_file_tip),
        enabled=False,
    )

    changeOutputDir = action( # 9
        self.tr(lngg.change_output_dir),
        slot=self.changeOutputDirDialog,
        shortcut=shortcuts["save_to"],
        icon="open",
        tip=self.tr(lngg.change_output_dir_tip),
    )

    saveAuto = action( # 10
        text=self.tr(lngg.save_auto),
        slot=lambda x: self.actions.saveAuto.setChecked(x),
        icon="save",
        tip=self.tr(lngg.save_auto_tip),
        checkable=True,
        enabled=True,
    )
    saveAuto.setChecked(self._config["auto_save"])

    saveWithImageData = action(  # 11
        text=lngg.save_with_img_data,
        slot=self.enableSaveImageWithData,
        tip=lngg.save_with_img_data_tip,
        checkable=True,
        checked=self._config["store_data"],
    )

    close = action(  # 12
        lngg.close,
        self.closeFile,
        shortcuts["close"],
        "close",
        lngg.close_tip,
    )

    # <2> Editc
    # 魔棒
    magic_wand = action(
        self.tr(lngg.magic_wand),
        # self.slot_magic_wand,
        lambda: self.toggleDrawMode(False, createMode="magic_wand"),
        None,  # 快捷键
        'magic_wand',
        self.tr(lngg.magic_wand_tip),
        checked=True,
    )

    # 切换，保持前一帧标注
    toggle_keep_prev_mode = action(  # 13
        self.tr(lngg.keep_previous_annotation),
        self.toggleKeepPrevMode,
        shortcuts["toggle_keep_prev_mode"],
        None,
        self.tr(lngg.keep_previous_annotation_tip),
        checkable=True, )
    toggle_keep_prev_mode.setChecked(self._config["keep_prev"])

    # 新建多边形  # 14
    createMode = action(
        self.tr(lngg.create_polygons),
        lambda: self.toggleDrawMode(False, createMode="polygon"),
        shortcuts["create_polygon"],
        "objects",
        self.tr(lngg.create_polygons_tip),
        enabled=False,
    )

    # 新建矩形  # 15
    createRectangleMode = action(
        self.tr(lngg.create_rectangle),
        lambda: self.toggleDrawMode(False, createMode="rectangle"),
        shortcuts["create_rectangle"],
        "objects",
        self.tr(lngg.create_rectangle_tip),
        enabled=False,
    )

    # 新建圆  # 16
    createCircleMode = action(
        self.tr(lngg.create_circle),
        lambda: self.toggleDrawMode(False, createMode="circle"),
        shortcuts["create_circle"],
        "objects",
        self.tr(lngg.create_circle_tip),
        enabled=False,
    )
    # 新建线 17
    createLineMode = action(
        self.tr(lngg.create_line),
        lambda: self.toggleDrawMode(False, createMode="line"),
        shortcuts["create_line"],
        "objects",
        self.tr(lngg.create_line_tip),
        enabled=False,
    )
    # 新建点 18
    createPointMode = action(
        self.tr(lngg.create_point),
        lambda: self.toggleDrawMode(False, createMode="point"),
        shortcuts["create_point"],
        "objects",
        self.tr(lngg.create_point_tip),
        enabled=False,
    )
    # 新建线带 19
    createLineStripMode = action(
        self.tr(lngg.create_line_strip),
        lambda: self.toggleDrawMode(False, createMode="linestrip"),
        shortcuts["create_linestrip"],
        "objects",
        self.tr(lngg.create_line_strip_tip),
        enabled=False,
    )
    # 编辑模式，编辑多边形 20
    editMode = action(
        self.tr(lngg.edit_polygons),
        self.setEditMode,
        shortcuts["edit_polygon"],
        "edit",
        self.tr(lngg.edit_polygons_tip),
        enabled=False,
    )

    delete = action( # 21
        self.tr(lngg.delete_polygons),
        self.deleteSelectedShape,
        shortcuts["delete_polygon"],
        "cancel",
        self.tr(lngg.delete_polygons_tip),
        enabled=False,
    )
    duplicate = action(  # 22
        self.tr(lngg.duplicate_polygons),
        self.duplicateSelectedShape,
        shortcuts["duplicate_polygon"],
        "copy",
        self.tr(lngg.duplicate_polygons_tip),
        enabled=False,
    )
    copy = action(  # 23
        self.tr(lngg.copy_polygons),
        self.copySelectedShape,
        shortcuts["copy_polygon"],
        "copy_clipboard",
        self.tr(lngg.copy_polygons_tip),
        enabled=False,
    )
    paste = action(  # 24
        self.tr(lngg.paste_polygons),
        self.pasteSelectedShape,
        shortcuts["paste_polygon"],
        "paste",
        self.tr(lngg.paste_polygons_tip),
        enabled=False,
    )
    # 撤销上个点 25
    undoLastPoint = action(
        self.tr(lngg.undo_last_point),
        self.canvas.undoLastPoint,
        shortcuts["undo_last_point"],
        "undo",
        self.tr(lngg.undo_last_point_tip),
        enabled=False,
    )
    # 移除点 26
    removePoint = action(
        text=lngg.remove_selected_point,
        slot=self.removeSelectedPoint,
        shortcut=shortcuts["remove_selected_point"],
        icon="edit",
        tip=lngg.remove_selected_point_tip,
        enabled=False,
    )
    # 撤销上次增加或编辑的形状 27
    undo = action(
        self.tr(lngg.undo),
        self.undoShapeEdit,
        shortcuts["undo"],
        "undo",
        self.tr(lngg.undo_tip),
        enabled=False,
    )
    # 编辑 28
    edit = action(
        self.tr(lngg.edit_label),
        self.editLabel,
        shortcuts["edit_label"],
        "edit",
        self.tr(lngg.edit_label_tip),
        enabled=False,
    )

    # <3> View
    # 隐藏所有多边形 29
    hideAll = action(
        self.tr(lngg.hide_all),
        functools.partial(self.togglePolygons, False),
        icon="eye",
        tip=self.tr(lngg.hide_all_tip),
        enabled=False,
    )
    # 显示所有多边形 30
    showAll = action(
        self.tr(lngg.show_all),
        functools.partial(self.togglePolygons, True),
        icon="eye",
        tip=self.tr(lngg.show_all_tip),
        enabled=False,
    )

    # 缩小 31
    zoomIn = action(
        self.tr(lngg.zoom_in),
        functools.partial(self.addZoom, 1.1),
        shortcuts["zoom_in"],
        "zoom-in",
        self.tr(lngg.zoom_in_tip),
        enabled=False,
    )
    zoomOut = action( # 32
        self.tr(lngg.zoom_out),
        functools.partial(self.addZoom, 0.9),
        shortcuts["zoom_out"],
        "zoom-out",
        self.tr(lngg.zoom_out_tip),
        enabled=False,
    )
    zoomOrg = action( # 33
        self.tr(lngg.original_size),
        functools.partial(self.setZoom, 100),
        shortcuts["zoom_to_original"],
        "zoom",
        self.tr(lngg.original_size_tip),
        enabled=False,
    )
    keepPrevScale = action( # 34
        self.tr(lngg.keep_previous_scale),
        self.enableKeepPrevScale,
        tip=self.tr(lngg.keep_previous_scale_tip),
        checkable=True,
        checked=self._config["keep_prev_scale"],
        enabled=True,
    )
    # 适应窗口
    fitWindow = action( # 35
        self.tr(lngg.fit_window),
        self.setFitWindow,
        shortcuts["fit_window"],
        "fit-window",
        self.tr(lngg.fit_window_tip),
        checkable=True,
        enabled=False,
    )
    fitWidth = action( # 36
        self.tr(lngg.fit_width),
        self.setFitWidth,
        shortcuts["fit_width"],
        "fit-width",
        self.tr(lngg.fit_width_tip),
        checkable=True,
        enabled=False,
    )
    brightnessContrast = action( # 37
        lngg.brightness_contrast,
        self.brightnessContrast,
        None,
        "color",
        lngg.brightness_contrast_tip,
        enabled=False,
    )
    fill_drawing = action( # 38
        self.tr(lngg.fill_drawing),
        self.canvas.setFillDrawing,
        None,
        "color",
        self.tr(lngg.fill_drawing_tip),
        checkable=True,
        enabled=True,
    )
    fill_drawing.trigger()

    # <4> AI模块的action
    run_ai = action( # 39
        self.tr(lngg.run_ai),
        self.run_ai,  # 槽
        shortcuts['run_ai'],  # 快捷键
        icon='run_ai',
        tip=self.tr(lngg.run_ai_tip),
        checkable=False,
        enabled=True,
        checked=False,
    )
    stop_ai = action( # 40
        self.tr(lngg.stop_ai),
        self.stop_ai,
        shortcuts['stop_ai'],
        icon='stop_ai',
        tip=self.tr(lngg.auto_ai_tip),
        checkable=False,
        enabled=False,
    )
    configure_ai = action( # 41
        self.tr(lngg.config_ai),
        None,
        shortcut=None,
        icon='configure_ai',
        tip=self.tr(lngg.config_ai_tip),
        enabled=True,
    )
    auto_ai = action( # 42
        text=self.tr(lngg.auto_ai),
        slot=self.enableAutoAI,
        shortcut=shortcuts['auto_ai'],
        icon=None,
        tip=self.tr(lngg.auto_ai_tip),
        checkable=True,
        enabled=True,
        checked=self._config["ai"]["auto_ai"],

    )
    fusion_label = action( # 43
        text=self.tr(lngg.fusion_label),
        # 　slot=self.fusion_label,
        slot=self.test_print,
        shortcut=shortcuts['fusion_label'],
        icon="radar",
        tip=self.tr(lngg.fusion_label_tip),
        checkable=True,
        enabled=True,
        checked=self._config["ai"]["fusion_label"],
    )

    # <5> Help 
    help = action( # 44
        self.tr(lngg.tutorial),
        self.tutorial,
        icon="help",
        tip=self.tr(lngg.tutorial_tip),
    )
    license = action( # 45
        self.tr(lngg.license),
        self.license,
        icon="license",
        tip=self.tr(lngg.license_tip)
    )

    # <6> side bar
    resource_manager = action(
        self.tr(lngg.resource_manager),
        self.resource_manager,
        icon="resource_manager",
        tip=self.tr(lngg.resource_manager_tip),
    )
    search = action(
        self.tr(lngg.search),
        self.search,
        icon="search",
        tip=self.tr(lngg.search_tip),
    )   
    extension = action(
        self.tr(lngg.extension),
        self.extension,
        icon="extension",
        tip=self.tr(lngg.extension_tip),
    )


    # Group zoom controls into a list for easier toggling.
    zoomActions = (
        self.zoomWidget,
        zoomIn,
        zoomOut,
        zoomOrg,
        fitWindow,
        fitWidth,
    )
    self.zoomMode = self.FIT_WINDOW
    fitWindow.setChecked(Qt.Checked)
    self.scalers = {
        self.FIT_WINDOW: self.scaleFitWindow,
        self.FIT_WIDTH: self.scaleFitWidth,
        # Set to one to scale to 100% when loading files.
        self.MANUAL_ZOOM: lambda: 1,
    }


    # Store actions for further handling.
    actions = struct(
        saveAuto=saveAuto,
        saveWithImageData=saveWithImageData,
        changeOutputDir=changeOutputDir,
        save=save,
        saveAs=saveAs,
        quit=quit,
        open=open_,
        opendir=opendir,
        close=close,
        deleteFile=deleteFile,
        toggleKeepPrevMode=toggle_keep_prev_mode,
        delete=delete,
        edit=edit,
        duplicate=duplicate,
        copy=copy,
        paste=paste,
        undoLastPoint=undoLastPoint,
        undo=undo,
        removePoint=removePoint,
        createMode=createMode,
        hideAll=hideAll,
        showAll=showAll,
        editMode=editMode,
        magic_wand=magic_wand,
        createRectangleMode=createRectangleMode,
        createCircleMode=createCircleMode,
        createLineMode=createLineMode,
        createPointMode=createPointMode,
        createLineStripMode=createLineStripMode,
        zoom=zoom,
        zoomIn=zoomIn,
        zoomOut=zoomOut,
        zoomOrg=zoomOrg,
        keepPrevScale=keepPrevScale,
        fitWindow=fitWindow,
        fitWidth=fitWidth,
        brightnessContrast=brightnessContrast,
        fill_drawing=fill_drawing,
        zoomActions=zoomActions,
        openNextImg=openNextImg,
        openPrevImg=openPrevImg,
        fileMenuActions=(open_, opendir, save, saveAs, close, quit),
        run_ai=run_ai,
        stop_ai=stop_ai,
        configure_ai=configure_ai,
        auto_ai=auto_ai,
        fusion_label=fusion_label,
        help=help,
        license=license,
        resource_manager=resource_manager,
        search=search,
        extension=extension,
        tool=(),
        # XXX: need to add some actions here to activate the shortcut
        editMenu=(
            edit,  # 编辑标签，
            duplicate,
            delete,
            None,
            undo,
            undoLastPoint,
            None,
            removePoint,
            None,
            toggle_keep_prev_mode,
        ),
        # menu shown at right click
        menu=(  # 对应右键菜单
            createMode,
            createRectangleMode,
            createCircleMode,
            createLineMode,
            createPointMode,
            createLineStripMode,
            editMode,
            edit,
            duplicate,
            copy,
            paste,
            delete,
            undo,
            undoLastPoint,
            removePoint,
        ),
        onLoadActive=(
            close,
            createMode,
            createRectangleMode,
            createCircleMode,
            createLineMode,
            createPointMode,
            createLineStripMode,
            editMode,
            brightnessContrast,
        ),
        onShapesPresent=(saveAs, hideAll, showAll),
        ai=(
            run_ai,
            stop_ai,
            configure_ai,
            auto_ai,
            fusion_label,
        ),
        side_bar=(
            resource_manager,
            search,
            extension,
        ),
        edit_tools=(  # 编辑工具
            magic_wand,
            createMode,
            createRectangleMode,
            createCircleMode,
            createLineMode,
            createPointMode,
            createLineStripMode,
            editMode,  # 编辑形状
        ),
    )

    return actions