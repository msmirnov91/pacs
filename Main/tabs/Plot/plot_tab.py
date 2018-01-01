from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Visualizer.Widgets.Plot.cluster_plot import ClusterPlot


class PlotTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Plot/plot.ui"
        super(PlotTab, self).__init__(ui_file, parent)
        self.name = "Проекция"

        self.cluster_plot = ClusterPlot()
        self.plot_layout.addWidget(self.cluster_plot)

    def update_tab(self, data):
        x = "x0"
        y = "x1"
        self.change_visualization_widget_to(self.visualizer.get_cluster_plot(data, x, y))

