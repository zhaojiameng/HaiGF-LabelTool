
import os, sys
from pathlib import Path
import yaml
from .enum import Colors, FontFamilys
from .preset import Font
from hai_ltt.utils import general

here = Path(__file__).parent

def load_config():
    config_file = f'{here}/default_config.yaml'
    assert os.path.exists(config_file), f'config file {config_file} not exists'
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


class HGF(object):

    def __init__(self):
        self.SCALE_FACTOR = self.auto_scale()
        self.COLORS = Colors()
        self.FONT_FAMILYS = FontFamilys()
        self.CONFIG = load_config()

    @property
    def FONT_FAMILY(self):
        """默认字体类型"""
        return self.FONT_FAMILYS.AlBayan
    
    @property
    def FONT_SIZE(self):
        """默认字体大小"""
        return self.CONFIG['font_size']
        return self.CONFIG['font_size']*self.SCALE_FACTOR

    @property
    def FONT(self):
        """默认字体"""
        return Font(
            family=self.FONT_FAMILY, 
            size=self.FONT_SIZE,
            bold=False,
            )

    @property
    def THEME(self):
        """主题"""
        return self.CONFIG['theme']

    @property
    def CORE_FUNC_BAR_BACKGOUND_COLOR(self):
        """核心功能栏背景色"""
        if self.THEME == 'Dark':
            return self.COLORS.LightBlack
        elif self.THEME == 'Light':
            return self.COLORS.LightGray

    def auto_scale(self, ):
        """根据屏幕分辨率自动缩放"""
        resolution = general.get_screen_resolution()
        w, h = resolution.split('x')
        w, h = int(w), int(h)
        rw = w / 1920
        rh = h / 1080
        return min(rw, rh)

    @property
    def TAB_FONT(self):
        """Tab字体"""
        return Font(
            family=self.FONT_FAMILY, 
            size=int(self.FONT_SIZE*0.9),
            bold=False,
            )

