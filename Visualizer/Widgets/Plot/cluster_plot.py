from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget, plt


class ClusterPlot(MatplotlibWidget):
    def __init__(self, parent=None):
        super(ClusterPlot, self).__init__(parent)
        self.set_image_name("scatter_plot")

    def plot_one_cluster(self, x, y, color, label):
        plt.scatter(x, y, c=color, label=label)
