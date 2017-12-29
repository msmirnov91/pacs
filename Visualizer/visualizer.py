import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from Visualizer.gui.Plot.plot_visualizer import PlotVisualizer
from Visualizer.gui.Empty.empty_widget import EmptyWidget


class Visualizer(object):
    def visualize_comparison(self, data):
        pass

    def visualize_representation(self, data):
        pass

    def visualize_data_on_axis(self, data, coord1, coord2):
        visualizer = PlotVisualizer()

        x = coord1
        y = coord2

        labels = data.get_labels_list()
        colors = cm.rainbow(np.linspace(0, 1, len(labels) + 1))
        for label, color in zip(labels, colors):
            cluster = data.cluster(label)

            visualizer.plot_one_cluster(cluster[x], cluster[y], color, label)

        visualizer.show()

    @classmethod
    def get_empty(cls):
        return EmptyWidget()
