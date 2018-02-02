from matplotlib import ticker
from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget


class MatrixRep(MatplotlibWidget):
    # need this for make cluster labels on the plot readable
    # one label corresponds to element [-1; -1]
    MAX_X_LABELS = 21
    MAX_Y_LABELS = 11

    def __init__(self, parent=None):
        super(MatrixRep, self).__init__(parent)

    def plot_matrix(self, matrix, x_labels, y_labels):
        """
        Examples:
            https://matplotlib.org/examples/pylab_examples/matshow.html
            https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels
            https://stackoverflow.com/questions/21712047/matplotlib-imshow-matshow-display-values-on-plot
            https://stackoverflow.com/questions/34781096/matplotlib-matshow-with-many-string-labels

        """

        matrix_plot = self.ax.matshow(matrix)

        x_labels_amount = len(x_labels)
        y_labels_amount = len(y_labels)

        x_base = 1 if x_labels_amount < self.MAX_X_LABELS else int(x_labels_amount / self.MAX_X_LABELS)
        y_base = 1 if y_labels_amount < self.MAX_Y_LABELS else int(y_labels_amount / self.MAX_Y_LABELS)

        x_labels = x_labels[0::x_base]
        y_labels = y_labels[0::y_base]

        self.ax.set_xticklabels([''] + x_labels)
        self.ax.set_yticklabels([''] + y_labels)

        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(x_base))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(y_base))

        self.figure.colorbar(matrix_plot)

