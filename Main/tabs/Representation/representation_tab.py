from PyQt4.QtGui import QStandardItemModel, QStandardItem

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab


class RepresentationTab(AbstractVisualizationTab):
    def __init__(self, data, parent=None):
        ui_file = "Representation/representation_gui.ui"
        super(RepresentationTab, self).__init__(ui_file, data=data, parent=parent)
        self.name = "Оценка результата"

        self.bww.toggled.connect(self.update_tab)
        self.dens_distribution.toggled.connect(self.update_tab)
        self.color_matrix.toggled.connect(self.update_tab)
        self.validity_vector.toggled.connect(self.update_tab)
        self.cluster_number.valueChanged.connect(self.update_tab)

    def update_tab(self):
        if self.sender().parent() == self.visualization_type and not self.sender().isChecked():
            # signal from released radiobutton
            return

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

        dunn = self.processor.get_dunn(self.data)
        db = self.processor.get_db(self.data)
        silhouette = self.processor.get_silhouette(self.data)

        self.dunn_value.setText(self.index_val_pattern.format(dunn))
        self.db_value.setText(self.index_val_pattern.format(db))
        self.silhouette_value.setText(self.index_val_pattern.format(silhouette))

        self.cluster_amount_display.setText(str(self.data.clusters_amount()))
        self.cluster_number.setRange(0, self.data.clusters_amount() - 1)

        model = QStandardItemModel(self.elements_list)
        if self.data.is_clusterized() and self.data.has_names():
            names_df = self.data.get_element_names(cluster=self.cluster_number.value())
            for name in list(names_df):
                item = QStandardItem(str(name))
                model.appendRow(item)
        else:
            model.clear()

        self.elements_list.setModel(model)

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
