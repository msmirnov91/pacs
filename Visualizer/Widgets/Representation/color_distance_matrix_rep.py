import sys

from PyQt4.QtGui import QApplication

from DataStructures.splitting import Splitting
from GUI.Representation.abstract_matrix_rep import AbstractMatrixRep
from Auxiliary.metrics import euclidean_distance


class ColorMatrix(AbstractMatrixRep):
    def __init__(self, splitting, parent=None):
        self.splitting = splitting
        super(ColorMatrix, self).__init__(splitting, parent)

    def make_matrix_and_labels(self):
        """
        Examples:
            https://matplotlib.org/examples/pylab_examples/matshow.html
            https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels
            https://stackoverflow.com/questions/21712047/matplotlib-imshow-matshow-display-values-on-plot
            https://stackoverflow.com/questions/34781096/matplotlib-matshow-with-many-string-labels

        """

        labels = self.splitting.elements.index.unique()

        for label in labels:
            """
            # TODO: make this as splitting.get_cluster(label)
            cluster = self.splitting.cluster(label)


            for _, element in cluster.iterrows():
                row = []
                self.labels.append(str(label))
                for __, another_element in self.splitting.elements.iterrows():
                    row.append(euclidean_distance(element, another_element))
                self.matrix.append(row)

            for _, element in cluster.iterrows():
                self.labels.append(str(label))
            """

            self.matrix, self.labels = self.splitting.get_distance_matrix_rep()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_splitting = Splitting()
    test_splitting.string_generate('r4(4,4)(1,1)ro e4(1,1)(1,1)g+')
    rep = ColorMatrix(test_splitting)
    rep.show()
    sys.exit(app.exec_())
