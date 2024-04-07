import base64
import json
import requests
import numpy as np
import os
import matplotlib.pyplot as plt
import hai
import cv2
import random


def seg_via_sam(input_points=None, input_labels=None, input_boxes=None, img=None, upload_type=0, api_key=None):
    if input_points is not None and len(input_points) == 0:
        input_points = None
    if input_labels is not None and len(input_labels) == 0:
        input_labels = None
    if input_boxes is not None and len(input_boxes) == 0:
        input_boxes = None
    only_mask = True if upload_type == 0 else False
    # only_mask = False
    masks_list = hai.Models.inference(
        model='meta/segment_anything_model',  # 指定可用模型名字
        api_key=api_key,  # 输入hepai_api_key
        img = img,  # 输入图片路径或cv2读取的图片
        input_points = input_points,  # 点提示，格式为[[x1,y1],[x2,y2],...] 
        input_labels = input_labels,  # 点提示对应的标签，0代表背景点，1代表前景点，格式为[0, 1, ...], 需要与input_points一一对应，如不提供默认全为前景点
        input_boxes = input_boxes,  # 框提示，格式为[[x1,y1,x2,y2],[x1,y1,x2,y2],...]
        only_mask = only_mask,  # 是否只返回掩码，不返回其他信息
        stream=False,  # 是否流式输出
        timeout=60,  # 网络请求超时时间，单位秒
    )
    if upload_type == 1:
        return get_bbox_from_dict(masks_list) if isinstance(masks_list[0], dict) else get_bbox_from_list(masks_list)
    return masks_list

def plot_masks(img, masks, color=None):
    colors = [random.random() for i in range(len(masks))]
    if isinstance(img, str):
        img = cv2.imread(img) 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    if isinstance(masks, list):
        sorted_masks = masks
    else:
        sorted_masks = sorted(masks.values(), key=lambda x: x.get('area',-1), reverse=True)

    for i, mask in enumerate(sorted_masks):
        if isinstance(masks, dict):
            m = mask['segmentation']
        else: 
            m = mask
        
        mask_color_img = np.zeros_like(img)
        mask_color_img[...] = colors[i]
        mask_indices = np.where(m == 1)
        
        alpha = 0.35
        img[mask_indices] = alpha * mask_color_img[mask_indices] + (1-alpha) * img[mask_indices]
    
    return img

def get_bbox_from_dict(masks):
    rects = []
    for item in masks:
        bbox = item['bbox']
        rects.append(bbox)
    return rects

def get_bbox_from_list(masks):
    rects = []
    for item in masks:
        bbox = calculate_rect(item)
        rects.append(bbox)
    

def calculate_rect(mask):
    min_x = min(point[0] for point in mask)
    min_y = min(point[1] for point in mask)
    max_x = max(point[0] for point in mask)
    max_y = max(point[1] for point in mask)
    w, h = max_x - min_x, max_y - min_y
    return min_x, min_y, w, h