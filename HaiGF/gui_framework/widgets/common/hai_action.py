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
    """
    This is a wrapper for QAction.

    :param text: Text to be displayed in menu items. It will be shown if icon is None.
    :param parent: Parent widget, usually `mw`.
    :param optional slot: Slot function to be called when the action is triggered.
    :param soptional hortcut: Shortcut key to trigger the action.
    :param optional icon: Icon to be displayed in menu items, only icon will be shown if setted.
    :param optional tip: Tooltip to be displayed when mouse hover on the action.
    :param optional checkable: Whether the action is checkable, `False` by default.
    :param optional enabled: Whether the action is enabled, `True` by default.
    :param optional checked: Whether the action is checked, `False` by default.
    """
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




    


