"""
存储所有预设的枚举变量
Usage:
>>> from hai_ltt import HGF
>>> a = HGF.COLORS.RED
>>> widget.setStyleSheet(f'background-color: {a};')
"""

from .preset import Font

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

    Blue = "#0000FF"  # 纯蓝，0, 0, 255
    MediumBlue = "#0000CD"  # 中蓝，0, 0, 205
    MidnightBlue = "#191970"  # 午夜蓝，25, 25, 112
    DarkBlue = "#00008B"  # 深蓝，0, 0, 139
    Navy = "#000080"  # 海军蓝，0, 0, 128
    RoyalBlue = "#4169E1"  # 皇家蓝，65, 105, 225
    CornflowerBlue = "#6495ED"  # 矢车菊蓝，100, 149, 237
    LightSteelBlue = "#B0C4DE"  # 淡钢蓝，176, 196, 222
    SteelBlue = "#4682B4"  # 钢蓝，70, 130, 180
    SkyBlue = "#87CEEB"  # 天蓝，135, 206, 235
    LightSkyBlue = "#87CEFA"  # 淡天蓝，135, 206, 250
    DeepSkyBlue = "#00BFFF"  # 深天蓝，0, 191, 255
    DodgerBlue = "#1E90FF"  # 道奇蓝，30, 144, 255
    Azure = "#F0FFFF"  # 蔚蓝，240, 255, 255

    # 设定控件颜色
    # CoreFuncBarBackground = DimGray
    CoreFuncBarBackground = LightGray

class FontFamilys(object):
    MicrosoftYaHei = "Microsoft YaHei"
    AlBayan = "Al Bayan"
    

    