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

    def accept(self):
        name = self.info_tab.le_name.text()
        if name is None or name == "":
            self.close()
            return self.Rejected

        self._data.data_name = name
        self._data.clustering_alg_name = self.info_tab.le_alg.text()
        self._data.clustering_alg_params = self.info_tab.le_alg_param.text()
        self._data.user_comment = self.info_tab.le_comment.text()

        StorageManager().store(self._data)
        self.close()
