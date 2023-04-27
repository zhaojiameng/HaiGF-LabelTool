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
column_list = ["baseInformation", "question", "answer", "category","artificial_answer", "answer_quality"]
base_list = ["id", "labeler", "label_time", "checked", "locked", "questioner", "question_time"]

class MarkIhepPage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('mark ihep Q&A'))
        self.set_icon(HGF.ICONS('ihep'))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.data = [{'id': 1, 'question': 'question1', 'answer': 'answer1', 'category': 'category1', 'artificial_answer': 'artificial_answer1', 'answer_quality': 'answer_quality1', 'labeler': 'labeler1', 'label_time': 'label_time1', 'checked': 'checked1', 'locked': 'locked1', 'questioner': 'questioner1', 'question_time': 'question_time1'}]
      
        # for i in range(5):
        #     hbox = self.creat_QA()
        #     self.layout.addLayout(hbox)
        self.creat_Table()

    def creat_Table(self):
        self.table = QtWidgets.QTableWidget()
        #版本2
        self.table.setColumnCount(len(column_list))
        self.table.setHorizontalHeaderLabels(column_list)
        self.update_table()

        # 自适应列宽
        # 不显示行号
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        #设置行高最大为60
        self.table.verticalHeader().setDefaultSectionSize(250)

        # 设置表头自适应大小
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setMaximumSectionSize(300)

        # 将QTableWidget添加到布局管理器中
        self.layout.addWidget(self.table)

    # 更新表格数据
    def update_table(self):
        self.table.setRowCount(len(self.data))
        
        #版本2
        for i, row in enumerate(self.data):
            baseInformation = {}
            for j, key in enumerate(label_list):
                value = row.get(key, ' ')
                if key in base_list:
                    baseInformation[key] = value
                else:
                    table_item = QtWidgets.QTableWidgetItem(str(value))
                    self.table.setItem(i, j, table_item)
            table_item = QtWidgets.QTableWidgetItem(str(baseInformation))
            self.table.setItem(i, 0, table_item)

    def creat_QA(self):
        hbox = QtWidgets.QHBoxLayout()
    
        Q_label = QtWidgets.QLabel("Q: ")
        Q_text = QtWidgets.QTextEdit()
        #设置为绿底白字，字号为20，宽度为200，高度为100
        Q_text.setStyleSheet("background-color:green;color:white;font-size:20px;width:100px;height:30px;")
  
        A_label = QtWidgets.QLabel("A: ")
        A_text = QtWidgets.QTextEdit()
        #设置为白底黑色，字号为20，宽度为200，高度为100
        A_text.setStyleSheet("background-color:white;color:black;font-size:20px;width:100px;height:30px;")

        hbox.addWidget(Q_label)
        hbox.addWidget(Q_text)
        hbox.addWidget(A_label)
        hbox.addWidget(A_text)

        # 创建一个下拉框，并添加选项
        combo_boxQ = QtWidgets.QComboBox()
        combo_boxQ.addItem("标注A")
        combo_boxQ.addItem("标注B")
        combo_boxQ.addItem("标注C")
        combo_boxA = QtWidgets.QComboBox()
        combo_boxA.addItem("标注A")
        combo_boxA.addItem("标注B")
        combo_boxA.addItem("标注C")
        
        hbox.addWidget(combo_boxQ)
        hbox.addWidget(combo_boxA)
        return hbox

