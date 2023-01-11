from PySide2.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PySide2.QtGui import QPainter, QPixmap, QFontDatabase
from PySide2.QtCore import Qt
import sys
import numpy as np
from hai_ltt.utils import general

     

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        # id2 = QFontDatabase.addApplicationFont(f'{dir_path}/HarmonyOS_Sans_SC_Bold.ttf')
        # font_str = QFontDatabase.applicationFontFamilies(id)[0]
        # font_str2 = QFontDatabase.applicationFontFamilies(id2)[0]
        # print(id, font_str, id2, font_str2)
        label = QLabel(self)
        label.setText("Hello World")
        label.setStyleSheet("background-color: white; font-size: 40px; font-family: 'HarmonyOS Sans SC';  font-weight: bold")
        label.move(300, 100)

        layout = QHBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.mask_widget()

    def mask_widget(self):
        """遮罩控件"""
        mask = QWidget(self)
        mask.resize(self.size())
        mask.setStyleSheet("background-color: rgba(0, 0, 255, 100);")
        mask.show()


    # def paintEvent(self, event):
    #     print(f'paintEvent: {event}')
    #     painter = QPainter(self)

    #     # 设置图像的透明度
    #     painter.setOpacity(0.8)
    #     # 画笔置顶

    #     # 绘制图像
    #     img = np.zeros((self.size().height(), self.size().width(), 3), dtype=np.uint8)
    #     img[...] =  (65, 105, 225)
    #     img[...] =  (100, 149, 237)
    #     pixmap = general.img2pixmap(img)
    #     painter.drawPixmap(0, 0, self.width()/2, self.height(), pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    dir_path = f'./hai_ltt/gui_framework/translate/fonts/'
    id = QFontDatabase.addApplicationFont(f'{dir_path}/HarmonyOS_Sans_SC_Medium.ttf')
   

    w.show()
    sys.exit(app.exec_())
