from PySide2.QtWidgets import *

class HPage(QWidget):
    """抽象页面，包含ToolBar和Page"""
    def __init__(self, parent=None, icon=None, title=None, **kwargs):
        super().__init__(parent, **kwargs)

        # 设置Tab bar
        self._icon = icon
        self._title = self.tr(title)
        

    
    @property
    def icon(self):
        return self._icon

    @property
    def title(self):
        return self._title

