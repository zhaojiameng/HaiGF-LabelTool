

from HaiGF.apis import HGF
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class HMenuBar(QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        self.drag = False
        self.old_pos = QPoint(0, 0)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        frame = QFrame(self)
        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(10, 10, 10, 10)
        frame_layout.setSpacing(10)
        
        # 加载logo
        self.logo = QLabel()
        self.logo.setPixmap(HGF.ICONS.get('ai').pixmap(HGF.LOGO_SIZE, HGF.LOGO_SIZE))
        frame_layout.addWidget(self.logo)
        
        # 菜单栏
        frame_layout.addWidget(HMenuBar2(self))

        # 添加空间，使得菜单栏靠左
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame_layout.addWidget(spacer)

        # 添加按钮minimum button, maximum button, close button
        min_button, max_button, close_button = self.create_min_max_close_button()
        frame_layout.addWidget(min_button)
        frame_layout.addWidget(max_button)
        frame_layout.addWidget(close_button)

        frame.setStyleSheet(HGF.TITLE_BAR_CSS)
        frame.setLayout(frame_layout)
        
        layout.addWidget(frame)
        self.setLayout(layout)
        # 居中对齐
        frame_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def create_min_max_close_button(self):
        # minimum button
        min_button = QPushButton(self)
        min_button.setIcon(HGF.ICONS.get('minus'))
        # min_button.setFixedSize(16, 16)
        min_button.setStyleSheet('background-color: rgb(255, 255, 255);')
        min_button.setFlat(True)
        min_button.clicked.connect(self.p.showMinimized)

        # maximum button
        max_button = QPushButton(self)
        max_button.setIcon(HGF.ICONS.get('square-small'))
        # max_button.setFixedSize(16, 16)
        max_button.setStyleSheet('background-color: rgb(255, 255, 255);')
        max_button.setFlat(True)
        max_button.clicked.connect(self.p.showMaximized)

        # close button
        close_button = QPushButton(self)
        close_button.setIcon(HGF.ICONS.get('close'))
        # close_button.setFixedSize(16, 16)
        close_button.setStyleSheet('background-color: rgb(255, 255, 255);')
        close_button.setFlat(True)
        close_button.clicked.connect(self.p.close)

        return min_button, max_button, close_button

        


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print('press')

        # 按住鼠标左键移动窗口
        if event.button() == Qt.LeftButton:
            self.drag = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self.drag:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.p.move(self.p.x() + delta.x(), self.p.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.drag = False

class HMenuBar2(QMenuBar):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        self.setup_menu()

        # side plolicy minimum
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # self.setStyleSheet('background-color: rgb(255, 255, 255);')
        # 设置居中对齐
        # self.layout().setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


    def setup_menu(self):
        file_menu = self.addMenu(self.tr("&File"))
        edit_menu = self.addMenu(self.tr("Edit"))
        run_menu = self.addMenu(self.tr("Run"))
        view_menu = self.addMenu(self.tr("View"))
        help_menu = self.addMenu(self.tr("Help"))


        # 文件菜单的动作
        # new_action = file_menu.addAction("新建")
        # open_action = file_menu.addAction("打开")
        # save_action = file_menu.addAction("保存")
        # save_as_action = file_menu.addAction("另存为")
        # file_menu.addSeparator()
        # exit_action = file_menu.addAction("退出")
        new_action = file_menu.addAction(self.tr("New"))
        open_action = file_menu.addAction(self.tr("Open"))
        save_action = file_menu.addAction(self.tr("Save"))
        save_as_action = file_menu.addAction(self.tr("Save as"))
        file_menu.addSeparator()
        exit_action = file_menu.addAction(self.tr("Exit"))

        # 编辑菜单的动作
        undo_action = edit_menu.addAction(self.tr("Undo"))
        redo_action = edit_menu.addAction(self.tr("Redo"))
        edit_menu.addSeparator()
        cut_action = edit_menu.addAction(self.tr("Cut"))
        copy_action = edit_menu.addAction(self.tr("Copy"))
        paste_action = edit_menu.addAction(self.tr("Paste"))
        delete_action = edit_menu.addAction(self.tr("Delete"))
        edit_menu.addSeparator()
        select_all_action = edit_menu.addAction(self.tr("Select all"))
        find_action = edit_menu.addAction(self.tr("Find"))
        replace_action = edit_menu.addAction(self.tr("Replace"))

        # 运行菜单的动作
        run_action = run_menu.addAction(self.tr("Run"))
        run_action.setShortcut("F5")
        run_menu.addSeparator()
        run_in_terminal_action = run_menu.addAction(self.tr("Run in terminal"))
        run_in_terminal_action.setShortcut("Ctrl+Shift+R")

        # 视图菜单的动作
        full_screen_action = view_menu.addAction(self.tr("Full screen"))
        full_screen_action.setShortcut("F11")
        view_menu.addSeparator()
        show_toolbar_action = view_menu.addAction(self.tr("Show panel widget"))
        show_toolbar_action.setShortcut("Ctrl+Shift+p")

        # 帮助菜单的动作
        about_action = help_menu.addAction(self.tr("About"))
        about_action.setShortcut("F1")
        # help_menu.addSeparator()


        self.addAction(file_menu.menuAction())
        self.addAction(edit_menu.menuAction())
        self.addAction(run_menu.menuAction())
        self.addAction(view_menu.menuAction())
        self.addAction(help_menu.menuAction())
