from PyQt4 import uic
from PyQt4.QtGui import *


class AbstractSettingsWidget(QWidget):
    settings_for_algorithm = None

    def __init__(self, ui_file, parent=None):
        self.parent = parent
        super(AbstractSettingsWidget, self).__init__(parent)
        uic.loadUi(ui_file, self)

    def get_settings(self):
        return {}
