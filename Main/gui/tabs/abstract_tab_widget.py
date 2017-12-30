import os
from PyQt4 import uic
from PyQt4.QtGui import *


class AbstractTab(QWidget):
    def __init__(self, ui_file, parent=None):
        super(AbstractTab, self).__init__(parent)
        self.name = None
        self.index_val_pattern = "{:4.2f}"
        ui_path = self.get_full_path(ui_file)
        uic.loadUi(ui_path, self)
        self.adjustVisualizer()

    def get_full_path(self, ui_rel_path):
        path_to_current_script = os.path.dirname(__file__)
        return os.path.join(path_to_current_script, ui_rel_path)

    def adjustVisualizer(self):
        pass


