import re

# from qtpy import QT_VERSION
# from qtpy import QtCore
# from qtpy import QtGui
# from qtpy import QtWidgets

from PySide2 import QtCore, QtWidgets, QtGui
from hai_gui.logger import logger
import hai_gui.utils

QT_VERSION = ['5']
QT5 = QT_VERSION[0] == "5"


# TODO(unknown):
# - Calculate optimal position so as not to go out of screen area.


class LabelQLineEdit(QtWidgets.QLineEdit):
    def setListWidget(self, list_widget):
        self.list_widget = list_widget

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]:
            self.list_widget.keyPressEvent(e)
        else:
            super(LabelQLineEdit, self).keyPressEvent(e)

def load_LabelDialog(self):
    return LabelDialog(
            parent=self,
            labels=self._config["labels"],
            sort_labels=self._config["sort_labels"],
            show_text_field=self._config["show_label_text_field"],
            completion=self._config["label_completion"],
            fit_to_content=self._config["fit_to_content"],
            flags=self._config["label_flags"],
            lngg=self.lngg,
            )
            

class LabelDialog(QtWidgets.QDialog):
    def __init__(
        self,
        text="Enter object label",
        parent=None,
        labels=None,
        sort_labels=True,
        show_text_field=True,
        completion="startswith",
        fit_to_content=None,
        flags=None,
        lngg=None
    ):
        if fit_to_content is None:
            fit_to_content = {"row": False, "column": True}
        self._fit_to_content = fit_to_content

        super(LabelDialog, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()  # 整个对话框的layout
        # 1.编辑目标类别区域
        class_tag = QtWidgets.QLabel(f'{f"{lngg.ldiag_class}"}: ')
        self.edit = LabelQLineEdit()
        self.edit.setPlaceholderText(lngg.ldiag_class_holder)
        self.edit.setValidator(hai_gui.utils.labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        if flags:
            self.edit.textChanged.connect(self.updateFlags)
        self.edit_group_id = QtWidgets.QLineEdit()
        self.edit_group_id.setPlaceholderText(f"{lngg.ldiag_class_groupid_holder}")
        self.edit_group_id.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r"\d*"), None)
        )
        if show_text_field:
            layout_edit = QtWidgets.QHBoxLayout()
            layout_edit.addWidget(class_tag)
            layout_edit.addWidget(self.edit, 6)
            layout_edit.addWidget(self.edit_group_id, 2)
            layout.addLayout(layout_edit)

        # 2.目标跟踪id
        tid_tag = QtWidgets.QLabel(f'{lngg.ldiag_tid:>8}: ')
        self.tid_edit = LabelQLineEdit()
        self.tid_edit.setPlaceholderText(lngg.ldiag_tid_holder)
        self.tid_edit.editingFinished.connect(self.tid_postProcess)
        self.tid_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"\d*"), None))
        # self.tid_edit.setMaximumSize(10)
        layout_tid = QtWidgets.QHBoxLayout()
        layout_tid.addWidget(tid_tag)
        layout_tid.addWidget(self.tid_edit)
        layout_tid.addWidget(QtWidgets.QLabel(f'{"":>80}'))
        layout.addLayout(layout_tid)

        # 3. 目标状态类别
        status_tag = QtWidgets.QLabel(f'{lngg.ldiag_status:<6}: ')
        self.status_edit = LabelQLineEdit()
        self.status_edit.setPlaceholderText(lngg.ldiag_status_holder)
        self.status_edit.editingFinished.connect(self.status_postProcess)
        self.status_edit.setValidator(hai_gui.utils.labelValidator())
        self.status_group_id = QtWidgets.QLineEdit()
        self.status_group_id.setPlaceholderText(lngg.ldiag_status_groupid_holder)
        self.status_group_id.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"\d*"), None))
        layout_status = QtWidgets.QHBoxLayout()
        layout_status.addWidget(status_tag)
        layout_status.addWidget(self.status_edit, 6)
        layout_status.addWidget(self.status_group_id, 2)
        layout.addLayout(layout_status)

        # 4. buttons
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
        )
        bb.button(bb.Ok).setIcon(hai_gui.utils.newIcon("done"))
        bb.button(bb.Cancel).setIcon(hai_gui.utils.newIcon("undo"))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        # 5.label_list 和status list
        self.labelList = QtWidgets.QListWidget()
        self.statusList = QtWidgets.QListWidget()
        if self._fit_to_content["row"]:  # 按行fit内容
            self.labelList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.statusList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        if self._fit_to_content["column"]:  # 按列
            self.labelList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.statusList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._sort_labels = sort_labels
        if labels:
            self.labelList.addItems(labels)
            # TODO 状态List的item
        if self._sort_labels:
            self.labelList.sortItems()
            self.statusList.sortItems()
        else:
            self.labelList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
            self.statusList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # 目标类别列表的触发
        self.labelList.currentItemChanged.connect(self.labelSelected)
        self.labelList.itemDoubleClicked.connect(self.labelDoubleClicked)
        self.edit.setListWidget(self.labelList)
        # 状态列表的触发
        self.statusList.currentItemChanged.connect(self.statusLabelSelected)
        # self.statusList.itemDoubleClicked.connect(self.statusLabelDoubleClicked)  # TODO 双击触发没写
        self.status_edit.setListWidget(self.statusList)
        # 两个列表组成布局
        layout_list = QtWidgets.QHBoxLayout()
        layout_list.addWidget(self.labelList)
        layout_list.addWidget(self.statusList)
        # layout.addWidget(self.labelList)
        layout.addLayout(layout_list)

        # label_flags
        if flags is None:
            flags = {}
        self._flags = flags
        self.flagsLayout = QtWidgets.QVBoxLayout()
        self.resetFlags()
        layout.addItem(self.flagsLayout)
        self.edit.textChanged.connect(self.updateFlags)
        self.setLayout(layout)
        # completion 自动补全
        completer = QtWidgets.QCompleter()
        status_completer = QtWidgets.QCompleter()
        if not QT5 and completion != "startswith":
            logger.warn(
                "completion other than 'startswith' is only "
                "supported with Qt5. Using 'startswith'"
            )
            completion = "startswith"
        if completion == "startswith":
            completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
            status_completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
            # Default settings.
            # completer.setFilterMode(QtCore.Qt.MatchStartsWith)
        elif completion == "contains":
            completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            completer.setFilterMode(QtCore.Qt.MatchContains)
            status_completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            status_completer.setFilterMode(QtCore.Qt.MatchContains)
        else:
            raise ValueError("Unsupported completion: {}".format(completion))
        completer.setModel(self.labelList.model())
        status_completer.setModel(self.statusList.model())
        self.edit.setCompleter(completer)
        self.status_edit.setCompleter(status_completer)

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

    def popUp(self, text=None, move=True, flags=None, group_id=None,
              tid_text=None, status_text=None, status_group_id=None):
        # print(f'popup: text: {text} {move} {flags} {group_id} tid: {tid_text} {status_text} {status_group_id}')
        # 这后面自带了补全算法，就是tid什么的为None时，自动补全上次传入的了
        if self._fit_to_content["row"]:
            self.labelList.setMinimumHeight(
                self.labelList.sizeHintForRow(0) * self.labelList.count() + 2)
            self.statusList.setMinimumHeight(
                self.statusList.sizeHintForRow(0) * self.statusList.count() + 2)
        if self._fit_to_content["column"]:
            self.labelList.setMinimumWidth(self.labelList.sizeHintForColumn(0) + 2)
            self.statusList.setMinimumWidth(self.statusList.sizeHintForColumn(0) + 2)
        # if text is None, the previous label in self.edit is kept
        if text is None:
            text = self.edit.text()
        tid_text = str(tid_text) if tid_text else self.tid_edit.text()
        status_text = status_text if status_text else self.status_edit.text()
        if flags:
            self.setFlags(flags)
        else:
            self.resetFlags(text)
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.tid_edit.setText(str(tid_text))
        self.tid_edit.setSelection(0, len(tid_text))
        self.status_edit.setText(status_text)
        self.status_edit.setSelection(0, len(status_text))

        if group_id is None:
            self.edit_group_id.clear()
        else:
            self.edit_group_id.setText(str(group_id))
        if status_group_id is None:
            self.status_group_id.clear()
        else:
            self.status_group_id.setText(str(status_group_id))

        # 同步edit控件和labelList的选择项
        items = self.labelList.findItems(text, QtCore.Qt.MatchFixedString)  # 从labelList中按text匹配Item
        if items:
            if len(items) != 1:
                logger.warning("Label list has duplicate '{}'".format(text))
            self.labelList.setCurrentItem(items[0])  # 聚焦到该item，就是edit和labelList的同步
            row = self.labelList.row(items[0])
            self.edit.completer().setCurrentRow(row)
        # 同步status空间和statusList的选择项
        s_items = self.statusList.findItems(status_text, QtCore.Qt.MatchFixedString)
        if s_items:
            if len(s_items) != 1:
                logger.warning(f"Status label has duplicate {status_text}")
            self.statusList.setCurrentItem(s_items[0])
            srow = self.statusList.row(s_items[0])
            self.status_edit.completer().setCurrentRow(srow)

        self.edit.setFocus(QtCore.Qt.PopupFocusReason)  # 设置聚焦
        if move:
            self.move(QtGui.QCursor.pos())
        if self.exec_():
            cls, flags, gid = self.edit.text(), self.getFlags(), self.getGroupId()
            tid, status, sgid = self.tid_edit.text(), self.status_edit.text(), self.getStatusGroupId()
            tid = int(tid) if tid else 0
            return cls, flags, gid, tid, status, sgid
            # return self.edit.text(), self.getFlags(), self.getGroupId(), self.tid_edit.text(), self.status_edit.
        else:
            return None, None, None, None, None, None
