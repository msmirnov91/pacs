import os

from PyQt4 import uic
from PyQt4.QtGui import *

from Visualizer.visualizer import Visualizer
from Processor.processor import Processor


class AbstractTab(QWidget):
    def __init__(self, ui_file, parent=None):
        super(AbstractTab, self).__init__(parent)
        self.name = None
        self.need_two_data_sets = False
        self.index_val_pattern = "{:4.2f}"
        ui_path = self.get_full_path(ui_file)
        uic.loadUi(ui_path, self)
        self.visualizer = Visualizer()
        self.processor = Processor()
        self.adjustVisualizer()

    def get_full_path(self, ui_rel_path):
        path_to_current_script = os.path.dirname(__file__)
        return os.path.join(path_to_current_script, ui_rel_path)

    def adjustVisualizer(self):
        pass

    def change_visualization_widget_to(self, new_widget):
        curr_widget_item = self.plot_layout.takeAt(0)
        if curr_widget_item is not None:
            curr_widget = curr_widget_item.widget()
            self.plot_layout.removeWidget(curr_widget)
            curr_widget.deleteLater()
        self.plot_layout.addWidget(new_widget)

    def update_tab(self, data):
        pass


