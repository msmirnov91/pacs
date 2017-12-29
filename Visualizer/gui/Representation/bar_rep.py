from PyQt4.QtGui import QApplication
from GUI.Representation.rep_widget import RepWidget
import sys
import numpy as np


class Bar(RepWidget):
    def __init__(self, splitting, parent=None):
        super(Bar, self).__init__(splitting, parent)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rep = Bar()
    rep.show()
    sys.exit(app.exec_())
