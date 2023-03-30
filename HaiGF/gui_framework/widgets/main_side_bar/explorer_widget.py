import os
from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from pathlib import Path

from HaiGF.apis import HGF, root_path, __appname__
from ..common.blue_button import BlueButton
from ..common.hai_msb_widget import HMainSideBarWidget
from ... import utils

import damei as dm

logger = dm.get_logger('explorer_widget')

class ExplorerWidget(HMainSideBarWidget):
    """资源浏览器空间，包含标题、标题工具和内容区域，被放置在MainSideBar中"""
    def __init__(self, parent=None, dir=None, **kwargs):
        super().__init__(parent=parent)
        self.p = parent  # mw
        self.dir = dir
        self.tree = None
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setObjectName('ExplorerWidget')
        
        # 标题和标题工具
        # self.setWindowTitle(self.tr('Explorer'))
        self._title = self.tr('Explorer')
        self._title_actions = self._init_actions()
        self.setStyleSheet(HGF.MAIN_SIDE_BAR_CSS)
        self.load()

    def set_dir(self, dir):
        self.dir = dir

    def load_default(self):
        # 1.标签
        label1 = QLabel(self.tr('Folder not opend.'))
        label1.setFont(HGF.FONT)
        label1.setWordWrap(True)
        label1.setStyleSheet(f"color: {HGF.COLORS.LightBlack};")
        # 2.按钮
        self.button1 = BlueButton(self.tr('Open Folder'), pparent=self)
        self.button1.setObjectName(u'openDirButton2')
        self.button1.clicked.connect(self.on_openDirButton2_clicked)
        self.button1.setMinimumSize(QSize(0, 30))
        # button1.setStyleSheet(f"color: {HGF.COLORS.DimGray};")
        # 3.提示
        label2 = QLabel(self.tr('Please open a folder to start.'))
        label2.setFont(HGF.FONT)
        label2.setWordWrap(True)
        label2.setStyleSheet(f"color: {HGF.COLORS.LightBlack};")
        # 4.spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # # x.spacer
        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addWidget(label1)
        self.layout().addWidget(self.button1)
        self.layout().addWidget(label2)
        # self.layout().addSpacerItem(spacer)
        self.layout().addWidget(spacer)

    def load(self):
        """加载，如果为空，则显示默认界面"""
        dir = self.dir
        # 清空layout
        for i in reversed(range(self.layout().count())):
            w = self.layout().itemAt(i).widget()
            if w is not None:
                w.setParent(None)
            # self.layout().itemAt(i).widget().setParent(None)
        if dir is None:
            self.load_default()
        else:
            self.load_explorer_tree(dir)

    def load_explorer_tree(self, dir):
        """根据路径加载文件夹"""
        # print('load_dir', dir)
        # 文件系统
        self.model = QFileSystemModel()
        self.model.setRootPath(f"/")
        self.tree = HTreeView(self)  # 树
        # self.tree.setWindowTitle('title')
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir))
        
        self.layout().addWidget(self.tree)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
    
    @QtCore.Slot()
    def on_openDirButton2_clicked(self):
        # print('openDirButton2 clicked')
        defaultOpenDirPath = self.p.settings.value('lastDirPath', root_path)

        selected_dir = str(
            QFileDialog.getExistingDirectory(
                self,
                self.tr("%s - Open Directory") % __appname__,
                defaultOpenDirPath,
                QFileDialog.ShowDirsOnly
                | QFileDialog.DontResolveSymlinks,
            )
        )
        self.p.load_file_or_dir(dir=selected_dir)

    def _init_actions(self):
        action = utils.newAction(
                parent=self,
                text='Explorer action',
                icon='more',)
        return [action]



class HTreeView(QTreeView):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.p = parent  # explorer widget
        self.setColumnWidth(0, 250)
        # self.setHeaderHidden(True)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)
        # self.headerItem().setText(0, "1")
        # self.header().setVisible(False)

    def mouseDoubleClickEvent(self, event):
        """
        双击事件
        """
        # 如果双击文件，则打开文件
        index = self.indexAt(event.pos())
        if index.isValid():
            file_path = self.model().filePath(index)
            # print('file_path', file_path)
            if os.path.isfile(file_path):
                self.file_duble_clicked(file_path)
                
            elif os.path.isdir(file_path):  # 如果是文件夹
                logger.info(f'Folder double clicked: {file_path}')
                pass
                # self.p.load_file_or_dir(dir=file_path)

    def cope_pre_button(self):
        """ 返回上一张图片的路径 """
        if self.current_index is not None:
            self.current_index =  self.current_index.model().index(self.current_index.row() - 1, 0, self.current_index.parent()) if self.current_index.row() > 0 else self.current_index
            if self.current_index.isValid():
                self.file_duble_clicked(self.model().filePath(self.current_index))

    def cope_pro_button(self):
        """ 返回下一张图片的路径 """
        if self.current_index is not None:
            self.current_index =  self.current_index.model().index(self.current_index.row() + 1, 0, self.current_index.parent()) if self.current_index.row() < self.current_index.model().rowCount(self.current_index.parent()) - 1 else self.current_index
            if self.current_index.isValid():
                self.file_duble_clicked(self.model().filePath(self.current_index))

    def on_context_menu(self):
        print('on_context_menu')


    def file_duble_clicked(self, file_path):
        """
        Deal with file double clicked event.
        """
        mw = self.p.p

        if file_path.endswith('.py'):
            plg  = mw.plugins['PyEditorPlugin']
            plg.open_file(file_path)
            raise NotImplementedError('TODO open .py file')
        elif self.is_image_file(file_path):  # if is image file
            #返回文件的index
            self.current_index = self.model().index(file_path)
            #根据路径返回QModelIndex
            plg = mw.plugins['AnnoPlugin']
            plg.open_image_file(file_path)
            lat = mw.plugins['AntrainPlugin']
            lat.open_image_file(file_path)

        pass

    
    def is_image_file(self, file_path):
        """判断是否是图片文件"""
        return file_path.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))