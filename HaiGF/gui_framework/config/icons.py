import os
import os.path as osp
from pathlib import Path
from PySide2 import QtGui
from PySide2.QtGui import QIcon

here = Path(__file__).parent

class Icons(object):

    def __init__(self) -> None:
        pass

    def __call__(self, icon_name: str) -> QIcon:
        if hasattr(self, icon_name):
            return super().__getattribute__(icon_name)
        else:  # 创建新的Icon
            icon = self.new_icon(icon_name)
            self.__setattr__(icon_name, icon)
            return icon


    def new_icon(self, icon: str):
        icons_dir = f'{here.parent}/icons'
        # print(osp.join(":/", icons_dir, "%s.png" % icon))
        icons = os.listdir(icons_dir)
        if f'{icon}.svg' in icons:
            icon_name = f'{icon}.svg'
        elif f'{icon}.png' in icons:
            icon_name = f'{icon}.png'
        else:
            icon_name = 'unknown.png'
        icon_path = osp.join(icons_dir, icon_name)

        icon = QtGui.QIcon(icon_path)
        return icon