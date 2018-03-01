from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QStandardItemModel, QStandardItem, QAbstractItemView
from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
# TODO: put them all in one module
from Main.tabs.Clustering.Settings.kmeans.kmeans_settings import KmeansSettings
from Main.tabs.Clustering.Settings.dbscan.dbscan_settings import DbscanSettings


# maybe it is not good idea to make this tab an
# instance of AbstractVisualizationTab
class ClusteringTab(AbstractVisualizationTab):
    clusterize_data = pyqtSignal()

    def __init__(self, parent=None):
        ui_file = "Clustering/clustering_gui.ui"
        super(ClusteringTab, self).__init__(ui_file, parent)

        self.name = "Кластеризация"

        for name in self.processor.get_clustering_algorithm_names():
            self.cb_alg_name.addItem(name)

        self.lv_coordinates.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # TODO: add validator to le_element_numbers

        self.settings_widget_classes = [
            KmeansSettings,
            DbscanSettings
        ]

        # lack_of_the_time
        self.settings_widget = None

        self.set_appropriate_settings_widget()
        self.cb_alg_name.currentIndexChanged.connect(self.set_appropriate_settings_widget)
        self.pb_submit.clicked.connect(self.emit_clusterize_signal)
        self.cb_use_all.toggled.connect(self._enable_choose_data)

        # lack_of_the_time
        self.element_numbers = []

    def update_tab(self, data):
        # need this method to set the list of coordinates
        # and possible numbers of elements
        data_has_names = data.has_names()
        self.le_element_numbers.setEnabled(data_has_names)  # disable if data hsd no names
        if data_has_names:
            self.element_numbers = data.get_element_names()

        model = QStandardItemModel(self.lv_coordinates)
        for coord in data.get_coords_list():
            item = QStandardItem(str(coord))
            model.appendRow(item)
        self.lv_coordinates.setModel(model)

    def set_appropriate_settings_widget(self):
        alg_name = self.cb_alg_name.currentText()

        settings_widget = None
        for settings_widget_class in self.settings_widget_classes:
            if settings_widget_class.settings_for_algorithm == alg_name:
                settings_widget = settings_widget_class()
                break
        if settings_widget is not None:
            self.settings_widget = settings_widget
            self._change_widget_on_layout_to(self.alg_params_layout, settings_widget)

    def _enable_choose_data(self):
        if self.cb_use_all.isChecked():
            self.gb_choose_data.setEnabled(False)
        else:
            self.gb_choose_data.setEnabled(True)

    def get_algorithm_and_settings(self):
        alg_name = self.cb_alg_name.currentText()
        return alg_name, self.settings_widget.get_settings()

    def use_all_data(self):
        return self.cb_use_all.isChecked()

    def get_choosed_coords(self):
        coords_list = []
        for index in self.lv_coordinates.selectedIndexes():
            coords_list.append(str(index.data()))
        return coords_list

    def get_choosed_names(self):
        return self.le_element_numbers.text()

    def emit_clusterize_signal(self):
        self.clusterize_data.emit()
