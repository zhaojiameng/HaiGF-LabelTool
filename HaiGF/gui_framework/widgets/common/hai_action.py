import os.path as osp
import os
from pathlib import Path

import cv2
import numpy as np
from PySide2.QtGui import *
from PySide2.QtWidgets import QAction
from PySide2.QtSvg import QSvgRenderer

from ...utils import newIcon
from HaiGF.utils import general


here = Path(__file__).parent


class HAction(QAction):
    def __init__(self, text, parent, 
                slot=None, 
                shortcut=None,
                icon=None,
                tip=None,
                checkable=False,
                enabled=True,
                checked=False,):
        super().__init__(text, parent)

        if icon is not None:
            icon_text = "" if text is None else text.replace(" ", "\n")
            self.setIconText(icon_text)
            self.setIcon(newIcon(icon))
        
        if shortcut:
            if isinstance(shortcut, (list, tuple)):
                self.setShortcuts(shortcut)
            else:
                self.setShortcut(shortcut)
        if tip is not None:
            self.setToolTip(tip)
            self.setStatusTip(tip)
        if slot is not None:
            self.triggered.connect(slot)
        if checkable:
            self.setCheckable(True)
        self.setEnabled(enabled)
        self.setChecked(checked)




    


