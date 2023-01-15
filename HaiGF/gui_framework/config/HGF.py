
import os, sys
from pathlib import Path
import yaml
from .enum import Colors, FontFamilys
from .preset import Font
from HaiGF.utils import general
import damei as dm

here = Path(__file__).parent

def load_config():
    config_file = f'{here}/default_config.yaml'
    assert os.path.exists(config_file), f'config file {config_file} not exists'
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


class HGF(object):

    def __init__(self):
        self.tsf = self.get_text_scale_factor()  # windows system font scale factor
        self.SCALE_FACTOR = self.auto_scale()
        self.COLORS = Colors()
        self.FONT_FAMILYS = FontFamilys()
        self.CONFIG = load_config()

    def get_text_scale_factor(self, ):
        """获取缩放系数"""
        # mac为1，windows为1.8， linux为2
        system = dm.current_system()
        if system == 'windows':
            return 1.8
        elif system == 'linux':
            return 2.5
        elif system == 'macos':
            return 1
        else:
            raise ValueError(f'Unsupported system: {system}')

    @property
    def FONT_FAMILY(self):
        """默认字体类型"""
        # return self.FONT_FAMILYS.AlBayan
        return self.FONT_FAMILYS.HarmonyOS
    
    @property
    def FONT_SIZE(self):
        """默认字体大小"""
        return self.CONFIG['font_size']
        return self.CONFIG['font_size']*self.SCALE_FACTOR
    @property
    def TEXT_FONT_SIZE(self):
        """默认应用于CSS的文本字体大小，是默认字体大小的乘以文本缩放系数"""
        return self.FONT_SIZE*self.tsf

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
        if resolution is None:
            return 1
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
    
    @property
    def FIRST_LEVEL_FONT(self):
        """一级字体"""
        return Font(
            family=self.FONT_FAMILY, 
            size=int(self.FONT_SIZE*1.2),
            bold=True,
            )

    @property
    def FIRST_LEVEL_TITLE_CSS(self):
        """一级字体CSS"""
        back = f'font-family: {self.FONT_FAMILY}; font-size: {int(self.TEXT_FONT_SIZE*1.8)}px; \
                font-weight: bold; color: {self.COLORS.LightBlack}; \
                    background-color: #EE3B3B; border-radius: 4px; border: 2px solid {self.COLORS.LightBlack};'
        # return back
        return f'font-family: {self.FONT_FAMILY}; font-size: {int(self.TEXT_FONT_SIZE*1.8)}px; \
                font-weight: bold; color: {self.COLORS.LightBlack}; '

    @property
    def SECOND_LEVEL_TITLE_CSS(self):
        """二级字体CSS"""
        return f'font-family: {self.FONT_FAMILY}; font-size: {int(self.TEXT_FONT_SIZE*1.4)}px; \
                font-weight: bold; color: {self.COLORS.DimGray}; '

    @property
    def MAIN_TEXT_CSS(self):
        return f'font-family: {self.FONT_FAMILY}; font-size: {int(self.TEXT_FONT_SIZE)}px; \
            font-weight: False; color: {self.COLORS.Black}; '

    @property
    def MAIN_SIDE_BAR_CSS(self):
        return f'font-family: {self.FONT_FAMILY}; font-size: {int(self.TEXT_FONT_SIZE)}px; \
                font-weight: False; color: {self.COLORS.Black}; '

    @property
    def STATUS_BAR_CSS(self):
        return f'font-family: {self.FONT_FAMILY}; font-size: {int(self.TEXT_FONT_SIZE)}px; \
                font-weight: False; color: {self.COLORS.White}; background-color: #FF9966; '
        