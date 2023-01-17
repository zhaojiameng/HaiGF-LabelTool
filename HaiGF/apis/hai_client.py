

import os, sys
from pathlib import Path


try:
    import hai_client
except ImportError:
    path = f'{Path(__file__).parent.parent.parent.parent}/hai-client'
    sys.path.insert(0, path)
    import hai_client
    sys.path.pop(0)