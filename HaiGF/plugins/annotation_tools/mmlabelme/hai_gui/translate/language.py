

def build_language_config(language='English'):
    if language.lower() == 'english':
        return English
    elif language.lower() == 'chinese':
        return Chinese
    else:
        raise NotImplemented(f'build language config error: {language} not implement')


class English:
    __appname__ = 'hai-gui'
    # menu
    menu_file = "&File"
    menu_edit = "&Edit"
    menu_view = "&View"
    menu_ai = "&AI"
    menu_help = "&Help"

    # actions
    # file actions
    open_recent = "Open &Recent"
    quit = "&Quit"
    open_ = "&Open"
    open_dir = "&Open Dir"
    next_img = "&Next Image"
    prev_img = "&Prev Image"
    save = "&Save"
    save_as = "&Save As"
    delete_file = "&Delete File"
    change_output_dir = "&Change Output Dir"
    save_auto = "Save &Automatically"
    save_with_img_data = "Save With Image Data"
    close = "&Close"
    # tips
    quit_tip = "Quit application"
    open_tip = "Open image or label file"
    open_dir_tip = "Open Dir"
    next_img_tip = "Open next (hold Ctl+Shift to copy labels)"
    prev_img_tip = "Open prev (hold Ctl+Shift to copy labels)"
    save_tip = "Save labels to file"
    save_as_tip = "Save labels to a different file"
    delete_file_tip = "Delete current label file"
    change_output_dir_tip = "Change where annotations are loaded/saved"
    save_auto_tip = "Save automatically"
    save_with_img_data_tip = "Save image data in label file"
    close_tip = "Close current file"

    # Edit actions
    magic_wand = 'Magic Wand'
    keep_previous_annotation = "Keep Previous Annotation"
    create_polygons = "Create Polygons"
    create_rectangle = "Create Rectangle"
    create_circle = "Create Circle"
    create_line = "Create Line"
    create_point = "Create Point"
    create_line_strip = "Create LineStrip"
    edit_polygons = "Edit Polygons"
    delete_polygons = "Delete Polygons"
    duplicate_polygons = "Duplicate Polygons"
    copy_polygons = "Copy Polygons"
    paste_polygons = "Paste Polygons"
    undo_last_point = "Undo last point"
    remove_selected_point = "Remove Selected Point"
    undo = "Undo"
    edit_label = "&Edit Label"
    fill_drawing = "Fill Drawing Polygon"
    # Edit tips
    magic_wand_tip = 'Use magic wand to select objects'
    keep_previous_annotation_tip = 'Toggle "keep pevious annotation" mode'
    create_polygons_tip = "Start drawing polygons"
    create_rectangle_tip = "Start drawing rectangles"
    create_circle_tip = "Start drawing circles"
    create_line_tip = "Start drawing lines"
    create_point_tip = "Start drawing points"
    create_line_strip_tip = "Start drawing linestrip. Ctrl+LeftClick ends creation"
    edit_polygons_tip = "Move and edit the selected polygons"
    delete_polygons_tip = "Delete the selected polygons"
    duplicate_polygons_tip = "Create a duplicate of the selected polygons"
    copy_polygons_tip = "Copy selected polygons to clipboard"
    paste_polygons_tip = "Paste copied polygons"
    undo_last_point_tip = "Undo last drawn point"
    remove_selected_point_tip = "Remove selected point from polygon"
    undo_tip = "Undo last add and edit of shape"
    edit_label_tip = "Modify the label of the selected polygon"
    fill_drawing_tip = "Fill polygon while drawing"

    # View actions
    hide_all = "&Hide\nPolygons"
    show_all = "&Show\nPolygons"
    zoom_in = "Zoom &In"
    zoom_out = "Zoom &Out"
    original_size = "&Original size"
    keep_previous_scale = "&Keep Previous Scale"
    fit_window = "&Fit Window"
    fit_width = "Fit &Width"
    brightness_contrast = "&Brightness Contrast"
    # View tips
    hide_all_tip = "Hide all polygons"
    show_all_tip = "Show all polygons"
    zoom_in_tip = "Increase zoom level"
    zoom_out_tip = "Decrease zoom level"
    original_size_tip = "Zoom to original size"
    keep_previous_scale_tip = "Keep previous zoom scale"
    fit_window_tip = "Zoom follows window size"
    fit_width_tip = "Zoom follows window width"
    brightness_contrast_tip = "Adjust brightness and contrast"

    # AI actions
    run_ai = 'Run'
    stop_ai = 'Stop'
    config_ai = 'AI Configurations'
    auto_ai = "Auto AI"
    fusion_label = 'Fusion labelling based on Radar'
    # AI tips
    run_ai_tip = 'Run AI for object detection and tracking in current image'
    stop_ai_tip = 'stop AI'
    config_ai_tip = "AI Configurations"
    auto_ai_tip = "Call AI automatically when load image"
    fusion_label_tip = 'Assist labelling based on fusion of radar image and visual image'

    # Tutorial
    tutorial = "&Tutorial"
    tutorial_tip = "Tutorial"
    license = "&License"
    license_tip = "License"

    # dock
    dock_flags = "Flags"
    dock_label_list = "Label List"
    dock_polygon_labels = "Polygon Labels"
    dock_file_list = "File List"
    dock_mm_list = "MM list"

    # 下级filelist里
    search_filename = "Search Filename"

    # 关于子窗口label_dialog的汉化
    ldiag_class = 'Class'
    ldiag_class_holder = 'Enter Object label'
    ldiag_class_groupid_holder = 'Group ID'
    ldiag_tid = 'Tid'
    ldiag_tid_holder = 'Enter object tracking id'
    ldiag_status = 'Status'
    ldiag_status_holder = 'Enter object status'
    ldiag_status_groupid_holder = 'Group ID'


    # hai
    # sidebar
    resource_manager = "Resource Manager"
    resource_manager_tip = "Open Resource Manager"
    search = "Search"
    search_tip = "Search Algorithms"
    extension = "Extension"
    extension_tip = "Add Algorithm Modules"

    # dock
    manager_dock = "Manager"


