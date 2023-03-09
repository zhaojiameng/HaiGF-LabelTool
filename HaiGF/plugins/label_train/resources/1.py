# 调整彩色图像的亮度和对比度
import cv2 as cv
import numpy as np
from PIL import Image
data = Image.open('D:\\yolov5s\\hep\\te\\000000.jpg')
            
img = np.array(data)
# img = cv.imread('D:\\yolov5s\\hep\\te\\000000.jpg')
img_t = cv.cvtColor(img,cv.COLOR_BGR2HSV)
h,s,v = cv.split(img_t)
delta = 30
# 增加图像亮度
v1 = np.clip(cv.add(1*v,delta),0,255)

# 增加图像对比度
factor = 2
v2 = np.clip(cv.add(factor*v,20),0,255)

img1 = np.uint8(cv.merge((h,s,v1)))
img1 = cv.cvtColor(img1,cv.COLOR_HSV2BGR)
img2 = np.uint8(cv.merge((h,s,v2)))
img2 = cv.cvtColor(img2,cv.COLOR_HSV2BGR)

tmp = np.hstack((img,  img2))  # 三张图片横向合并（便于对比显示）

cv.imshow('image', tmp)
cv.waitKey(0)
cv.destroyAllWindows()
