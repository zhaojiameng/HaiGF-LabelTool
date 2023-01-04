import numpy as np
from PySide2.QtGui import QImage, QPixmap

def img2pixmap(img, size=None):
    img = np.array(img, dtype=np.uint8)
    image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    return QPixmap.fromImage(image)
