import re

from PyQt4 import uic
from PyQt4.QtGui import QDialog

from IO.storage_manager import StorageManager
from Main.tabs.Info.data_info_tab import DataInfoTab


class SaveWidget(QDialog):
    def __init__(self, data, parent=None):
        super(SaveWidget, self).__init__(parent)
        uic.loadUi("IO/gui/save_dialog.ui", self)
        self.info_tab = DataInfoTab()
        self._data = data

        self.form_layout.addWidget(self.info_tab)
        self.info_tab.enable_fields()
        self.info_tab.update_tab(self._data)

    def get_name_and_comment(self):
        return self.info_tab.le_name.text(), self.info_tab.le_comment.text()

    def accept(self):
        pattern = '[0-9a-zA-Z_:\\.\\-]+$'
        name = self.info_tab.le_name.text()

        if re.match(pattern, name):
            print("match")
            super(SaveWidget, self).accept()
            return
        super(SaveWidget, self).reject()
