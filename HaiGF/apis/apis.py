
# import os, sys
from pathlib import Path
here = Path(__file__).parent

root_path = f'{here.parent.parent}'

# from ..gui_framework.config.enum import Colors
# COLORS = Colors()
from ..gui_framework.config.HGF import HGF
HGF = HGF()


# from ..plugins.hai_tools.PyFlow.Core.NodeBase import NodeBase as HNode


