
from .gui_framework import FrameworkMainWindow
# from .apis.apis import root_path

from .__main__ import main

import damei as dm
import logging
logger = dm.get_logger('hai_ltt')
logger.setLevel(logging.DEBUG)
