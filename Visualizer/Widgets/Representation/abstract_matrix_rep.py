from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget, plt


class AbstractMatrixRep(MatplotlibWidget):
    def __init__(self, parent=None):
        self.matrix = None
        self.labels = ['']
        super(AbstractMatrixRep, self).__init__(parent)

    def plot_matrix(self, data):
        self.make_matrix_and_labels(data)

        matrix_plot = self.ax.matshow(self.matrix)
        self.figure.colorbar(matrix_plot)

    def make_matrix_and_labels(self, data):
        raise NotImplementedError
