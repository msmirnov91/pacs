import sys

from PyQt4.QtGui import *

from Main.tabs.abstract_tab_widget import AbstractTab

# from Algorithms.clustering.clustering_algorithm_factory import ClusteringAlgorithmFactory
# from Algorithms.validation.validation_algorithms_factory import calculate_validity_indexes
# from DataStructures.splitting import Splitting
# from GUI.Representation.bar_rep import Bar
# from GUI.Representation.box_with_whisers_rep import BoxWithWhiskers
# from GUI.Representation.color_distance_matrix_rep import ColorMatrix
# from GUI.Representation.validity_vector_rep import ValidityVectorRep
# from GUI.abstract_visualizer import AbstractVisualizer


class RepresentationTab(AbstractTab):
    def __init__(self, parent=None):
        ui_file = "Representation/representation_gui.ui"
        super(RepresentationTab, self).__init__(ui_file, parent)
        self.name = "Представление"

        self.bww.toggled.connect(self.emit_update_required_signal)
        self.dens_distribution.toggled.connect(self.emit_update_required_signal)
        self.color_matrix.toggled.connect(self.emit_update_required_signal)
        self.validity_vector.toggled.connect(self.emit_update_required_signal)

        """
        self.splitting = splitting
        if splitting.is_empty():
            self.splitting.string_generate('r200(4,4)(6,55)ro r300(4,4)(7,77)ro e100(1,2)(7,88)g+')

        self.current_rep = None
        self.reps = [BoxWithWhiskers(splitting=self.splitting),
                     BoxWithWhiskers(splitting=self.splitting),
                     # Bar(splitting=self.splitting),
                     ColorMatrix(splitting=self.splitting),
                     ValidityVectorRep(splitting=self.splitting)]

        self.clustering_algorithm_factory = ClusteringAlgorithmFactory()

        for algorithm in self.clustering_algorithm_factory.algorithms:
            self.algorithm.addItem(algorithm.name)

        self.current_settings_widget = None
        self.update_settings_widget()

        self.update_cluster_elements_info()

        self.bww.toggled.connect(self.bww_toggled)
        self.dens_distribution.toggled.connect(self.dens_distrib_toggled)
        self.color_matrix.toggled.connect(self.color_matrix_toggled)
        self.validity_vector.toggled.connect(self.validity_vector_toggled)

        self.algorithm.currentIndexChanged.connect(self.update_settings_widget)
        self.submit.clicked.connect(self.reclusterize)
        self.save_button.clicked.connect(self.save_splitting)

        self.cluster_number.valueChanged.connect(self.update_cluster_elements_list)

    def update_settings_widget(self):
        if self.current_settings_widget is not None:
            self.current_settings_widget.setParent(None)

        algorithm_number = self.algorithm.currentIndex()
        self.current_settings_widget = self.clustering_algorithm_factory.settings[algorithm_number]
        self.algorithm_settings_layout.addWidget(self.current_settings_widget)

    def update_validity_scores(self):
        scores = calculate_validity_indexes(self.splitting)
        self.dunn_value.setText(self.index_val_pattern.format(scores['dunn']))
        self.db_value.setText(self.index_val_pattern.format(scores['db']))
        self.silhouette_value.setText(self.index_val_pattern.format(scores['silhouette']))

    def update_cluster_elements_info(self):
        self.cluster_amount_display.setText(str(self.splitting.clusters_amount()))
        self.cluster_number.setMaximum(self.splitting.clusters_amount())
        # self.update_cluster_elements_list(self.cluster_number.value())

    def update_cluster_elements_list(self, cluster_num):
        cluster = self.splitting.clusters[cluster_num - 1]

        elements_list_model = QStandardItemModel(self.elements_list)
        for i in range(0, cluster.capacity):
            element_sign = cluster.elements[i].identification_sign
            elements_list_item = QStandardItem(str(element_sign))

            elements_list_model.appendRow(elements_list_item)

        self.elements_list.setModel(elements_list_model)

    def reclusterize(self):
        algorithm_number = self.algorithm.currentIndex()
        algorithm = self.clustering_algorithm_factory.algorithms[algorithm_number]

        settings = self.current_settings_widget.get_settings()

        self.splitting.unclusterize()
        self.splitting.clusterize_raw_elements(algorithm, settings)
        self.current_rep.update_splitting(self.splitting)
        self.update_validity_scores()
        self.update_cluster_elements_info()

    def bww_toggled(self):
        if self.bww.isChecked():
            self.current_rep.setParent(None)
            self.current_rep = self.reps[0]
            self.plot_layout.addWidget(self.current_rep)

    def dens_distrib_toggled(self):
        if self.dens_distribution.isChecked():
            self.current_rep.setParent(None)
            self.current_rep = self.reps[1]
            self.plot_layout.addWidget(self.current_rep)

    def color_matrix_toggled(self):
        if self.color_matrix.isChecked():
            self.current_rep.setParent(None)
            self.current_rep = self.reps[2]
            self.plot_layout.addWidget(self.current_rep)

    def validity_vector_toggled(self):
        if self.validity_vector.isChecked():
            self.current_rep.setParent(None)
            self.current_rep = self.reps[3]
            self.plot_layout.addWidget(self.current_rep)

    def save_splitting(self):
        dialog = QFileDialog()
        file_name = dialog.getSaveFileName(self, 'Save clustering',
                                           self.splitting.store_dir_name, "Clustering (*.clust)")
        self.splitting.save(file_name)

    def adjustVisualizer(self):
        self.update_validity_scores()
        self.current_rep = self.reps[0]
        self.plot_layout.addWidget(self.current_rep)

    def update_representations_splitting(self, splitting):
        self.splitting = splitting
        for rep in self.reps:
            rep.update_splitting(splitting)
"""
    def update_tab(self, data):
        if self.bww.isChecked():
            new_widget = self.visualizer.get_bww(data)
        elif self.dens_distribution.isChecked():
            new_widget = self.visualizer.get_dense_distribution(data)
        elif self.color_matrix.isChecked():
            new_widget = self.visualizer.get_color_matrix(data)
        elif self.validity_vector.isChecked():
            new_widget = self.visualizer.get_validity_vector(data)
        else:
            return
        self.change_visualization_widget_to(new_widget)

        dunn = self.processor.get_dunn(data)
        db = self.processor.get_db(data)
        silhouette = self.processor.get_silhouette(data)

        self.dunn_value.setText(self.index_val_pattern.format(dunn))
        self.db_value.setText(self.index_val_pattern.format(db))
        self.silhouette_value.setText(self.index_val_pattern.format(silhouette))

        self.cluster_amount_display.setText(str(data.clusters_amount()))
        self.cluster_number
        self.elements_list

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = RepresentationTab()
    v.show()
    sys.exit(app.exec_())
