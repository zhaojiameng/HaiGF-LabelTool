"""
用pyside2-lupdate来生成ts文件，用于翻译界面
使用方法：
    1. python gen_ts.py, 生成的ts文件在hai_ltt/gui_framework/translate/translate_zh_CN.ts
    2. 打开Linguist软件，打开translate_zh_CN.ts文件，手动翻译，发布为translate_zh_CN.qm文件
    3. 程序启动时，自动加载translate_zh_CN.qm文件，即可显示翻译后的界面
"""

import os
import sys
from pathlib import Path
here = Path(__file__).parent

def run():
    # 1.获取所有py文件
    root_path = f'{here.parent}/hai_ltt'
    py_files = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    # 2.生成ts文件
    print(py_files, len(py_files))

    ts_file = f'{here.parent}/hai_ltt/gui_framework/translate/translate_zh_CN.ts'
    cmd = f'pyside2-lupdate {" ".join(py_files)} -ts {ts_file} '
    print(cmd)
    os.system(cmd)
    # ts_file = os.path.join(root_path, 'gui_framework

if __name__ == '__main__':
    run()