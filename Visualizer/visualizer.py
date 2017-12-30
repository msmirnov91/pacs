import matplotlib.cm as cm
import numpy as np

from Visualizer.Widgets.Plot.cluster_plot import ClusterPlot


class Visualizer(object):
    def visualize_comparison(self, data):
        pass

    def visualize_representation(self, data):
        pass

    @classmethod
    def get_cluster_plot(cls, data, x, y):
        plot = ClusterPlot()

        labels = data.get_labels_list()
        colors = cm.rainbow(np.linspace(0, 1, len(labels) + 1))
        for label, color in zip(labels, colors):
            cluster = data.cluster(label)

            plot.plot_one_cluster(cluster[x], cluster[y], color, label)

        return plot

