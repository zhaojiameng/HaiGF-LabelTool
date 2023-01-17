

import os, sys
from pathlib import Path


try:
    import HaiClient
except ImportError:
    path = f'{Path(__file__).parent.parent.parent.parent}/hai-client'
    sys.path.insert(0, path)
    import HaiClient
    sys.path.pop(0)