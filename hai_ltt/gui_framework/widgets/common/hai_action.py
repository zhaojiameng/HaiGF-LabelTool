import os.path as osp
import os
from pathlib import Path

from PySide2 import QtGui
from PySide2.QtWidgets import QAction
from PySide2.QtSvg import QSvgRenderer


here = Path(__file__).parent


class HAction(QAction):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self._shortcut = None
        self._tip = None
        self._icon = None
        self._text = None
        self._slot = None

        self._hovered = False

    def get_icon_path(self, icon):
        # icons_dir = osp.join(here, "../../icons")
        icons_dir = f'{here.parent.parent}/icons'
        # print(osp.join(":/", icons_dir, "%s.png" % icon))
        icons = os.listdir(icons_dir)
        if f'{icon}.svg' in icons:
            icon_name = f'{icon}.svg'
        elif f'{icon}.png' in icons:
            icon_name = f'{icon}.png'
        else:
            icon_name = 'unknown.png'
        icon_path = osp.join(icons_dir, icon_name)

        # icon = QtGui.QIcon(icon_path)
        # return icon
        return icon_path

    def newIcon(self, icon, color='Gray'):
        icon_path = self.get_icon_path(icon)
        if icon_path.endswith('.png'):
            icon = QtGui.QIcon(icon_path)
            return icon
        if color == 'Gray':
            print(icon_path)
            renderer = QSvgRenderer()
            renderer.load(icon_path)
            size = renderer.defaultSize()
            image = QtGui.QImage(size, QtGui.QImage.Format_ARGB32)
            image.fill(QtGui.Qt.red)
            painter = QtGui.QPainter(image)
            renderer.render(painter)
            painter.end()
            icon = QtGui.QIcon(QtGui.QPixmap.fromImage(image))
            return icon
        else:
            raise NotImplementedError
        return icon_path

    def setIcon(self, icon, color='Gray'):
        print(f"setIcon: {icon}")
        if isinstance(icon, str):
            icon = self.newIcon(icon, color=color)
        super().setIcon(icon)
        self._icon = icon

    def set_icon(self):
        pass
        # print(self.icon_stem)
        # self._icon = icon
        # icon = utils.newIcon(icon)
        # self.setIcon(icon)

