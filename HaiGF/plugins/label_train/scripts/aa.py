#导入adjust_contrast函数,adjust_brightness函数,adjust_saturation函数
import HaiGF.plugins.label_train.scripts.tool as tool
import cv2
import numpy as np

class ImageProcessor(object):

    def __init__(self):
        pass

    def __call__(self, img):
        funcs = [tool.ImageEnhancement.adjust_brightness, tool.ImageEnhancement.adjust_contrast]
        paramss = [
            {"delta": 10},
            {"factor": 1.5}
        ]
        return self.excutor(img, funcs, paramss)


    def excutor(self, img, funcs=[], paramss=[]):

        for func in funcs:
            params = paramss[funcs.index(func)]
            img = func(img, **params) 
        return img

"""
*表示收集参数，**表示收集关键字参数
*将元组或列表转换为参数列表，**将字典转换为关键字参数
"""