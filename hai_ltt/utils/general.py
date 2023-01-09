import numpy as np
from PySide2.QtGui import QImage, QPixmap
import subprocess


def img2pixmap(img, size=None):
    img = np.array(img, dtype=np.uint8)
    image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    return QPixmap.fromImage(image)


def get_screen_resolution():
    output = subprocess.run(["xrandr"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    for line in output.split("\n"):
        if "*" in line:
            resolution = line.split()[0]
            break
    # print(f"Screen resolution: {resolution}")
    return resolution
