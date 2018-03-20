from PyQt4.QtCore import pyqtSignal

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

    def get_algorithm_and_settings(self):
        alg_name = self.cb_alg_name.currentText()
        return alg_name, self.settings_widget.get_settings()

    def emit_clusterize_signal(self):
        self.clusterize_data.emit()
