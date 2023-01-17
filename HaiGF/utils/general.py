import numpy as np
from PySide2.QtGui import QImage, QPixmap, QImageReader
import subprocess
import PIL
import cv2
import io


def img2pixmap(img, size=None):
    img = np.array(img, dtype=np.uint8)
    image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    return QPixmap.fromImage(image)


def get_screen_resolution():
    return None
    output = subprocess.run(["xrandr"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    for line in output.split("\n"):
        if "*" in line:
            resolution = line.split()[0]
            break
    # print(f"Screen resolution: {resolution}")
    return resolution


def imgdata2qt(mw, img_data, filename):
    image = QImage.fromData(img_data)  # 读取图像，这个是QT的图像格式
    if image.isNull():
        formats = [
            "*.{}".format(fmt.data().decode())
            for fmt in QImageReader.supportedImageFormats()
        ]
        mw.errorMessage(
            mw.tr("Error opening file"),
            mw.tr(
                "<p>Make sure <i>{0}</i> is a valid image file.<br/>"
                "Supported image formats: {1}</p>"
            ).format(filename, ",".join(formats)),
        )
        mw.status(mw.tr("Error reading %s") % filename)
        return False
    return image


def numpy_img2bytes(img, suffix):
        image_pil = PIL.Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        with io.BytesIO() as f:  # 内存中创建一个二进制文件
            # if PY2 and QT4:
            #     format = "PNG"
            if suffix in [".jpg", ".jpeg"]:
                format = "JPEG"
            else:
                format = "PNG"
            image_pil.save(f, format=format)  # 保存格式
            f.seek(0)  # 一定文件读写指针的位置
            return f.read()
