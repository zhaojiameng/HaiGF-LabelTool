
from HaiGF import HMainSideBarWidget, HAction
from ..widgets.msb_ui import Ui_Form


class AntrainMSBWidget(HMainSideBarWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.p = parent


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
        plg.create_anno()

    def updateRoiType(self):
        mw = self.p
        plg = mw.plugins['AntrainPlugin']
        plg.updateRoiType(self.ui.roiComboBox.currentText())

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

    

        


