from PyQt4.QtCore import pyqtSignal
from Main.tabs.abstract_tab_widget import AbstractTab
# TODO: put them all in one file
from Main.tabs.Clustering.Settings.kmeans.kmeans_settings import KmeansSettings
from Main.tabs.Clustering.Settings.dbscan.dbscan_settings import DbscanSettings


class ClusteringTab(AbstractTab):
    clusterize_data = pyqtSignal()

    def __init__(self, parent=None):
        ui_file = "Clustering/clustering_gui.ui"
        super(ClusteringTab, self).__init__(ui_file, parent)
        self.name = "Кластеризация"

        for name in self.processor.get_clustering_algorithm_names():
            self.cb_alg_name.addItem(name)

        self.settings_widget_classes = [
            KmeansSettings,
            DbscanSettings
        ]

        self.set_appropriate_settings_widget()
        self.cb_alg_name.currentIndexChanged.connect(self.set_appropriate_settings_widget)

    def set_appropriate_settings_widget(self):
        alg_name = self.cb_alg_name.currentText()

        settings_widget = None
        for settings_widget_class in self.settings_widget_classes:
            if settings_widget_class.settings_for_algorithm == alg_name:
                settings_widget = settings_widget_class()
                break
        if settings_widget is not None:
            self._change_widget_on_layout_to(self.alg_params_layout, settings_widget)

    def get_algorithm_and_settings(self):
        alg_name = self.cb_alg_name.currentText()
        return alg_name, self.settings_widget.get_settings()

    def update_tab(self, data):
        pass

    # lack_of_the_time
    def emit_clusterize_signal(self):
        self.clusterize_data.emit()
