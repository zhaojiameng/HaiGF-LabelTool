

# import pyqtgraph.examples

# pyqtgraph.examples.run()
import os, sys
from pathlib import Path
sys.path.append(f'{Path(__file__).parent.parent.parent}')

from HaiGF.plugins.pyqtgraph.pyqtgraph.examples import run

run()