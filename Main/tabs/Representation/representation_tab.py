from PyQt4.QtGui import QStandardItemModel, QStandardItem

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab


class RepresentationTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Representation/representation_gui.ui"
        super(RepresentationTab, self).__init__(ui_file, parent)
        self.name = "Представление"

        self.bww.toggled.connect(self._update_tab)
        self.dens_distribution.toggled.connect(self._update_tab)
        self.color_matrix.toggled.connect(self._update_tab)
        self.validity_vector.toggled.connect(self._update_tab)
        self.cluster_number.valueChanged.connect(self._update_tab)

    def _update_tab(self):
        if self.sender().parent() == self.visualization_type and not self.sender().isChecked():
            # signal from released radiobutton
            return

        if self.bww.isChecked():
            new_widget = self.visualizer.get_bww(self._data)
        elif self.dens_distribution.isChecked():
            new_widget = self.visualizer.get_dense_distribution(self._data)
        elif self.color_matrix.isChecked():
            new_widget = self.visualizer.get_color_matrix(self._data)
        elif self.validity_vector.isChecked():
            new_widget = self.visualizer.get_validity_vector(self._data)
        else:
            return
        self.change_visualization_widget_to(new_widget)

        dunn = self.processor.get_dunn(self._data)
        db = self.processor.get_db(self._data)
        silhouette = self.processor.get_silhouette(self._data)

        self.dunn_value.setText(self.index_val_pattern.format(dunn))
        self.db_value.setText(self.index_val_pattern.format(db))
        self.silhouette_value.setText(self.index_val_pattern.format(silhouette))

        self.cluster_amount_display.setText(str(self._data.clusters_amount()))
        self.cluster_number.setRange(0, self._data.clusters_amount()-1)

        model = QStandardItemModel(self.elements_list)
        if self._data.is_clusterized() and self._data.has_names():
            names_df = self._data.get_element_names(cluster=self.cluster_number.value())
            for name in list(names_df):
                item = QStandardItem(str(name))
                model.appendRow(item)
        else:
            model.clear()

        self.elements_list.setModel(model)
