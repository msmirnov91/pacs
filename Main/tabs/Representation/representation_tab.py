import sys

from PyQt4.QtGui import *

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab

# from Algorithms.clustering.clustering_algorithm_factory import ClusteringAlgorithmFactory
# from Algorithms.validation.validation_algorithms_factory import calculate_validity_indexes
# from DataStructures.splitting import Splitting
# from GUI.Representation.bar_rep import Bar
# from GUI.Representation.box_with_whisers_rep import BoxWithWhiskers
# from GUI.Representation.color_distance_matrix_rep import ColorMatrix
# from GUI.Representation.validity_vector_rep import ValidityVectorRep
# from GUI.abstract_visualizer import AbstractVisualizer


class RepresentationTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Representation/representation_gui.ui"
        super(RepresentationTab, self).__init__(ui_file, parent)
        self.name = "Представление"

        self.bww.toggled.connect(self.emit_update_required_signal)
        self.dens_distribution.toggled.connect(self.emit_update_required_signal)
        self.color_matrix.toggled.connect(self.emit_update_required_signal)
        self.validity_vector.toggled.connect(self.emit_update_required_signal)

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
