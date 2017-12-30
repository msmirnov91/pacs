from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget


class MatrixRep(MatplotlibWidget):
    def __init__(self, parent=None):
        super(MatrixRep, self).__init__(parent)

    def plot_matrix(self, matrix, labels):
        """
        Examples:
            https://matplotlib.org/examples/pylab_examples/matshow.html
            https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels
            https://stackoverflow.com/questions/21712047/matplotlib-imshow-matshow-display-values-on-plot
            https://stackoverflow.com/questions/34781096/matplotlib-matshow-with-many-string-labels

        """

        matrix_plot = self.ax.matshow(matrix)
        self.figure.colorbar(matrix_plot)

