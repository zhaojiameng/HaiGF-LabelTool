"""
The cw page.
It is a mark Q&A tool.
"""

from pathlib import Path
from PySide2 import QtWidgets
from HaiGF import HPage, HGF
import damei as dm

logger = dm.get_logger('cw_page')
here = Path(__file__).parent.parent


label_list = ["id", "question", "answer", "category","artificial_answer", "answer_quality","labeler", "label_time", 
              "checked", "locked", "questioner", "question_time"]
large_list = ["question", "answer", "artificial_answer"]
annaotion_list = ["Others","Hep", "Particle", "Computer Science", "Astrophysics", "Photon physics"]

class MarkIhepPage1(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('mark ihep Q&A'))
        self.set_icon(HGF.ICONS('ihep'))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.data = []
        self.creat_Table()

    def creat_Table(self):
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(label_list)
        self.table.cellChanged.connect(self.cell_changed)
        self.table.setRowCount(0)
        for i in range(len(self.data)):
            self.insert_row(i)

        # 自适应列宽
        # 不显示行号
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        #设置行高最大为60
        self.table.verticalHeader().setDefaultSectionSize(70)

        # 设置表头自适应大小
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setMaximumSectionSize(200)

        # 将QTableWidget添加到布局管理器中
        self.layout.addWidget(self.table)

    # 单元格内容改变时触发
    def cell_changed(self, row, column):
        # 获取当前单元格的值
        value = self.table.item(row, column).text()
        # 更新数据
        self.data[row][label_list[column]] = value

    def combo_changed(self, row, key):
        # 获取当前下拉框的值
        combo = self.table.cellWidget(row, label_list.index(key))
        value = combo.currentText()
        # 更新数据
        self.data[row][key] = value
        # 更新表格数据
        self.update_table()

    # 更新表格数据
    def update_table(self):
        self.insert_row(len(self.data)-1)

    def insert_row(self, row):
        self.table.insertRow(row)
        data = self.data[row]
        for j, key in enumerate(label_list):
            if key in large_list:
                btn = QtWidgets.QPushButton('查看文本')
                btn.clicked.connect(lambda *args, i=row, key=key: self.show_large_text(i, key))
                self.table.setCellWidget(row, j, btn)
            elif key == 'category':
                combo = QtWidgets.QComboBox()
                combo.addItems(annaotion_list)
                combo.setCurrentText(data.get(key, annaotion_list[0]))
                combo.currentTextChanged.connect(lambda *args, i=row, key=key: self.combo_changed(i, key))
                self.table.setCellWidget(row, j, combo)
            else:
                item = QtWidgets.QTableWidgetItem(str(data.get(key, '')))
                self.table.setItem(row, j, item)
        
        
    def show_large_text(self, row, key):
        large_text = self.data[row].get(key, ' ')
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f'{key} - 文本')

        vbox = QtWidgets.QVBoxLayout()

        text_edit = QtWidgets.QTextEdit()
        text_edit.setPlainText(large_text)
        vbox.addWidget(text_edit)

        close_button = QtWidgets.QPushButton('关闭')
        close_button.clicked.connect(dialog.close)
        vbox.addWidget(close_button)

        dialog.setLayout(vbox)
        dialog.exec_()
        
    

