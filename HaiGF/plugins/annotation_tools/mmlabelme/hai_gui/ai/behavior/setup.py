"""
命令：python setup.py build_ext --inplace
把.py源码编译成.so文件，并且删除.py源码
"""

import os
from distutils.core import setup

from pathlib import Path
from Cython.Build import cythonize

pys = ['classifier/classifier.py', 'detector/detector.py', 'poser/poser.py', 'tracker/tracker.py',
       'classifier/fallen_detection.py']

# check
pys = [x for x in pys if os.path.exists(x)]

print(f'转换：{pys}')

setup(name='behavior app',
      ext_modules=cythonize(pys))

# 删除
if len(pys) >= 1:
    ipt = input(f'\nDo you want to delete source files: {pys}\n delete? [Yes]/no:  ')
    if ipt in ['Y', 'Yes', 'yes', 'YES', 'y']:
        for py in pys:
            c_file = f'{Path(py).parent}/{Path(py).stem}.c'
            print(f'delete: {py} {c_file}')
            os.system(f'rm {py}')
            os.system(f'rm {c_file}')
    else:
        print('Did not delete anything.')
