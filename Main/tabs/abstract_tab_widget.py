import os

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignal

from Visualizer.visualizer import Visualizer
from Processor.processor import Processor


class AbstractTab(QWidget):
    data_update_required = pyqtSignal()

    def __init__(self, ui_file, parent=None):
        super(AbstractTab, self).__init__(parent)
        self.name = None
        self.need_two_data_sets = False
        self.index_val_pattern = "{:4.2f}"
        ui_path = self.get_full_path(ui_file)
        uic.loadUi(ui_path, self)

        self.visualizer = Visualizer()
        self.processor = Processor()

    def get_full_path(self, ui_rel_path):
        path_to_current_script = os.path.dirname(__file__)
        return os.path.join(path_to_current_script, ui_rel_path)

    def change_visualization_widget_to(self, new_widget):
        self._change_widget_on_layout_to(self.plot_layout, new_widget)

    @classmethod
    def _change_widget_on_layout_to(cls, layout, new_widget):
        curr_widget_item = layout.takeAt(0)
        if curr_widget_item is not None:
            curr_widget = curr_widget_item.widget()
            layout.removeWidget(curr_widget)
            curr_widget.deleteLater()
        layout.addWidget(new_widget)

    def update_tab(self, data):
        pass

    def emit_update_required_signal(self):
        self.data_update_required.emit()
