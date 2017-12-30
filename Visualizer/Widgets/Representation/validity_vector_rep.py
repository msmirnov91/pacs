from Visualizer.Widgets.Representation.abstract_matrix_rep import AbstractMatrixRep


class ValidityVectorRep(AbstractMatrixRep):
    def __init__(self, splitting, parent=None):
        super(ValidityVectorRep, self).__init__(splitting, parent)
        self.index_val_pattern = "{:4.2f}"

    def make_matrix_and_labels(self):
        """
        Examples:
            https://matplotlib.org/examples/pylab_examples/matshow.html
            https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels
            https://stackoverflow.com/questions/21712047/matplotlib-imshow-matshow-display-values-on-plot
            https://stackoverflow.com/questions/34781096/matplotlib-matshow-with-many-string-labels

        """
        self.matrix = []
        row = []
        for label in self.splitting.get_unique_labels():
            cluster = self.splitting.cluster(label)
            db_index = 0
            row.append(db_index)
            self.labels.append(str(label))
        self.matrix.append(row)

