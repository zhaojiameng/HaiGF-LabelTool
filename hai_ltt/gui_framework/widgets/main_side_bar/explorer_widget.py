
from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from pathlib import Path

from hai_ltt.apis import HGF, root_path, __appname__
from ..common.blue_button import BlueButton
from ..common.hai_msb_widget import HMainSideBarWidget
from ... import utils

import damei as dm

logger = dm.get_logger('explorer_widget')

class ExplorerWidget(HMainSideBarWidget):
    """资源浏览器空间，包含标题、标题工具和内容区域，被放置在MainSideBar中"""
    def __init__(self, parent=None, dir=None, **kwargs):
        super().__init__(parent=parent)
        self.p = parent
        self.dir = dir
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setObjectName('ExplorerWidget')
        
        # 标题和标题工具
        # self.setWindowTitle(self.tr('Explorer'))
        self._title = self.tr('Explorer')
        self._title_actions = self._init_actions()
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
        self.tree = QTreeView()  # 树
        # self.tree.setWindowTitle('title')
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir))
        # self.tree.setHeaderHidden(True)
        self.tree.setColumnWidth(0, 250)

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
