from Visualizer.Widgets.Representation.abstract_matrix_rep import AbstractMatrixRep


class ColorMatrix(AbstractMatrixRep):
    def __init__(self, parent=None):
        super(ColorMatrix, self).__init__(parent)

    def make_matrix_and_labels(self, data):
        """
        Examples:
            https://matplotlib.org/examples/pylab_examples/matshow.html
            https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels
            https://stackoverflow.com/questions/21712047/matplotlib-imshow-matshow-display-values-on-plot
            https://stackoverflow.com/questions/34781096/matplotlib-matshow-with-many-string-labels

        """
        self.matrix = data.get_distance_matrix()

