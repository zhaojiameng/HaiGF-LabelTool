
from HaiGF import HMainSideBarWidget, HAction
from HaiGF.gui_framework.widgets.main_side_bar.explorer_widget import ExplorerWidget
from ..widgets.msb_ui import Ui_Form



class AntrainMSBWidget(HMainSideBarWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent
        self.annoShape = 'Line ROI'
        self.upload_type = 0 #0：显示掩码，1：检测， 2：分割


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

        self.ui.label_type.currentTextChanged.connect(self.on_label_type_changed)

        self.ui.seg_group.buttonClicked.connect(self.on_seg_group_clicked)
        # self.ui.seg_anything.clicked.connect(self.on_seg_anything_clicked)
        self.ui.uploadButton.clicked.connect(self.on_uploadButton_clicked)
        self.ui.uploadType.currentTextChanged.connect(self.change_upload_type)
        self.ui.enable_sam_button.clicked.connect(self.on_enable_sam_button_clicked)
        self.ui.enable_label_button.clicked.connect(self.on_enable_label_button_clicked)
        self.ui.save_improve_button.clicked.connect(self.on_save_improve_button_clicked)
        self.ui.clear_prompt.clicked.connect(self.on_clear_prompt_button_clicked)
        self.ui.reset_screen_button.clicked.connect(self.on_reset_screen_button_clicked)

        # self.set_input_none()
        
    def change_upload_type(self):
        if self.ui.uploadType.currentText() == "显示掩码":
            self.upload_type = 0
        elif self.ui.uploadType.currentText() == "检测":
            self.upload_type = 1
        elif self.ui.uploadType.currentText() == "分割":
            self.upload_type = 2
        else:
            self.upload_type = 0


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
        self.on_save_improve_button_clicked()
        mw = self.p
        key = list(mw.main_side_bar._aw_dict.keys())[0]
        widget = mw.main_side_bar._aw_dict[key]
        tree = widget.tree
        assert tree is not None
        tree.cope_pre_button()
        self.set_input_none()
        self.on_enable_label_button_clicked()
        # self.on_clear_prompt_button_clicked()
       
       

    def on_proButton_clicked(self):
        #调用gui_framework中main_side_bar下explorer_widget中的on_proButton_clicked
        self.on_save_improve_button_clicked()
        mw = self.p
        #取得mw中的main_side_bar中的_aw_dicts中的第一个key
        key = list(mw.main_side_bar._aw_dict.keys())[0]
        widget = mw.main_side_bar._aw_dict[key]
        tree = widget.tree
        assert tree is not None
        tree.cope_pro_button()
        self.set_input_none()
        self.on_enable_label_button_clicked()
        # self.on_clear_prompt_button_clicked()
        

    def on_label_type_changed(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.update_label_type(self.ui.label_type.currentText())

    def on_seg_group_clicked(self, button=None):
        mode = 0
        if button == self.ui.seg_point:
            self.ui.seg_point.setChecked(True)
            self.ui.seg_box.setChecked(False)
            self.ui.seg_anything.setChecked(False)
            mode = 1
        elif button == self.ui.seg_box:
            self.ui.seg_point.setChecked(False)
            self.ui.seg_box.setChecked(True)
            self.ui.seg_anything.setChecked(False)
            mode = 2
        else:
            self.ui.seg_point.setChecked(False)
            self.ui.seg_box.setChecked(False)
            self.ui.seg_anything.setChecked(True)
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.update_prompt_mode(mode)
        if mode == 0:
            plg.clear_prompt()
            plg.predict_sam(self.upload_type)

    def on_uploadButton_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        # if plg.upload():
        #     self.set_input_mode_enabled(True)
        plg.predict_sam(self.upload_type)

    def set_input_mode_enabled(self, enabled):
        if not enabled:
            # self.ui.seg_group.setExclusive(False)
            self.ui.seg_point.setChecked(False)
            self.ui.seg_box.setChecked(False)
            self.ui.seg_anything.setChecked(True)
            mw = self.p
            plg = mw.plugins['AntrainPlugin']
            plg.update_prompt_mode(0)
        self.ui.seg_point.setEnabled(enabled)
        self.ui.seg_box.setEnabled(enabled)
        self.ui.seg_anything.setEnabled(enabled)
        self.ui.uploadButton.setEnabled(enabled)


    def set_input_none(self):
        # self.on_seg_group_clicked()
        self.set_input_mode_enabled(self.ui.enable_sam_button.isChecked())

    def on_enable_sam_button_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        self.set_input_mode_enabled(self.ui.enable_sam_button.isChecked())
        plg.enable_sam(self.ui.enable_sam_button.isChecked())
        
    def enable_sam_button(self, enabled):
        self.ui.enable_sam_button.setEnabled(enabled)   

    def on_seg_anything_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.clear_prompt()
        self.on_seg_group_clicked()
        # plg.update_prompt_mode(0)
        plg.predict_sam(self.upload_type)

    def on_enable_label_button_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.enable_label(self.ui.enable_label_button.isChecked())

    def on_save_improve_button_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.save_improve(self.ui.save_improve_button.isChecked())
    
    def on_clear_prompt_button_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        # print('clear prompt')
        plg.clear_prompt()

    def on_reset_screen_button_clicked(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.reset_screen()


    

        