class Chinese:
    __appname__ = 'HAI-GUI'
    menu_file = "文件"
    menu_edit = "编辑"
    menu_view = "视图"
    menu_ai = "&AI"
    menu_help = "帮助"

    # File actions
    open_recent = "打开最近的文件"
    quit = "退出"
    open_ = "加载图像..."
    open_dir = "加载文件夹..."
    next_img = "下一张"
    prev_img = "上一张"
    save = "保存"
    save_as = "另存为..."
    delete_file = "删除文件"
    change_output_dir = "修改输出路径..."
    save_auto = "自动保存"
    save_with_img_data = "保存图像数据"
    close = "关闭"
    # file tips
    quit_tip = "退出应用软件"
    open_tip = "打开图像或标注文件"
    open_dir_tip = "加载文件夹下所有图像和标注"
    next_img_tip = "打开下一张图像，(按住 Ctl+Shift 复制标注)"
    prev_img_tip = "打开下一张图像，(按住 Ctl+Shift 复制标注)"
    save_tip = "保存标注到文件"
    save_as_tip = "另存为标注到文件"
    delete_file_tip = "删除当前标注文件"
    change_output_dir_tip = "修改标注文件加载/保存目录"
    save_auto_tip = "切换是否自动保存"
    save_with_img_data_tip = "切换是否在标注文件中保存图像"
    close_tip = "关闭当前文件"

    # 编辑 actions
    magic_wand = '魔棒工具'
    keep_previous_annotation = "继承前一个标注"
    create_polygons = "创建多边形"
    create_rectangle = "创建矩形"
    create_circle = "创建圆形"
    create_line = "创建线"
    create_point = "创建点"
    create_line_strip = "创建线带"
    edit_polygons = "编辑形状"
    delete_polygons = "删除形状"
    duplicate_polygons = "克隆形状"
    copy_polygons = "复制形状"
    paste_polygons = "粘贴形状"
    undo_last_point = "撤销上个点"
    remove_selected_point = "移除选中点"
    undo = "撤销"
    edit_label = "编辑标签"
    fill_drawing = "填充绘制形状"
    # 编辑 tips
    magic_wand_tip = '使用魔棒工具智能选择'
    keep_previous_annotation_tip = '切换是否继承前一个标注'
    create_polygons_tip = "开始绘制多边形"
    create_rectangle_tip = "开始绘制矩形"
    create_circle_tip = "Start drawing circles"
    create_line_tip = "Start drawing lines"
    create_point_tip = "Start drawing points"
    create_line_strip_tip = "Start drawing linestrip. Ctrl+LeftClick ends creation"
    edit_polygons_tip = "Move and edit the selected polygons"
    delete_polygons_tip = "Delete the selected polygons"
    duplicate_polygons_tip = "Create a duplicate of the selected polygons"
    copy_polygons_tip = "Copy selected polygons to clipboard"
    paste_polygons_tip = "Paste copied polygons"
    undo_last_point_tip = "Undo last drawn point"
    remove_selected_point_tip = "Remove selected point from polygon"
    undo_tip = "Undo last add and edit of shape"
    edit_label_tip = "Modify the label of the selected polygon"
    fill_drawing_tip = "Fill polygon while drawing"

    # 视图 actions
    hide_all = "隐藏所有形状"
    show_all = "显示所有形状"
    zoom_in = "缩小"
    zoom_out = "放大"
    original_size = "原始尺寸"
    keep_previous_scale = "保存上一个缩放"
    fit_window = "适应窗口"
    fit_width = "适应宽度"
    brightness_contrast = "亮度/对比度"
    # 视图 tips
    hide_all_tip = "Hide all polygons"
    show_all_tip = "Show all polygons"
    zoom_in_tip = "Increase zoom level"
    zoom_out_tip = "Decrease zoom level"
    original_size_tip = "Zoom to original size"
    keep_previous_scale_tip = "Keep previous zoom scale"
    fit_window_tip = "Zoom follows window size"
    fit_width_tip = "Zoom follows window width"
    brightness_contrast_tip = "Adjust brightness and contrast"

    # AI actions
    run_ai = '运行'
    stop_ai = '停止'
    config_ai = '配置'
    auto_ai = '自动AI检测'
    fusion_label = '融合标注'
    # AI tip
    run_ai_tip = '在当前图像上运行AI'
    stop_ai_tip = '停止AI'
    config_ai_tip = "配置AI"
    auto_ai_tip = "切换是否在加载图像时自动运行AI"
    fusion_label_tip = '基于雷达图像与视觉图像融合的辅助标注'

    # 教程
    tutorial = "教程"
    tutorial_tip = "打开教程"
    license = "证书"
    license_tip = "查看证书和激活"

    # dock
    dock_flags = "标记"
    dock_label_list = "类别列表"
    dock_polygon_labels = "标注列表"
    dock_file_list = "文件列表"
    dock_mm_list = "多模态列表"

    # 下级filelist里
    search_filename = "搜索文件"

    # 关于子窗口label_dialog的汉化
    ldiag_class = '目标类别'
    ldiag_class_holder = '输入类别标签'
    ldiag_class_groupid_holder = '类别分组'
    ldiag_tid = '跟踪ID'
    ldiag_tid_holder = '输入跟踪ID'
    ldiag_status = '目标状态'
    ldiag_status_holder = '输入状态标签'
    ldiag_status_groupid_holder = '状态分组'

    # sidebar
    resource_manager = "算法"
    resource_manager_tip = "打开算法管理器"
    search = "搜索"
    search_tip = "搜索内容"
    extension = "扩展"
    extension_tip = "扩展算法模块"

    manager_dock = "算法管理器"