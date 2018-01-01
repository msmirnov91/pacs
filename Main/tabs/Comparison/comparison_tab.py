import sys

from PyQt4.QtGui import *

from Main.tabs.abstract_tab_widget import AbstractTab


class ComparisonTab(AbstractTab):
    def __init__(self, parent=None):
        ui_file = "Comparison/comparison_gui.ui"
        super(ComparisonTab, self).__init__(ui_file, parent)
        self.pie_rep = None
        self.need_two_data_sets = True
        self.name = "Сравнение"

        # amount_of_clusters_first = splitting1.clusters_amount()
        # amount_of_clusters_second = splitting2.clusters_amount()
        # self.amount_of_clusters_first_splitting.setText(str(amount_of_clusters_first))
        # self.amount_of_clusters_second_splitting.setText(str(amount_of_clusters_second))

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
        pass
        # self.update_validity_scores()
        # self.compare_clusters(self.splitting1.clusters[0], self.splitting2)

    def update_tab(self, data1, data2):
        if data2 is None:
            return

        # maybe it will be better to pass needed cluster as Data object
        self.change_visualization_widget_to(self.visualizer.get_pie(data1.cluster(0), data2))

        ami = self.processor.get_ami(data1, data2)
        ari = self.processor.get_ari(data1, data2)
        self.le_adj_mut_info.setText(self.index_val_pattern.format(ami))
        self.le_adj_rand.setText(self.index_val_pattern.format(ari))

        self.amount_of_clusters_first_splitting.setText(str(data1.clusters_amount()))
        self.amount_of_clusters_second_splitting.setText(str(data2.clusters_amount()))

        dunn_1 = self.processor.get_dunn(data1)
        dunn_2 = self.processor.get_dunn(data2)
        self.dunn_value_1.setText(self.index_val_pattern.format(dunn_1))
        self.dunn_value_2.setText(self.index_val_pattern.format(dunn_2))

        db_1 = self.processor.get_db(data1)
        db_2 = self.processor.get_db(data2)
        self.db_value_1.setText(self.index_val_pattern.format(db_1))
        self.db_value_2.setText(self.index_val_pattern.format(db_2))

        silhouette_1 = self.processor.get_silhouette(data1)
        silhouette_2 = self.processor.get_silhouette(data2)
        self.silhouette_value_1.setText(self.index_val_pattern.format(silhouette_1))
        self.silhouette_value_2.setText(self.index_val_pattern.format(silhouette_2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = ComparisonTab()
    v.show()
    sys.exit(app.exec_())
