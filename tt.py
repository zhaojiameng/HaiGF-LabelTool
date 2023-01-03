import sys
from PySide2.QtWidgets import (QApplication, QWidget, QSplitter, QTextEdit, QVBoxLayout, QHBoxLayout,
    QToolBar,  QListView)
from PySide2.QtCore import Qt, QAbstractItemModel, QModelIndex, Qt

from hai_ltt.gui_framework.widgets.certral_widgets.tab_widget import Page

def tt1():
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



class MyModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return 3

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.row() == 0:
                return "Item 1"
            elif index.row() == 1:
                return "Item 2"
            elif index.row() == 2:
                return "Item 3"
        return None


if __name__ == '__main__':
    app = QApplication([])

    list_view = QListView()
    model = MyModel()
    list_view.setModel(model)
    list_view.show()
    sys.exit(app.exec_())







