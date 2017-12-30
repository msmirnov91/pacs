from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget, plt
import numpy as np


class Bar(MatplotlibWidget):
    def __init__(self, parent=None):
        super(Bar, self).__init__(parent)

    def make_bars(self, data):
        quart_amount = 4
        # distance from cluster center that limits the quartile
        quartile_length = 0

        cluster_amount = data.clusters_amount()

        ind = np.arange(cluster_amount)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        bottoms = None
        for i in range(0, quart_amount):
            heights = []
            for j in range(0, cluster_amount):
                heights.append(2)

            plt.bar(left=ind, height=heights, width=width, bottom=bottoms)
            bottoms = self.make_new_bottoms(bottoms, heights)

    def plot(self):
        quart_amount = 4
        # distance from cluster center that limits the quartile
        quartile_length = 0

        cluster_amount = self.splitting.clusters_amount()

        ind = np.arange(cluster_amount)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        bottoms = None
        for i in range(0, quart_amount):
            heights = []
            for j in range(0, cluster_amount):
                current_cluster = self.splitting.clusters[j]
                quartile_length = current_cluster.get_next_quartile_radius(quartile_length)
                heights.append(quartile_length)

            self.ax.bar(left=ind, height=heights, width=width, bottom=bottoms)
            bottoms = self.make_new_bottoms(bottoms, heights)

    def make_new_bottoms(self, old_bottoms, heights):
        new_bottoms = []
        if old_bottoms is None:
            new_bottoms = heights
        else:
            for i in range(0, len(heights)):
                new_bottoms.append(old_bottoms[i] + heights[i])
        return new_bottoms
