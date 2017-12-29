import matplotlib.pyplot as plt

from Visualizer.gui.matplotlib_widget import MatplotlibWidget


class ClusterPlot(MatplotlibWidget):
    def __init__(self, parent=None):
        self.x = None
        self.y = None
        super(ClusterPlot, self).__init__(parent)

    def plot_one_cluster(self, x, y, color, label):
        plt.scatter(x, y, c=color, label=label)
