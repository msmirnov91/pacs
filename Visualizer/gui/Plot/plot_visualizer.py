from Visualizer.gui.abstract_visualizer_widget import AbstractVisualizer
from Visualizer.gui.Plot.cluster_plot import ClusterPlot


class PlotVisualizer(AbstractVisualizer):
    def __init__(self, parent=None):
        self.cluster_plot = ClusterPlot()
        self.plot_layout.addWidget(self.cluster_plot)

        ui_file = "Visualizer/gui/Plot/plot.ui"
        super(PlotVisualizer, self).__init__(ui_file, parent)

    def plot_one_cluster(self, x, y, color, label):
        self.cluster_plot.plot_one_cluster(x, y, color, label)

    def show(self):
        self.cluster_plot.redraw()

