from PyQt4.QtGui import QStandardItemModel, QStandardItem, QAbstractItemView

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Main.tabs.adviser_tab_mixin import AdviserTabMixin
from Main import PACS_DIR
from Main.Plot.coords_plot_widget import CoordsPlot


class PreprocessingTab(AbstractVisualizationTab, AdviserTabMixin):
    def __init__(self, data, parent=None):
        ui_file = PACS_DIR + "/Main/tabs/Preprocessing/preprocessing.ui"
        super(PreprocessingTab, self).__init__(ui_file, data=data, parent=parent)
        self.name = "Предварительая обработка"

        self.plot = CoordsPlot()
        self.scatter_plot_layout.addWidget(self.plot)

        # lack_of_the_time
        self.element_numbers = []
        self.lv_coordinates.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.cb_use_all.toggled.connect(self._enable_choose_data)

    def update_tab(self):
        data_has_names = self.data.has_names()
        self.le_element_numbers.setEnabled(data_has_names)  # disable if data hsd no names
        if data_has_names:
            self.element_numbers = self.data.get_element_names()

        model = QStandardItemModel(self.lv_coordinates)
        for coord in self.data.get_coords_list():
            item = QStandardItem(str(coord))
            model.appendRow(item)
        self.lv_coordinates.setModel(model)

        self.plot.update_tab(self.data)

    def _enable_choose_data(self):
        if self.cb_use_all.isChecked():
            self.gb_choose_data.setEnabled(False)
        else:
            self.gb_choose_data.setEnabled(True)

    def use_all_data(self):
        return self.cb_use_all.isChecked()

    def get_choosed_coords(self):
        coords_list = []
        for index in self.lv_coordinates.selectedIndexes():
            coords_list.append(str(index.data()))
        return coords_list

    def get_choosed_names(self):
        return self.le_element_numbers.text()

    def reduce_data(self):
        pass

    def get_description_for_report(self):
        return self.plot.get_description_for_report()

    # lack_of_the_time
    def add_image_to_report(self, rep_dir, number):
        return self.plot.add_image_to_report(rep_dir, number)

    # lack_of_the_time
    def get_plot_name(self):
        return self.plot.get_plot_name()

