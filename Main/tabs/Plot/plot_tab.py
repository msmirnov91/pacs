from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Visualizer.Widgets.Plot.cluster_plot import ClusterPlot


class PlotTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Plot/plot.ui"
        super(PlotTab, self).__init__(ui_file, parent)
        self.name = "Проекция"

        self.cluster_plot = ClusterPlot()
        self.plot_layout.addWidget(self.cluster_plot)

    def _update_tab(self):
        coordinates = self._data.get_coords_list()

        self.x1.clear()
        self.x2.clear()
        for coordinate in coordinates:
            self.x1.addItem(coordinate)
            self.x2.addItem(coordinate)

        self.x1.setCurrentIndex(0)
        if len(coordinates) == 1:
            self.x2.setCurrentIndex(0)
        else:
            self.x2.setCurrentIndex(1)

        self.x1.currentIndexChanged.connect(self.show_selected_projection)
        self.x2.currentIndexChanged.connect(self.show_selected_projection)
        self.show_selected_projection()

    def show_selected_projection(self):
        x = self.x1.currentText()
        y = self.x2.currentText()

        # lack_of_the_time
        if x == '' or y == '':
            return

        self.change_visualization_widget_to(self.visualizer.get_cluster_plot(self._data, x, y))

    def get_description_for_report(self):
        description = "scatter plot of {} dataset on axis {}, {}".format(self._data.data_name,
                                                                         self.x1.currentText(),
                                                                         self.x2.currentText())
        return description

