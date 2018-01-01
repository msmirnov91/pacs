import os

from PyQt4 import uic
from PyQt4.QtGui import QDialog, QFileDialog

from IO.storage_manager import StorageManager


class LoadWidget(QDialog):
    def __init__(self, parent=None):
        super(LoadWidget, self).__init__(parent)
        uic.loadUi("IO/gui/load_dialog.ui", self)

        self.btn_choose.clicked.connect(self.choose)

    def choose(self):
        dialog = QFileDialog()
        raw_files_dir = os.path.join(StorageManager.STORAGE_DIR, StorageManager.RAW_FILES_DIR)
        file_name = dialog.getOpenFileName(self, 'Open file with data', raw_files_dir)
        self.le_path.setText(file_name)

    def accept(self):
        name = self.le_name.text()
        if name is None or name == "":
            self.close()
            return self.Rejected

        path = self.le_path.text()
        comment = self.le_comment.text()
        StorageManager().load(path=path, name=name, comment=comment)
        self.close()
