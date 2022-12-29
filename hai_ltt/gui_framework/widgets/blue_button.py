from hai_ltt.apis import HGF
from PySide2.QtWidgets import QPushButton
from PySide2 import QtCore, QtWidgets


class BlueButton(QPushButton):
    def __init__(self, text, parent=None, **kwargs):
        super().__init__(text, parent)
        # 设置字体
        self.setFont(HGF.FONT)
        self.setStyleSheet(
            f"background-color: {HGF.COLORS.RoyalBlue}; \
                color: {HGF.COLORS.White}; \
                border-radius: 5px;")
        # 设置尺寸策略为适应内容
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
