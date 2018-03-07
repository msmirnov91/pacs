from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget, plt


class ClusterPlot(MatplotlibWidget):
    saved_images = 0

    def __init__(self, parent=None):
        super(ClusterPlot, self).__init__(parent)
        self.image_name = "scatter_plot"

    def plot_one_cluster(self, x, y, color, label):
        plt.scatter(x, y, c=color, label=label)

    def _get_saved_images_amount(self):
        ClusterPlot.saved_images += 1
        return self.saved_images
