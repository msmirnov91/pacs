from PyQt4.QtCore import pyqtSignal

from Main.tabs.abstract_tab import AbstractTab
from Visualizer.visualizer import Visualizer


class AbstractVisualizationTab(AbstractTab):
    data_update_required = pyqtSignal()

    def __init__(self, ui_file, parent=None):
        super(AbstractVisualizationTab, self).__init__(ui_file, parent)
        self.need_two_data_sets = False
        self.index_val_pattern = "{:4.2f}"

        self.is_visualization_tab = True
        self.visualizer = Visualizer()

    def change_visualization_widget_to(self, new_widget):
        self._change_widget_on_layout_to(self.plot_layout, new_widget)

    def update_tab(self, data):
        pass

    def emit_update_required_signal(self):
        self.data_update_required.emit()
