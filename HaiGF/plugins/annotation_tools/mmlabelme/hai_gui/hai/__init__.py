
import os, sys
from pathlib import Path


try:
    import hai_client
except ImportError:
    path = f'{Path(__file__).parent.parent.parent.parent}/hai-client'
    sys.path.insert(0, path)
    import hai_client
    sys.path.pop(0)

# print(hai_client.__file__)
# from hai_client import HaiClient
# ip = 'localhost'
# port = 9999
# hai = hai_client.HAIClient(ip, port)

