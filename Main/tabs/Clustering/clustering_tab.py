from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
# TODO: put them all in one module
from Main.tabs.Clustering.Settings.kmeans.kmeans_settings import KmeansSettings
from Main.tabs.Clustering.Settings.dbscan.dbscan_settings import DbscanSettings

from Processor.processor import Processor
from Recorder.recorder import Recorder


# maybe it is not good idea to make this tab an
# instance of AbstractVisualizationTab
class ClusteringTab(AbstractVisualizationTab):
    def __init__(self, data, parent=None):
        self.data = data
        ui_file = "Clustering/clustering_gui.ui"
        super(ClusteringTab, self).__init__(ui_file, data=data, parent=parent)

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
        self.pb_submit.clicked.connect(self.perform_algorithm)

    def update_tab(self):
        # lack_of_the_time
        if self.data.data_name is '':  # it means we have no data selected
            self.pb_submit.setEnabled(False)
        else:
            self.pb_submit.setEnabled(True)

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

    def perform_algorithm(self):
        if self.data is None:
            return

        alg = self.cb_alg_name.currentText()
        params = self.settings_widget.get_settings()
        labels = Processor().get_cluster_labels(self.data, alg, params)
        self.data.set_labels(labels)
        self.data.clustering_alg_name = alg
        self.data.clustering_alg_params = str(params)

        record_msg = """Clustered data:
                \tdata: {}
                \tcoordinates: {}
                \telements: {}
                \talgorithm: {}
                \tparameters: {}\n"""

        recorder = Recorder.get_instance()
        recorder.add_record(record_msg.format(self.data.data_name,
                                              self.data.get_coords_list(),
                                              self.data.get_elements_names_string(),
                                              self.data.clustering_alg_name,
                                              self.data.clustering_alg_params))
