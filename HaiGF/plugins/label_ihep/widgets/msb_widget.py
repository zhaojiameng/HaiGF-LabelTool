
from HaiGF import HMainSideBarWidget, HAction
from HaiGF.gui_framework.widgets.main_side_bar.explorer_widget import ExplorerWidget
from ..widgets.msb_ui import Ui_Form
from PySide2 import QtWidgets, QtCore
from ..scripts.data_process import get_data, save_dataset
import damei as dm

logger = dm.get_logger('label_ihep_msb_widget')


class LabelIhepMSBWidget(HMainSideBarWidget):
    """数据标注空间，包含标题、标题工具和内容区域，被放置在MainSideBar中"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
       
        self.set_title(self.tr('label ihep Q&A'))

        title_actions = [
            HAction(text='test ihep', parent=self.p, slot=None),]
        self.set_title_actions(title_actions)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.index = 540
        self.data = []

        self.ui.fetchButton.clicked.connect(self.on_fetch_button_clicked)
        self.ui.uploadButton.clicked.connect(self.on_upload_button_clicked)
        self.ui.autoUploadButton.clicked.connect(self.on_auto_upload_button_clicked)
        self.ui.saveButton.clicked.connect(self.save_data)
        self.ui.tree.itemDoubleClicked.connect(self.on_tree_item_double_clicked)
        self.ui.preButton.clicked.connect(self.on_pre_button_clicked)
        self.ui.nextButton.clicked.connect(self.on_next_button_clicked)
        self.ui.annotateUserEditer.textChanged.connect(self.on_annotate_user_editer_text_changed)
        self.load_datas(self.data)
        
    def load_data(self, record):
        item = QtWidgets.QTreeWidgetItem(self.ui.tree, [str(record["index"]),'第{}条记录'.format(record["index"])])
        item.setData(0, QtCore.Qt.UserRole, record)

    def load_datas(self, records=None):
        for record in records:
            self.load_data(record)


    def on_fetch_button_clicked(self):
        # mw = self.p
        # plg = mw.plugins['LabelIhepPlugin']
        # plg.fetch_data(self.index)
        # self.index += 1
        records = get_data(self.index, self.ui.annotateUserEditer.text())
        self.data += records
        self.index += len(records)
        self.load_datas(records)

    def on_auto_upload_button_clicked(self):
        mw = self.p
        plg = mw.plugins['LabelIhepPlugin']
        plg.auto_upload(self.ui.autoUploadButton.isChecked())
        

    def on_upload_button_clicked(self):
        mw = self.p
        plg = mw.plugins['LabelIhepPlugin']
        # plg.save_data()
        plg.update_label()

    def on_tree_item_double_clicked(self):
        mw = self.p
        plg = mw.plugins['LabelIhepPlugin']
        #将双击的记录传递给LabelIhepPlugin的show_data函数
        record = self.ui.tree.currentItem().data(0, QtCore.Qt.UserRole)
        self.ui.preButton.setEnabled(self.hasPrevRecord())
        self.ui.nextButton.setEnabled(self.hasNextRecord())
        plg.show_data(record)

    def hasPrevRecord(self):
        return self.ui.tree.indexOfTopLevelItem(self.ui.tree.currentItem()) > 0

    def hasNextRecord(self):
        return self.ui.tree.indexOfTopLevelItem(self.ui.tree.currentItem()) < self.ui.tree.topLevelItemCount() - 1
    
    def on_pre_button_clicked(self):
        self.ui.tree.setCurrentItem(self.ui.tree.topLevelItem(self.ui.tree.indexOfTopLevelItem(self.ui.tree.currentItem()) - 1))
        self.on_tree_item_double_clicked()

    def on_next_button_clicked(self):     
        self.ui.tree.setCurrentItem(self.ui.tree.topLevelItem(self.ui.tree.indexOfTopLevelItem(self.ui.tree.currentItem()) + 1))
        self.on_tree_item_double_clicked()

    def save_data(self):
        save_dataset(self.ui.annotateUserEditer.text())

    def on_annotate_user_editer_text_changed(self):
        mw = self.p
        plg = mw.plugins['LabelIhepPlugin']
        plg.set_annotate_user(self.ui.annotateUserEditer.text())

        
        

    


    

    

        


