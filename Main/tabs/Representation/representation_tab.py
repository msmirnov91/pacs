from PyQt4.QtGui import QStandardItemModel, QStandardItem

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab


class RepresentationTab(AbstractVisualizationTab):
    def __init__(self, data, parent=None):
        ui_file = "Representation/representation_gui.ui"
        super(RepresentationTab, self).__init__(ui_file, data=data, parent=parent)
        self.name = "Оценка результата"

        self.bww.toggled.connect(self.change_plot)
        self.dens_distribution.toggled.connect(self.change_plot)
        self.color_matrix.toggled.connect(self.change_plot)
        self.validity_vector.toggled.connect(self.change_plot)
        self.cluster_number.valueChanged.connect(self.update_elements_list)
        self.join_clusters_pb.clicked.connect(self.join_clusters)

    def change_plot(self):
        if self.bww.isChecked():
            new_widget = self.visualizer.get_bww(self.data)
        elif self.dens_distribution.isChecked():
            new_widget = self.visualizer.get_dense_distribution(self.data)
        elif self.color_matrix.isChecked():
            new_widget = self.visualizer.get_color_matrix(self.data)
        elif self.validity_vector.isChecked():
            new_widget = self.visualizer.get_validity_vector(self.data)
        else:
            return
        self.change_visualization_widget_to(new_widget)

    def update_elements_list(self):
        model = QStandardItemModel(self.elements_list)
        if self.data.is_clusterized() and self.data.has_names():
            names_df = self.data.get_element_names(cluster=self.cluster_number.value())
            for name in list(names_df):
                item = QStandardItem(str(name))
                model.appendRow(item)
        else:
            model.clear()

        self.elements_list.setModel(model)

    def update_tab(self):
        if self.sender().parent() == self.visualization_type and not self.sender().isChecked():
            # signal from released radiobutton
            return

        self.change_plot()

        dunn = self.processor.get_dunn(self.data)
        db = self.processor.get_db(self.data)
        silhouette = self.processor.get_silhouette(self.data)

        self.dunn_value.setText(self.index_val_pattern.format(dunn))
        self.db_value.setText(self.index_val_pattern.format(db))
        self.silhouette_value.setText(self.index_val_pattern.format(silhouette))

        self.cluster_amount_display.setText(str(self.data.clusters_amount()))
        self.cluster_number.setRange(0, self.data.clusters_amount() - 1)
        self.first_join_sb.setRange(0, self.data.clusters_amount() - 1)
        self.second_join_sb.setRange(0, self.data.clusters_amount() - 1)

        self.update_elements_list()

    def join_clusters(self):
        self.data.join(self.first_join_sb.value(), self.second_join_sb.value())
        self.update_tab()

    def get_description_for_report(self):
        if self.bww.isChecked():
            widget_name = "box with whiskers"
        elif self.dens_distribution.isChecked():
            widget_name = "density distribution"
        elif self.color_matrix.isChecked():
            widget_name = "distance matrix"
        elif self.validity_vector.isChecked():
            widget_name = "validity vector"
        else:
            return "something very bad happens"

        description = "{} of {} dataset".format(widget_name, self.data.data_name)
        return description
