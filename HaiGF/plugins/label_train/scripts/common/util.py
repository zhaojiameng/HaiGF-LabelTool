
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox
from PySide2.QtCore import Qt
import os
class CommonDialog(QDialog):
    def __init__(self, parent=None, title='Common Dialog'):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout(self)
        self.label_edit = QLineEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.layout.addWidget(self.label_edit)
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

def rectroi_to_yolo(rectroi, img_width, img_height):
    x, y, w, h = rectroi.pos().x(), rectroi.pos().y(), rectroi.size().x(), rectroi.size().y()
    x_center = x + w / 2
    y_center = y + h / 2
    x_center /= img_width
    y_center /= img_height
    w /= img_width
    h /= img_height
    class_id = rectroi.label
    return class_id, x_center, y_center, w, h

def asure_folder(folder):
    if  folder is None:
        from tkinter import filedialog
        # 弹出文件夹选择对话框
        folder_path = filedialog.askdirectory()
        # 判断选择的是否是文件夹
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print("请选择一个文件夹!")
        pass
    else:
        if os.path.isdir(folder):
            return folder
        else:
            print("请选择一个文件夹!")
        pass
        