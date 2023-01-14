from PySide2.QtGui import QIcon, QFont

class Font(QFont):
    def __init__(self, family, size, **kwargs):
        super().__init__()
        bold = kwargs.pop("bold", False)

        self.setFamily(family)
        self.setPointSize(size)
        self.setBold(bold)
