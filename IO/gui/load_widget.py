from PyQt4 import uic
from PyQt4.QtGui import QDialog, QFileDialog

from IO import *


class LoadWidget(QDialog):
    def __init__(self, parent=None):
        super(LoadWidget, self).__init__(parent)
        uic.loadUi("IO/gui/load_dialog.ui", self)

        self.btn_choose.clicked.connect(self.choose)

    def choose(self):
        dialog = QFileDialog()
        file_name = dialog.getOpenFileName(self, 'Open file with data', RAW_FILES_DIR)
        self.le_path.setText(file_name)

    def get_new_data_info(self):
        return self.le_path.text(), self.le_name.text(), self.le_comment.text()

    def accept(self):
        name = self.le_name.text()
        if name is None or name == "":
            super(LoadWidget, self).reject()

        super(LoadWidget, self).accept()
