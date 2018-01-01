import os

from PyQt4 import uic
from PyQt4.QtGui import *

from Processor.processor import Processor


class AbstractTab(QWidget):
    def __init__(self, ui_file, parent=None):
        super(AbstractTab, self).__init__(parent)
        self.name = None
        ui_path = self.get_full_path(ui_file)
        uic.loadUi(ui_path, self)

        # lack_of_the_time
        self.is_visualization_tab = False
        self.processor = Processor()

    @classmethod
    def get_full_path(cls, ui_rel_path):
        path_to_current_script = os.path.dirname(__file__)
        return os.path.join(path_to_current_script, ui_rel_path)

    @classmethod
    def _change_widget_on_layout_to(cls, layout, new_widget):
        curr_widget_item = layout.takeAt(0)
        if curr_widget_item is not None:
            curr_widget = curr_widget_item.widget()
            layout.removeWidget(curr_widget)
            curr_widget.deleteLater()
        layout.addWidget(new_widget)
