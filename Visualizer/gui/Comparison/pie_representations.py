from PyQt4 import QtGui
from Visualizer.gui.matplotlib_widget import MatplotlibWidget
import sys


class PieDiagramm(MatplotlibWidget):
    def __init__(self, cluster, splitting, parent=None):
        self.cluster = cluster
        self.splitting = splitting

        self.sizes = None
        self.labels = None
        self.explode = None

        super(PieDiagramm, self).__init__(parent)

    def __calculate_sizes(self):
        # FIXME: cant add int to tuples
        self.sizes = []
        self.labels = ()  # tuple
        self.explode = ()

        for clust in self.splitting.clusters:
            self.labels += (clust.label, )
            self.explode += (0, )
            size = 0
            # for each element of splitting clusters
            for element in clust.elements:
                # if element matches any element in self.cluster.elements
                for target in self.cluster.elements:
                    if element.coordinates == target.coordinates:
                        size += 1
            self.sizes.append(size/self.cluster.capacity)
            pass  # for debug

        # look for elements which does not match any elements of self.splitting.clusters
        matched_elements_part = 0
        for size in self.sizes:
            matched_elements_part += size

        if matched_elements_part < 1:
            self.labels += ('unmatched', )
            self.sizes.append(1 - matched_elements_part)
            self.explode += (0,)

    def plot(self):
        self.__calculate_sizes()

        self.ax.pie(self.sizes, explode=self.explode, labels=self.labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = PieDiagramm()
    main.show()

    sys.exit(app.exec_())
