import matplotlib.cm as cm
import numpy as np

from Main.gui.tabs.Empty.empty_widget import EmptyWidget
from Main.gui.tabs.Plot.plot_tab import PlotTab


class Visualizer(object):
    def visualize_comparison(self, data):
        pass

    def visualize_representation(self, data):
        pass

    def make_scatter_plot(self, data, coord1, coord2):
        visualizer = PlotTab()

        x = coord1
        y = coord2

        labels = data.get_labels_list()
        colors = cm.rainbow(np.linspace(0, 1, len(labels) + 1))
        for label, color in zip(labels, colors):
            cluster = data.cluster(label)

            visualizer.plot_one_cluster(cluster[x], cluster[y], color, label)

        visualizer.show()

        return PlotTab()

    @classmethod
    def get_empty(cls):
        return EmptyWidget()
