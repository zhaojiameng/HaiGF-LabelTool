
from PySide2.QtCore import QRect
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QTabWidget,
    QLabel, QTabBar, QPushButton)

from .tab_widget import TabWidget, get_tab_widget

def get_central_widget(parent=None):
    return CentralWidget(parent=parent)

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.tab_widgets = [get_tab_widget(id=i) for i in range(2)]
        self.reload()
        
    def reload(self):
        """重新加载内容"""
        tab_widgets = self.tab_widgets
        # self.layout.removeWidget(tab_widgets)
        # 清除所有的子控件
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        for tab_widget in tab_widgets:
            self.layout.addWidget(tab_widget)




        


