"""
存储所有预设的枚举变量
Usage:
>>> from hai_ltt import HGF
>>> a = HGF.COLORS.RED
>>> widget.setStyleSheet(f'background-color: {a};')
"""

class Colors(object):
    White = "#FFFFFF"  # 255, 255, 255
    WhiteSmoke = "#F5F5F5"  # 245, 245, 245
    Gainsboro = "#DCDCDC"  # 220, 220, 220
    LightGray = "#D3D3D3"  # 211, 211, 211
    Silver = "#C0C0C0"  # 192, 192, 192
    DarkGray = "#A9A9A9"  # 169, 169, 169
    Gray = "#808080"  # 128, 128, 128
    DimGray = "#696969"  # 105, 105, 105
    LightSlateGray = "#778899"  # 119, 136, 153
    SlateGray = "#708090"  # 112, 128, 144
    DarkSlateGray = "#2F4F4F"  # 47, 79, 79
    LightBlack = "#404040"  # 64, 64, 64
    Black = "#000000"  # 0, 0, 0

class FontFamilys(object):
    default = "Microsoft YaHei"


class HGF(object):
    COLORS = Colors()
    FONT_FAMILYS = FontFamilys()
    FONT_FAMILY = FONT_FAMILYS.default
    FONT_SIZE = 12



    