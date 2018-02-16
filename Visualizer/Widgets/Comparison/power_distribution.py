import sys
import random

from PyQt4 import QtGui
from GUI.matplotlib_widget import MatplotlibWidget
import numpy as np

from DataStructures import splitting, cluster


class PowerDistribution(MatplotlibWidget):
    def __init__(self, cluster, splitting, parent=None):
        self.cluster = cluster
        self.splitting = splitting

        self.sizes = None
        self.labels = None
        self.explode = None

        super(PowerDistribution, self).__init__(parent)
        self.image_name = "power_distr"

    def __calculate_sizes(self):
        # FIXME: cant add int to tuples
        self.sizes = []
        self.labels = ()  # tuple
        self.explode = ()

        for clust in self.splitting.clusters:
            self.labels += (clust.label, )
            self.explode += (0, )
            size = 0
            # for each element of splitting clusters
            for element in clust.elements:
                # if element matches any element in self.cluster.elements
                for target in self.cluster.elements:
                    if element.coordinates == target.coordinates:
                        size += 1
            self.sizes.append(size/self.cluster.capacity)
            pass  # for debug

        # look for elements which does not match any elements of self.splitting.clusters
        matched_elements_part = 0
        for size in self.sizes:
            matched_elements_part += size

        if matched_elements_part < 1:
            self.labels += ('unmatched', )
            self.sizes.append(1 - matched_elements_part)
            self.explode += (0,)

    def plot(self):
        np.random.seed(0)

        x = []
        n_bins = 10
        for i in range(0, n_bins):
            val = random.uniform(0, 1)
            x.append(val)
        # x = np.array(x)
        x = np.random.randn(1000, 3)
        self.ax.hist(x, n_bins,  histtype='bar', stacked=True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = PowerDistribution(cluster.Cluster(), splitting.Splitting())
    main.show()

    sys.exit(app.exec_())
