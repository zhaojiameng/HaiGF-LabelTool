# flake8: noqa

import logging
import sys

# from qtpy import QT_VERSION

# from PySide2 import QT_VERSION
QT_VERSION = ['5']

__appname__ = "hai_gui"

# Semantic Versioning 2.0.0: https://semver.org/
# 1. MAJOR version when you make incompatible API changes;
# 2. MINOR version when you add functionality in a backwards-compatible manner;
# 3. PATCH version when you make backwards-compatible bug fixes.
# __version__ = "1.1.0"  # 关联到标注文件里的内容
from .version import __version__


QT4 = QT_VERSION[0] == "4"
QT5 = QT_VERSION[0] == "5"
del QT_VERSION

PY2 = sys.version[0] == "2"
PY3 = sys.version[0] == "3"
del sys

# from hai_gui.label_file import LabelFile
# from hai_gui import testing
# from hai_gui import utils

from .__main__ import main


# from .hai import hai_client
