

from Main.gui.tabs.abstract_tab_widget import AbstractTab
from Visualizer.gui.Plot.cluster_plot import ClusterPlot


class PlotTab(AbstractTab):
    def __init__(self, parent=None):
        ui_file = "Plot/plot.ui"
        super(PlotTab, self).__init__(ui_file, parent)
        self.name = "Проекция"

        self.cluster_plot = ClusterPlot()
        self.plot_layout.addWidget(self.cluster_plot)

    def plot_one_cluster(self, x, y, color, label):
        self.cluster_plot.plot_one_cluster(x, y, color, label)

    def redraw(self):
        self.cluster_plot.redraw()

