import os

from PyQt4 import uic
from PyQt4.QtGui import QDialog, QStandardItemModel, QStandardItem


class StartDialog(QDialog):
    def __init__(self, session_dir, parent=None):
        super(StartDialog, self).__init__(parent)
        self.session_dir = session_dir
        uic.loadUi("Main/StartDialog/start_dialog.ui", self)
        self._fill_sessions_list()

        self.new_session_rb.toggled.connect(self._update_widget)
        self.old_session_rb.toggled.connect(self._update_widget)

    def _fill_sessions_list(self):
        data_list_model = QStandardItemModel(self.existing_sessions_list)
        names = os.listdir(self.session_dir)
        for name in names:
            item = QStandardItem(name)
            data_list_model.appendRow(item)
        self.existing_sessions_list.setModel(data_list_model)

    def _update_widget(self):
        if self.new_session_rb.isChecked():
            self.new_session_gb.setEnabled(True)
            self.old_session_gb.setEnabled(False)
        elif self.old_session_rb.isChecked():
            model = self.existing_sessions_list.model()
            if model.rowCount() == 0:
                return
            self.new_session_gb.setEnabled(False)
            self.old_session_gb.setEnabled(True)

    def get_session_name(self):
        if self.new_session_rb.isChecked():
            return self.new_session_name_le.text()
        elif self.old_session_rb.isChecked():
            selected_items = self.existing_sessions_list.selectedIndexes()
            if selected_items:
                return selected_items[0].data()

    def get_recorder_dir(self):
        return os.path.join(self.session_dir, self.get_session_name(), "Report")
