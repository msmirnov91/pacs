from GUI.Representation.rep_widget import RepWidget


class AbstractMatrixRep(RepWidget):
    def __init__(self, splitting, parent=None):
        self.matrix = []
        self.labels = ['']
        super(AbstractMatrixRep, self).__init__(splitting, parent)

    def plot(self):
        self.make_matrix_and_labels()

        matrix_plot = self.ax.matshow(self.matrix)

        self.figure.colorbar(matrix_plot)
        self.ax.set_xticklabels(self.labels)
        self.ax.set_yticklabels(self.labels)

    def make_matrix_and_labels(self):
        raise NotImplementedError
