
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from pathlib import Path

from ..title_bar import TitleBarWithAction
from hai_ltt.apis import HGF
from ..blue_button import BlueButton
from hai_ltt.apis import root_path, __appname__

def get_main_side_bar(parent=None, **kwargs):
    return MainSideBar(parent=parent, **kwargs)

class MainSideBar(QtWidgets.QDockWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.mw = parent
        title = kwargs.pop('title', 'Main Side Bar Title')
        self.setWindowTitle(title)

        # 1.标题栏，带有按钮
        self.title_bar = TitleBarWithAction()  # QFrame()
        self.setTitleBarWidget(self.title_bar)
        # 2.默认界面
        default_widget = self.get_example_widget()
        self.setWidget(default_widget)

        self.setupProperty()

    def load(self, title_bar=None, title=None, widget=None):
        """重新加载"""
        if title_bar:
            self.title_bar = title_bar
            self.setTitleBarWidget(title_bar)
        if title:
            self.title_bar.set_title(title)
        if widget:
            self.setWidget(widget)
        # else:
            # widget = ExampleWidget2(parent=self)
        self.setWidget(widget)

    def get_example_widget(self):
        """一个示例页面"""
        return ExampleWidget(parent=self)

    def setupProperty(self):
        self.setMinimumSize(QtCore.QSize(50, 0))


class ExampleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.mw = self.parent.mw
        print(self.parent)

        # 1.标签
        label1 = QLabel(self.tr('Folder not opend.'))
        label1.setFont(HGF.FONT)
        label1.setWordWrap(True)
        label1.setStyleSheet(f"color: {HGF.COLORS.LightBlack};")
        # 2.按钮
        self.button1 = BlueButton(self.tr('Open Folder'), pparent=self)
        self.button1.setObjectName(u'openDirButton2')
        self.button1.clicked.connect(self.on_openDirButton2_clicked)
        self.button1.setMinimumSize(QtCore.QSize(0, 30))
        # button1.setStyleSheet(f"color: {HGF.COLORS.DimGray};")
        # 3.提示
        label2 = QLabel(self.tr('Please open a folder to start.'))
        label2.setFont(HGF.FONT)
        label2.setWordWrap(True)
        label2.setStyleSheet(f"color: {HGF.COLORS.LightBlack};")
        # x.spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(label1)
        layout.addWidget(self.button1)
        layout.addWidget(label2)
        layout.addSpacerItem(spacer)
        self.setLayout(layout)
    
    @QtCore.Slot()
    def on_openDirButton2_clicked(self):
        # print('openDirButton2 clicked')
        defaultOpenDirPath = self.mw.settings.value('lastDirPath', root_path)

        selected_dir = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self,
                self.tr("%s - Open Directory") % __appname__,
                defaultOpenDirPath,
                QtWidgets.QFileDialog.ShowDirsOnly
                | QtWidgets.QFileDialog.DontResolveSymlinks,
            )
        )
        self.mw.load_file_or_dir(dir=selected_dir)

class ExampleWidget2(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 文件系统
        self.model = QFileSystemModel()
        self.model.setRootPath(f"/")

        # 树
        self.tree = QTreeView()
        self.tree.setWindowTitle('title')
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(f"{Path.home()}"))
        # self.tree.setHeaderHidden(True)
        self.tree.setColumnWidth(0, 250)

        self.layout.addWidget(self.tree)


