import sys
from PyQt4.QtGui import *

from GUI.Comparison.pie_representations import PieDiagramm
from Visualizer.gui.abstract_visualizer_widget import AbstractVisualizer
from Algorithms.validation.validation_algorithms_factory import calculate_validity_indexes
from Algorithms.validation.validation_algorithms_factory import calculate_splitting_comparison


class ComparisonVisualizer(AbstractVisualizer):
    def __init__(self, splitting1=None, splitting2=None, parent=None):
        ui_file = "Comparison/comparison_gui.ui"
        self.splitting1 = splitting1
        self.splitting2 = splitting2
        self.pie_rep = None

        super(ComparisonVisualizer, self).__init__(ui_file, parent)

        amount_of_clusters_first = splitting1.clusters_amount()
        amount_of_clusters_second = splitting2.clusters_amount()
        self.amount_of_clusters_first_splitting.setText(str(amount_of_clusters_first))
        self.amount_of_clusters_second_splitting.setText(str(amount_of_clusters_second))

        # self.pie_cluster.setMaximum(len(self.splitting1.clusters))
        # self.pie_cluster.valueChanged.connect(self.choose_cluster_to_pie)

    def compare_clusters(self, cluster, splitting):
        self.pie_cluster.setValue(cluster.label)
        if self.pie_rep is not None:
            self.pie_rep.setParent(None)
        self.pie_rep = PieDiagramm(cluster, splitting)
        self.plot_layout.addWidget(self.pie_rep)

    def update_validity_scores(self):
        scores_1 = calculate_validity_indexes(self.splitting1)
        self.dunn_value_1.setText(self.index_val_pattern.format(scores_1['dunn']))
        self.db_value_1.setText(self.index_val_pattern.format(scores_1['db']))
        self.silhouette_value_1.setText(self.index_val_pattern.format(scores_1['silhouette']))

        scores_2 = calculate_validity_indexes(self.splitting2)
        self.dunn_value_2.setText(self.index_val_pattern.format(scores_2['dunn']))
        self.db_value_2.setText(self.index_val_pattern.format(scores_2['db']))
        self.silhouette_value_2.setText(self.index_val_pattern.format(scores_2['silhouette']))

        comp = calculate_splitting_comparison(self.splitting1, self.splitting2)
        self.le_adj_rand.setText(self.index_val_pattern.format(comp['ari']))
        self.le_adj_mut_info.setText(self.index_val_pattern.format(comp['ami']))

    def choose_cluster_to_pie(self):
        cluster_number = self.pie_cluster.value()
        self.compare_clusters(self.splitting1.clusters[cluster_number - 1], self.splitting2)

    def adjustVisualizer(self):
        self.update_validity_scores()
        # self.compare_clusters(self.splitting1.clusters[0], self.splitting2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = ComparisonVisualizer()
    v.show()
    sys.exit(app.exec_())
