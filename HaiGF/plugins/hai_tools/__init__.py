
import os, sys
from pathlib import Path

here = Path(__file__).parent

sys.path.append(f'{here}')  # addn PyFlow 


# 初始化PyFlow，使得其加载预设的node、pin等


from .ai_plugin import AIPlugin


