
import os, sys
from pathlib import Path
import yaml
from .enum import Colors, FontFamilys
from .preset import Font

here = Path(__file__).parent

def load_config():
    config_file = f'{here}/default_config.yaml'
    assert os.path.exists(config_file), f'config file {config_file} not exists'
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


class HGF(object):

    def __init__(self):
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

