from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab


class ComparisonTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Comparison/comparison_gui.ui"
        super(ComparisonTab, self).__init__(ui_file, parent)
        self.need_two_data_sets = True
        self.name = "Сравнение"

        self._data_2 = None

    def update_tab(self, data1, data2):
        if data1 is None or data2 is None:
            return
        self._data = data1
        self._data_2 = data2

        clusters_amount = self._data.clusters_amount()

        self.pie_cluster.setRange(0, clusters_amount-1)

        self.pie_cluster.valueChanged.connect(self._update_tab)

        self._update_tab()

    def _update_tab(self):
        # maybe it will be better to pass needed cluster as Data object
        cluster = self.pie_cluster.value()
        self.change_visualization_widget_to(self.visualizer.get_pie(self._data.cluster(cluster),
                                                                    self._data_2))

        ami = self.processor.get_ami(self._data, self._data_2)
        ari = self.processor.get_ari(self._data, self._data_2)
        self.le_adj_mut_info.setText(self.index_val_pattern.format(ami))
        self.le_adj_rand.setText(self.index_val_pattern.format(ari))

        self.amount_of_clusters_first_splitting.setText(str(self._data.clusters_amount()))
        self.amount_of_clusters_second_splitting.setText(str(self._data_2.clusters_amount()))

        dunn_1 = self.processor.get_dunn(self._data)
        dunn_2 = self.processor.get_dunn(self._data_2)
        self.dunn_value_1.setText(self.index_val_pattern.format(dunn_1))
        self.dunn_value_2.setText(self.index_val_pattern.format(dunn_2))

        db_1 = self.processor.get_db(self._data)
        db_2 = self.processor.get_db(self._data_2)
        self.db_value_1.setText(self.index_val_pattern.format(db_1))
        self.db_value_2.setText(self.index_val_pattern.format(db_2))

        silhouette_1 = self.processor.get_silhouette(self._data)
        silhouette_2 = self.processor.get_silhouette(self._data_2)
        self.silhouette_value_1.setText(self.index_val_pattern.format(silhouette_1))
        self.silhouette_value_2.setText(self.index_val_pattern.format(silhouette_2))
