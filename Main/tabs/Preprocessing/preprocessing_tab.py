from PyQt4.QtGui import QStandardItemModel, QStandardItem, QAbstractItemView

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Main.tabs.adviser_tab_mixin import AdviserTabMixin
from Main import PACS_DIR
from Main.Plot.plot_tab import PlotTab


class PreprocessingTabMixin(AbstractVisualizationTab, AdviserTabMixin):
    def __init__(self, parent=None):
        ui_file = PACS_DIR + "/Main/tabs/Preprocessing/preprocessing.ui"
        super(PreprocessingTabMixin, self).__init__(ui_file, parent)
        self.name = "Предварительая обработка"

        self.plot = PlotTab()
        self.scatter_plot_layout.addWidget(self.plot)

        # lack_of_the_time
        self.element_numbers = []
        self.lv_coordinates.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.cb_use_all.toggled.connect(self._enable_choose_data)

    def update_tab(self, data):
        data_has_names = data.has_names()
        self.le_element_numbers.setEnabled(data_has_names)  # disable if data hsd no names
        if data_has_names:
            self.element_numbers = data.get_element_names()

        model = QStandardItemModel(self.lv_coordinates)
        for coord in data.get_coords_list():
            item = QStandardItem(str(coord))
            model.appendRow(item)
        self.lv_coordinates.setModel(model)

        if data is None:
            self.pb_submit.setEnabled(False)
        else:
            self.pb_submit.setEnabled(True)

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

    def get_description_for_report(self):
        return self.plot.get_description_for_report()

