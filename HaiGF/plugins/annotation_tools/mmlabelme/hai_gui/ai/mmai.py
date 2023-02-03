import os, sys
import time

# import torch
import logging

from .service import Service
from .client import Client
from .nerv_net import NervNet

logging.getLogger(__name__)


def build_ai():
    return MMAi()


class MMAi(object):
    """Multi Modal Artificial Intelligence"""
    def __init__(self):
        self.service = Service()
        self.client = Client()
        self.nervnet = None

    def check_and_init(self):
        if self.nervnet is None:
            """init"""
            self.nervnet = NervNet()

    def run(self, files):
        """"""
        logging.info(f"run ai")

        self.check_and_init()  # 检查服务并启动
        # track_ret = None
        status_ret = None
        im0s = None
        for i, file in enumerate(files):
            paths, imgs, im0s = self.nervnet.load_single_img(file, return_list=True)  # bs为1
            det_ret = self.nervnet.detector.detect(paths, imgs, im0s)
            track_ret = self.nervnet.tracker.track(det_ret, imgs=im0s)
            poser_ret = self.nervnet.poser.detect_pose(track_ret, im0s, paths, return_type='zzd')
            status_ret = self.nervnet.classifier.detect_status(poser_ret, paths, is_camera=False)
        # self.nervnet.classifier.analyse_ret(status_ret)
        assert len(status_ret) == 1  # bs为1
        assert len(im0s) == 1
        return status_ret[0], im0s[0]  # [n, 14]

    def stop(self):
        pass