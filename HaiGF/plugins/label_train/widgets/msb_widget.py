
from HaiGF import HMainSideBarWidget, HAction
from HaiGF.gui_framework.widgets.main_side_bar.explorer_widget import ExplorerWidget
from ..widgets.msb_ui import Ui_Form



class AntrainMSBWidget(HMainSideBarWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        self.annoShape = 'Line ROI'


        self.set_title(self.tr('Annotation and Train Tools'))

        title_actions = [
            HAction(text='test antrain', parent=self.p, slot=None),]
        self.set_title_actions(title_actions)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.runButton.clicked.connect(self.on_cannyPutton_clicked)
        self.ui.runButton1.clicked.connect(self.on_cancel_cannyButton_clicked)
        self.ui.annoButton.clicked.connect(self.on_annoButton_clicked)
        self.ui.roiComboBox.currentTextChanged.connect(self.updateRoiType)
        self.ui.roiButton.clicked.connect(self.on_roiButton_clicked)
        self.ui.roiButton1.clicked.connect(self.on_cancel_roiButton_clicked)

        self.ui.isoButton.clicked.connect(self.on_isoButton_clicked)
        self.ui.isoButton1.clicked.connect(self.on_cancel_isoButton_clicked)

        self.ui.pre_button.clicked.connect(self.on_preButton_clicked)
        self.ui.pro_button.clicked.connect(self.on_proButton_clicked)

    def on_cannyPutton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.canny_detect(self.ui.threshold1SpinBox.value(), self.ui.threshold2SpinBox.value())

    def on_cancel_cannyButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.cancel_canny()

    def on_annoButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.create_anno(self.annoShape)

    def updateRoiType(self):
        self.annoShape = self.ui.roiComboBox.currentText()
        # mw = self.p
        # plg = mw.plugins['AntrainPlugin']
        # plg.updateRoiType(self.ui.roiComboBox.currentText())

    def on_roiButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.create_ROI()

    def on_cancel_roiButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.cancel_ROI()

    def on_isoButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.analysis_iso()

    def on_cancel_isoButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.cancel_iso()

    def on_preButton_clicked(self):
        #调用gui_framework中main_side_bar下explorer_widget中的on_preButton_clicked
        mw = self.p
        key = list(mw.main_side_bar._aw_dict.keys())[0]
        widget = mw.main_side_bar._aw_dict[key]
        tree = widget.tree
        assert tree is not None
        tree.cope_pre_button()

    def on_proButton_clicked(self):
        #调用gui_framework中main_side_bar下explorer_widget中的on_proButton_clicked
        mw = self.p
        #取得mw中的main_side_bar中的_aw_dicts中的第一个key
        key = list(mw.main_side_bar._aw_dict.keys())[0]
        widget = mw.main_side_bar._aw_dict[key]
        tree = widget.tree
        assert tree is not None
        tree.cope_pro_button()

    

        


