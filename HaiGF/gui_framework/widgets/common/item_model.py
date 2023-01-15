
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtWidgets import QApplication, QListView

import numpy as np

class ItemModel(QAbstractItemModel):
    """
    用于QListView的数据模型，显示列表或表格数据
    """
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        data = data if data is not None else np.array([])
        self._entry = data
        # self.load_data(data)

    @property
    def entry(self):
        return self._entry

    # def load_data(self, data):
    #     if data.ndim == 1:
    #         self._entry = data.tolist()
    #     elif data.ndim == 2:
    #         self._entry = data.tolist()

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return self.entry.shape[0]

    def columnCount(self, parent=QModelIndex()):
        if self.entry.ndim == 1:
            return 1
        elif self.entry.ndim == 2:
            return self.entry.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if self.entry.ndim == 1:
                row = index.row()
                return self.entry[row]
            elif self.entry.ndim == 2:
                row, column = index.row(), index.column()
                return self.entry[row, column]
            else:
                return None
        return None

    @staticmethod
    def from_list(data, parent=None):
        """从列表中获取数据"""
        data = np.array(data)
        assert data.ndim in [1, 2], "Data must be 1D or 2D"
        return ItemModel(data=data, parent=parent)
    
    @staticmethod
    def from_numpy(data, parent=None):
        """从numpy中获取数据"""
        return ItemModel(data=data, parent=parent)

    

if __name__ == '__main__':
    app = QApplication([])

    list_view = QListView()
    model = ItemModel()
    list_view.setModel(model)
    list_view.show()

    app.exec()


