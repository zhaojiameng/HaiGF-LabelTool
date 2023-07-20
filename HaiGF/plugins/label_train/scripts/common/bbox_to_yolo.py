import os
import cv2
"""
将边界框坐标转换为YOLO格式

"""
def append_yolo_label(image_path, bbox, label_file):
    # 获取图像宽度和高度
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    # 将边界框坐标转换为YOLO格式
    x_center = bbox[0] + bbox[2] / 2
    y_center = bbox[1] + bbox[3] / 2
    x_center /= width
    y_center /= height
    bbox_width = bbox[2] / width
    bbox_height = bbox[3] / height

    # 将标注信息写入文件
    with open(label_file, 'a') as f:
        label = '{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format('object-class', x_center, y_center, bbox_width, bbox_height)
        f.write(label)

# 示例用法
image_path = 'path/to/image.jpg'
bbox = [100, 100, 200, 300] # [x, y, width, height]
label_file = 'path/to/label.txt'
append_yolo_label(image_path, bbox, label_file)