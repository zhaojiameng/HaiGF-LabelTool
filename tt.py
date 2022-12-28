import sys
from PySide2.QtWidgets import (QApplication, QWidget, QSplitter, QTextEdit, QVBoxLayout, QHBoxLayout,
    QToolBar)
from PySide2.QtCore import Qt

from hai_ltt.gui_framework.widgets.tab_widget import Page

app = QApplication(sys.argv)
# window = QWidget()
window = Page()
window.setGeometry(100, 100, 800, 600)

# splitter = QSplitter(Qt.Horizontal)

# textEdit1 = QTextEdit()
# textEdit2 = QTextEdit()

# splitter.addWidget(textEdit1)
# splitter.addWidget(textEdit2)

# # 把splitter放到widget中
# layout = QHBoxLayout()
# layout.addWidget(splitter)
# window.setLayout(layout)



window.show()

sys.exit(app.exec_())




