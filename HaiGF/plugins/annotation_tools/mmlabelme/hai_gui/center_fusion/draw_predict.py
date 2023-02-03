import xml.dom.minidom
import pandas as pd
import os
import math
import cv2
import torch
from center_fusion import RtoS_NN
import numpy as np

PI = math.pi


def get_points(img, yp, xp, point_size):
    for i in range(point_size):
        for j in range(point_size):
            img[xp + i - 1, yp + j - 1, 0] = 0
            img[xp + i - 1, yp + j - 1, 1] = 0
            img[xp + i - 1, yp + j - 1, 2] = 255
    return img


def fusion(file, points):
    model = RtoS_NN.RtoS_NN()
    model.load_state_dict(torch.load('/home/sawyer/codes/xsensing/mmlabelme/mmlabelme/center_fusion/NNmodel.pth'))

    # ste_name = file[0:-8] + '_ste.jpg'
    ste_name = file
    img = cv2.imread(ste_name)
    # for obj in objs:
    cx = (points[0][0] + points[1][0])/2

    cy = (points[0][1] + points[1][1])/2

    w = (max(points[1][0], points[0][0])-min(points[1][0], points[0][0]))

    h = (max(points[1][1], points[0][1])-min(points[1][1], points[0][1]))

    angle = 0

    if angle >= PI / 2:
        real_agl = angle + PI
    else:
        real_agl = angle
    # 得到底部两个坐标值（未旋转时）
    xlf_d_ = (0 - w) / 2
    ylf_d_ = (0 + h) / 2
    xrt_d_ = (0 + w) / 2
    yrt_d_ = (0 + h) / 2

    xlf_u_ = (0 - w) / 2
    ylf_u_ = (0 - h) / 2
    xrt_u_ = (0 + w) / 2
    yrt_u_ = (0 - h) / 2

    cos = math.cos(real_agl)
    sin = math.sin(real_agl)

    xlf_d = cx + cos * xlf_d_ - sin * ylf_d_
    ylf_d = cy + sin * xlf_d_ + cos * ylf_d_
    xrt_d = cx + cos * xrt_d_ - sin * yrt_d_
    yrt_d = cy + sin * xrt_d_ + cos * yrt_d_

    xlf_u = cx + cos * xlf_u_ - sin * ylf_u_
    ylf_u = cy + sin * xlf_u_ + cos * ylf_u_
    xrt_u = cx + cos * xrt_u_ - sin * yrt_u_
    yrt_u = cy + sin * xrt_u_ + cos * yrt_u_

    rdr_d = torch.FloatTensor([xlf_d, ylf_d, xrt_d, yrt_d])
    pre_ste_d = model(rdr_d)
    pre_ste_d = pre_ste_d.detach().numpy()
    pre_ste_d = pre_ste_d.astype(np.int_)
    # img = get_points(img, pre_ste_d[0], pre_ste_d[1], 5)
    # img = get_points(img, pre_ste_d[2], pre_ste_d[3], 5)

    rdr_u = torch.FloatTensor([xlf_u, ylf_u, xrt_u, yrt_u])
    pre_ste_u = model(rdr_u)
    pre_ste_u = pre_ste_u.detach().numpy()
    pre_ste_u = pre_ste_u.astype(np.int_)
    # img = get_points(img, pre_ste_u[0], pre_ste_u[1], 5)
    # img = get_points(img, pre_ste_u[2], pre_ste_u[3], 5)

    points_return = [(pre_ste_d[0], pre_ste_d[1]), (pre_ste_d[2], pre_ste_d[3]), (pre_ste_u[0], pre_ste_u[1]), (pre_ste_u[2], pre_ste_u[3])]
    # cv2.namedWindow('result', 0)
    # cv2.resizeWindow('result', 500, 500)
    # cv2.imshow('result', img)
    # while 1:
    #     if cv2.waitKey() == 27:
    #         break
    return img, points_return


if __name__ == '__main__':
    files = os.listdir('./rdr_ste_mix/')
    f_xml = r'./rdr_ste_mix/13_rdr.xml'
    result = center_fusion(f_xml)

