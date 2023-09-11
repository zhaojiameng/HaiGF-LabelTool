import base64
import json
import requests
import numpy as np
import os
import matplotlib.pyplot as plt
import hai


def seg_via_sam(input_points, input_labels, input_boxes, img=None):
    input_points = input_points if len(input_points) > 0 else None
    input_labels = input_labels if len(input_labels) > 0 else None
    input_boxes = input_boxes if len(input_boxes) > 0 else None
    masks_list = hai.Models.inference(
        model='meta/segment_anything_model',  # 指定可用模型名字
        api_key='Hi-USdbJhVVGOezXmeUaFEDPgxhEbAWEydniGIArQTNrPejzpQ',  # 输入hepai_api_key
        img = img,  # 输入图片路径或cv2读取的图片
        input_points = input_points,  # 点提示，格式为[[x1,y1],[x2,y2],...] 
        input_labels = input_labels,  # 点提示对应的标签，0代表背景点，1代表前景点，格式为[0, 1, ...], 需要与input_points一一对应，如不提供默认全为前景点
        input_boxes = input_boxes,  # 框提示，格式为[[x1,y1,x2,y2],[x1,y1,x2,y2],...]
        stream=False,  # 是否流式输出
        timeout=60,  # 网络请求超时时间，单位秒
    )
    return masks_list