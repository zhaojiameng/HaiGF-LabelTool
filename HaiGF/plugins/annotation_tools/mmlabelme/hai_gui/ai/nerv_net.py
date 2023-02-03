import os, sys
from pathlib import Path

from .behavior.detector.detector import Detector
from .behavior.tracker.tracker import Tracker
from .behavior.poser.poser import Poser
from .behavior.classifier.classifier import Classifier
from .behavior.dataloader import dataloader

py_dir = Path(os.path.abspath(__file__)).parent  # 本py文件所在文件夹


class Config(object):
    yaml_dir = f'{py_dir}/yamls'
    detector_cfg = f'{yaml_dir}/SEYOLOv5_config_file.yaml'
    tracker_cfg = f'{yaml_dir}/Deepsort_config_file.yaml'
    poser_cfg = f'{yaml_dir}/AlphaPose_config_file.yaml'
    classifier_cfg = f'{yaml_dir}/Resnet50_config_file.yaml'

    img_sz = 640


class NervNet(object):
    def __init__(self, app_cfg=None) -> None:
        app_cfg = app_cfg if app_cfg else Config()
        raw_path = os.getcwd()
        # now_path = raw_path + "/src/ws_detk/models/nerv_net/behavior"
        now_path = f'{py_dir}/behavior'
        sys.path.insert(0, now_path)
        os.chdir(now_path)

        self.detector = Detector(
            detector_type="SEYOLOv5",
            cfg_file=app_cfg.detector_cfg
        )
        self.tracker = Tracker(
            tracker_type="Deepsort",
            cfg_file=app_cfg.tracker_cfg
        )
        self.poser = Poser(
            poser_type="AlphaPose",
            cfg_file=app_cfg.poser_cfg
        )
        self.classifier = Classifier(
            classifier_type="Resnet50",
            cfg_file=app_cfg.classifier_cfg
        )

        self.detector.run_through_once(imgsz=app_cfg.img_sz)

        sys.path.__delitem__(0)
        os.chdir(raw_path)

    def load_single_img(self, file, img_sz=640, return_list=False):
        return dataloader.load_single_img(file, img_sz=img_sz, return_list=return_list)


def create_nerv_net(app_cfg):
    return NervNet(app_cfg)
