from math import sqrt
import os.path as osp
import os

import numpy as np

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtSvg

from ..widgets.common.hai_action import HAction


here = osp.dirname(osp.abspath(__file__))


def newIcon(icon):
    icons_dir = osp.join(here, "../icons")
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

    return QtGui.QIcon(osp.join(":/", icons_dir, "%s.png" % icon))


def newButton(text, icon=None, slot=None):
    b = QtWidgets.QPushButton(text)
    if icon is not None:
        b.setIcon(newIcon(icon))
    if slot is not None:
        b.clicked.connect(slot)
    return b


def newAction(
    parent,
    text,
    slot=None,
    shortcut=None,
    icon=None,
    tip=None,
    checkable=False,
    enabled=True,
    checked=False,
):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    # a = HAction(text, parent)
    if icon is not None:
        icon_text = "" if text is None else text.replace(" ", "\n")
        # a.setIconText(text.replace(" ", "\n"))
        a.setIconText(icon_text)
        a.setIcon(newIcon(icon))
        # a.setIcon(icon)
        
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    a.setChecked(checked)
    return a


def addActions(widget, actions):
    """
    给widget添加actions，为None是添加分割线，或添加菜单、或添加action
    """
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif action == "Spacer":
            spacer = QtWidgets.QWidget()
            spacer.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            )
            widget.addWidget(spacer)
        elif isinstance(action, QtWidgets.QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)


def labelValidator():
    return QtGui.QRegExpValidator(QtCore.QRegExp(r"^[^ \t].+"), None)


class struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())


def distancetoline(point, line):
    p1, p2 = line
    p1 = np.array([p1.x(), p1.y()])
    p2 = np.array([p2.x(), p2.y()])
    p3 = np.array([point.x(), point.y()])
    if np.dot((p3 - p1), (p2 - p1)) < 0:
        return np.linalg.norm(p3 - p1)
    if np.dot((p3 - p2), (p1 - p2)) < 0:
        return np.linalg.norm(p3 - p2)
    if np.linalg.norm(p2 - p1) == 0:
        return 0
    return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)


def fmtShortcut(text):
    mod, key = text.split("+", 1)
    return "<b>%s</b>+<b>%s</b>" % (mod, key)