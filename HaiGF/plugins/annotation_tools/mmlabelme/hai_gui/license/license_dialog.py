import os, sys
import re
from pathlib import Path

# from qtpy import QT_VERSION
# from qtpy import QtCore
# from qtpy import QtGui
# from qtpy import QtWidgets
# from qtpy.QtWidgets import QFrame

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame

from hai_gui import __version__, __appname__
from hai_gui.logger import logger
import hai_gui.utils
from .license import License

pydir = f'{Path(os.path.abspath(__file__)).parent}'

QT_VERSION = ['5']
QT5 = QT_VERSION[0] == "5"


class LabelQLineEdit(QtWidgets.QLineEdit):
    def setListWidget(self, list_widget):
        self.list_widget = list_widget

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]:
            self.list_widget.keyPressEvent(e)
        else:
            super(LabelQLineEdit, self).keyPressEvent(e)

def load_LicenseDialog(self):
    return LicenseDialog(
            parent=self,
            lngg=self.lngg,)

class LicenseDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent=None,
        lngg=None
    ):
        super(LicenseDialog, self).__init__(parent)
        self.parent = parent
        self.license = License()
        self.lngg = lngg
        self.lic_path = f'{pydir}/license.lic'

        self._status = False
        self._expiration_time = None
        self._mac = None

        self._init_dialog()

    def _init_dialog(self):
        lngg = self.lngg

        self.setWindowTitle(f'证书License')

        layout = QtWidgets.QVBoxLayout()  # 总体是水平布局
        # 1.第1层，信息和Info
        layout_top = QtWidgets.QHBoxLayout()
        layout_top.addWidget(QtWidgets.QLabel('证书信息: '))
        layout_top.addWidget(QtWidgets.QLabel('Information: '))
        layout.addLayout(layout_top)
        # 2.第2层，中英文信息
        layout_up = QtWidgets.QHBoxLayout()  # 第一层
        self.infoLabel_zh = QtWidgets.QLabel("这里是激活信息")
        self.infoLabel_zh.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.infoLabel_zh.setLineWidth(3)
        seprator = QtWidgets.QFrame()
        seprator.setFrameShape(QFrame.HLine)
        # 英文激活信息
        self.infoLabel_en = QtWidgets.QLabel("Here is the activate info")
        self.infoLabel_en.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.infoLabel_en.setLineWidth(3)
        layout_up.addWidget(self.infoLabel_zh)
        # layout_up.addWidget(seprator)
        layout_up.addWidget(self.infoLabel_en)
        layout.addLayout(layout_up)

        # 3.指纹码生成栏
        self.fcode_label = QtWidgets.QLabel(f'指纹码/Fingerprint Code: ')
        self.fcode_edit = LabelQLineEdit()
        # self.finfo_edit = QtWidgets.QPlainTextEdit()
        # fcode = f"EWy9v44C1YzTmvkdwEaTwg93uP428YystxCqmaQcMOtF+v+bLLABU2hqpyM0Fj7DQfEnH4Ko8p8Qbq4oAF6t6Hagjs2SkYiudsuu465ElolS4gxq21GKzIHTkSs8hStsa0WdmmJvDLX1swoHCaZx9U34GjA8B6esCB7AN+Ojv8w="
        self.fcode_edit.setPlaceholderText(f'复制指纹码')
        self.fcode_edit.setText('')
        self.fcode_label.hide()
        self.fcode_edit.hide()
        layout.addWidget(self.fcode_label)
        layout.addWidget(self.fcode_edit)

        # 4.激活码输入栏
        self.acode_label = QtWidgets.QLabel(f'激活码/Activation Code: ')
        self.edit = LabelQLineEdit()
        # self.edit = QtWidgets.QPlainTextEdit()
        self.edit.setPlaceholderText(f'粘贴激活码到此处/Paste the activation code here')
        self.edit.hide()
        layout.addWidget(self.acode_label)
        layout.addWidget(self.edit)

        # 3.按钮
        button_layout = QtWidgets.QHBoxLayout()
        self.fcodeBtn = QtWidgets.QPushButton(f'获取指纹码/Get FCode')
        self.activateBtn = QtWidgets.QPushButton(f'点击激活/&Go to Activate')
        self.activateBtn.setEnabled(False)
        # self.activateBtn.hide()
        button_layout.addWidget(self.fcodeBtn)
        button_layout.addWidget(self.activateBtn)
        layout.addLayout(button_layout)

        # 下半部分
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Close,
            QtCore.Qt.Horizontal,
            self)
        bb.button(bb.Close).setIcon(hai_gui.utils.newIcon("close"))
        bb.button(bb.Cancel).setText(f'&Exit')
        # bb.Cancel.clicked.connect(self._exit())
        # bb.accepted.connect(self.validate)
        bb.clicked.connect(self.bb_clicked)
        # bb.rejected.connect(self._exit)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        self.setLayout(layout)

        # 槽
        self.fcodeBtn.clicked.connect(self.get_fcode)
        self.edit.editingFinished.connect(self.editing_finished)
        # self.edit.modificationChanged.connect(self.editing_finished)
        self.edit.textEdited.connect(self.text_edited)
        self.activateBtn.clicked.connect(self.activate)
        self.rejected.connect(self.must_activated)

    def addLabelHistory(self, label):
        if self.labelList.findItems(label, QtCore.Qt.MatchExactly):
            return
        self.labelList.addItem(label)
        if self._sort_labels:
            self.labelList.sortItems()

    def addStatusHistory(self, status):
        if self.statusList.findItems(status, QtCore.Qt.MatchExactly):
            return
        self.statusList.addItem(status)
        if self._sort_labels:
            self.statusList.sortItems()

    def labelSelected(self, item):
        self.edit.setText(item.text())

    def statusLabelSelected(self, item):
        self.status_edit.setText(item.text())

    def validate(self):
        text = self.edit.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        if text:
            self.accept()

    def labelDoubleClicked(self, item):
        self.validate()

    def postProcess(self):
        text = self.edit.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        self.edit.setText(text)

    def tid_postProcess(self):
        text = self.tid_edit.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        self.tid_edit.setText(text)

    def status_postProcess(self):
        text = self.status_edit.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        self.status_edit.setText(text)

    def updateFlags(self, label_new):
        # keep state of shared flags
        flags_old = self.getFlags()

        flags_new = {}
        for pattern, keys in self._flags.items():
            if re.match(pattern, label_new):
                for key in keys:
                    flags_new[key] = flags_old.get(key, False)
        self.setFlags(flags_new)

    def deleteFlags(self):
        for i in reversed(range(self.flagsLayout.count())):
            item = self.flagsLayout.itemAt(i).widget()
            self.flagsLayout.removeWidget(item)
            item.setParent(None)

    def resetFlags(self, label=""):
        flags = {}
        for pattern, keys in self._flags.items():
            if re.match(pattern, label):
                for key in keys:
                    flags[key] = False
        self.setFlags(flags)

    def setFlags(self, flags):
        self.deleteFlags()
        for key in flags:
            item = QtWidgets.QCheckBox(key, self)
            item.setChecked(flags[key])
            self.flagsLayout.addWidget(item)
            item.show()

    def getFlags(self):
        flags = {}
        for i in range(self.flagsLayout.count()):
            item = self.flagsLayout.itemAt(i).widget()
            flags[item.text()] = item.isChecked()
        return flags

    def getGroupId(self):
        group_id = self.edit_group_id.text()
        if group_id:
            return int(group_id)
        return None

    def getStatusGroupId(self):
        sgid = self.status_group_id.text()
        if sgid:
            return int(sgid)
        return None

    @property
    def mac(self):
        return self._mac

    @property
    def status(self):
        return self._status

    @property
    def expiration_time(self):
        return self._expiration_time

    @property
    def activation_info(self):

        zh_status = '已激活' if self.status else '未激活'
        en_status = 'Activated' if self.status else 'Not activated'
        zh_info = f'{"软件名: hai-gui":<30}\n' \
                  f'版本: {__version__}\n' \
                  f'激活状态: {zh_status}\n' \
                  f'有效期限: {self.expiration_time}'
        en_pad = 1
        en_info = f'{"Software name":>{en_pad}}: {__appname__}\n' \
                  f'{"Version":>{en_pad}}: {__version__}\n' \
                  f'{"Status":>{en_pad}}: {en_status}\n' \
                  f'{"Expiration time":>{en_pad}}: {self.expiration_time}'
        return (zh_info, en_info)

    def bb_clicked(self, btn):
        if btn.text() == '&Exit':
            print('Exit.')
            exit()

    def reset(self):
        """默认是未激活状态"""
        self.fcode_edit.setText('')
        self.fcode_edit.hide()
        self.fcode_label.hide()
        self.activateBtn.setText(f'点击激活/Go to Activate')
        self.activateBtn.setEnabled(False)
        self.fcodeBtn.setEnabled(True)
        self.edit.setEnabled(True)
        self.edit.setText('')
        self.edit.show()
        self.activateBtn.setFocus()

        # 未激活状态无法关闭
        # self.buttonBox.Close.setEnabled(False)

    def popUp(self):
        self.reset()
        # 更新激活信息文本
        zh_info, en_info = self.activation_info
        self.infoLabel_zh.setText(zh_info)
        self.infoLabel_en.setText(en_info)

        status = self.status
        exp_time = self.expiration_time
        if status:  # True TODO
            self.edit.hide()
            self.acode_label.hide()
            self.fcodeBtn.setEnabled(False)
            # self.buttonBox.Close.setFocus()
            self.activateBtn.setEnabled(False)
            self.activateBtn.setText(f'已激活/Activated')
        else:
            # acode = f"FeF4pKaZOtaWSEp9Ua0CLiL4aFBWzizS6h9HQoEPZ69KvU8T581KMzu6hRDE5swN8bkARo2bMlNdvmYgucy7EbhPMm4484b1qamCkmyOZiH1DMolSXp7+NNaTHMc3qtfCSxq31s8IzoIiVtBuFH3zkmOBrE0Pk3PSgbVqvimlbwMAbpo5xbgEXXg2CPKcyezxFXhBGe6KA/p3mAGnx0ySVNfv8DaPc1rer/oIMXoQUmntzFb8lvqVg6w+LVEvLjeS9b9FzlFKaufyRjRKMHDdTgYka+kow4ObZAtDkUeEMkluc2Phwj64Z6DltXjuLHcoz0nHsu2VhUOmhWPPC1of3C0gOpKw+Oh1hM4+fbWHcpixiUA1thsjHO3jgKn40C2C/RQtkQ+srqWd2JVse48vECQouuupJOmTDHZZn7I5/Z/x/UI7OCNp1byRs54d5Nelhz2xlwl39grm7gNxtU/1r/OiTp+FG92cEu4OcxpKgIgllHlovralMSU/I9u3whE"
            # self.edit.setText(acode)
            acode = self.edit.text()
            if acode == '':
                self.edit.setFocus()
            # else:
            #     self.activateBtn.

        if self.exec_():
            return self.status
        else:
            return self.status

    def check_license(self):
        passed, message = self.license.verify_license()
        # 无证书、秘钥不对、证书失效等都会返回False
        return passed

    def get_fcode(self):
        fcode = self.license.gen_fcode()
        self.fcode_edit.setText(fcode)
        self.fcode_label.show()
        self.fcode_edit.show()

    def text_edited(self):
        # self.activateBtn.setFocus()
        self.edit.setFocus()
        self.activateBtn.setEnabled(True)

    def editing_finished(self):
        self.activateBtn.setFocus()

    def activate(self):
        """点击激活按钮的槽"""
        # print('activating')
        acode = self.edit.text()
        print(f'acode: {acode}')
        ret = self.license.register(acode=acode)
        if ret:
            QtWidgets.QMessageBox.information(
                self,
                self.tr('Success!'),
                self.tr('激活成功！/Successfully activated！'))
            self.update_activate_info()
            self.popUp()
            self.acode_label.show()
            self.edit.show()
            self.edit.setEnabled(False)
            # self.popUp()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                self.tr('Failed'),
                self.tr("激活码错误，激活失败/Activate Failed."))

    def update_activate_info(self):
        """
        更新激活信息
        :return:
        """
        passed, message = self.license.verify_license()
        if passed:
            # print(f'massage: {message}')
            message = [x.split('=') for x in message.split(';')]
            self._status = True
            self._mac = None
            self._expiration_time = message[2][1]
        else:
            self._status = False
            self._mac = None
            self._expiration_time = None

    def must_activated(self):
        """rejected的槽，必须激活"""
        if self.status:
            pass
        else:
            QtWidgets.QMessageBox.warning(
                self,
                self.tr('Failed'),
                self.tr("请先激活软件/Please Activate The Software."))




