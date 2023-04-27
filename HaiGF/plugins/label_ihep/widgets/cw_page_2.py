"""
The cw page.
It is a mark Q&A tool.
"""

from pathlib import Path
from PySide2 import QtWidgets
from HaiGF import HPage, HGF
from ..scripts.data_process import get_list
from PySide2 import QtCore
from ..scripts.data_process import set_datasets, update_label
from ..scripts.ai_annote import get_annotation
import threading
import damei as dm

logger = dm.get_logger('cw_page')
here = Path(__file__).parent.parent

set_datasets('zjm')
label_list = get_list('label_list', 'zjm')
catetory_list = get_list('category_list', 'zjm')


class MarkIhepPage2(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('mark ihep Q&A'))
        self.set_icon(HGF.ICONS('ihep'))
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.data = None
        self.auto_upload = False
        self.index = None
        self.labeler = None
        self.t1 = None
       
       

    def create_page(self):
        """
        category, answer_quality, and question & answer & artificial_answer
        """
        self.index = self.data["index"]
        self.t1 = threading.Thread(target=self.ai_annotate)
        self.t1.start()
        self.category_label = QtWidgets.QLabel("category")
        self.category_comboBox = QtWidgets.QComboBox()
        self.category_comboBox.addItems(catetory_list)
        self.category_comboBox.setCurrentText(self.data['data'].get('category', '1'))
        #在后面放置一个label,用来显示当前的index
        self.ai_label = QtWidgets.QLabel()
        self.ai_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_label.setStyleSheet("color: gray;")
        self.ai_label.hide()
        
        self.layout.addWidget(self.category_label, 0, 0)
        self.layout.addWidget(self.category_comboBox, 0, 1)
        self.layout.addWidget(self.ai_label, 0, 2)

        self.answer_quality_label = QtWidgets.QLabel("answer_quality")
        #spinbox来代替combobox
        self.answer_quality_textEdit = QtWidgets.QSpinBox()
        self.answer_quality_textEdit.setRange(0, 10)
        self.answer_quality_textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.answer_quality_textEdit.setStyleSheet("QSpinBox::up-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:right;\n"
"width:40px;\n"
"height:40px;\n"
"\n"
"}\n"
"QSpinBox::down-button{\n"
"subcontrol-origin:border;\n"
"subcontrol-position:left;\n"
"width:40px;\n"
"height:40px;\n"
"}")
        self.answer_quality_textEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.answer_quality_textEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.answer_quality_textEdit.setValue(self.data['data'].get('answer_quality', 0))
        self.layout.addWidget(self.answer_quality_label, 0, 3)
        self.layout.addWidget(self.answer_quality_textEdit, 0, 4)

        self.question_label = QtWidgets.QLabel("question")
        self.question_textEdit = QtWidgets.QTextEdit()
        self.question_textEdit.setText(self.data['data']['question'])
        self.question_textEdit.setReadOnly(True)
        self.layout.addWidget(self.question_label, 1, 0)
        self.layout.addWidget(self.question_textEdit, 1, 1, 1, 3)

        self.answer_label = QtWidgets.QLabel("answer")
        self.answer_textEdit = QtWidgets.QTextEdit()
        self.answer_textEdit.setText(self.data['data']['answer'])
        self.answer_textEdit.setReadOnly(True)
        self.layout.addWidget(self.answer_label, 2, 0)
        self.layout.addWidget(self.answer_textEdit, 2, 1, 1, 3)

        self.artificial_answer_label = QtWidgets.QLabel("artificial_answer")
        self.artificial_answer_textEdit = QtWidgets.QTextEdit()
        self.artificial_answer_textEdit.setText(self.data['data'].get('artificial_answer', ''))
        self.artificial_answer_textEdit.keyPressEvent = self.keyPressEvent
        self.layout.addWidget(self.artificial_answer_label, 3, 0)
        self.layout.addWidget(self.artificial_answer_textEdit, 3, 1, 1, 3)
        self.ai_annotate()

    def update_page(self):
        self.ai_label.hide()
        if self.auto_upload:
            self.save()
        self.index = self.data['index']
        #结束上一个线程
        if self.t1:
            self.t1.join()

        self.t1 = threading.Thread(target=self.ai_annotate)
        self.t1.start()
        self.category_comboBox.setCurrentText(self.data['data'].get('category', '1'))
        self.answer_quality_textEdit.setValue(self.data['data'].get('answer_quality', 0))
        self.question_textEdit.setText(self.data['data']['question'])
        self.answer_textEdit.setText(self.data['data']['answer'])
        self.artificial_answer_textEdit.setText(self.data['data'].get('artificial_answer', ''))
        

    def save(self):
        category = self.category_comboBox.currentText()
        answer_quality = self.answer_quality_textEdit.value()
        artificial_answer = self.artificial_answer_textEdit.toPlainText()
        update_label(self.index, category, answer_quality, artificial_answer, self.labeler)

    def ai_annotate(self):
        text = get_annotation(self.data['data']['question'], self.data['data']['answer'], catetory_list)
        #截取：后面的内容
        text = text.split(':')[-1]
        self.ai_label.setText(text)
        self.ai_label.show()

    #按下tab键时，将self.ai_label的值赋给self.category_comboBox
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            self.category_comboBox.setCurrentText(self.ai_label.text())
            print(self.category_comboBox.currentText())
            self.ai_label.hide()
        else:
            super().keyPressEvent(event)

        

        



   

