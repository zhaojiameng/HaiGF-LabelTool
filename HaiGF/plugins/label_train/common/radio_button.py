from PySide2 import QtWidgets, QtCore

class RadioButton(QtWidgets.QToolButton):
    def __init__(self, parent=None, text='', icon=None):
        super().__init__(parent)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        
        # 设置 QToolButton 的样式表
        self.setStyleSheet("""
            QToolButton {
                border: 1px solid black;
            }
            QToolButton:checked {
                background-color: blue;
            }
        """)

        # 设置 QToolButton 的文本和行为模式
        self.setText(text)
        self.setIcon(icon)
        self.setCheckable(True)

    def sizeHint(self):
        # 重写 sizeHint() 方法，使得按钮的大小适应文本和图标
        size = super().sizeHint()
        size.setHeight(size.height() + 10)
        size.setWidth(max(size.width(), size.height()) + 30)
        return size

    def nextCheckState(self):
        # 重写 nextCheckState() 方法，使得按钮的状态只有两种
        if self.isChecked():
            self.setChecked(False)
        else:
            self.setChecked(True)

    