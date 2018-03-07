from PyQt4 import QtGui
from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget
import sys


class PieDiagramm(MatplotlibWidget):
    saved_images = 0

    def __init__(self, parent=None):
        super(PieDiagramm, self).__init__(parent)
        self.image_name = "pie"

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

    def plot_pie(self, sizes, unmatched):
        """
        Examples:
            https://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html
        """
        labels = []
        for size in sizes:
            index = sizes.index(size)
            labels.append(str(index))

        if unmatched is not None and unmatched != 0:
            sizes.append(unmatched)
            labels.append('unmatched')

        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)

    def _get_saved_images_amount(self):
        PieDiagramm.saved_images += 1
        return self.saved_images


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = PieDiagramm()
    main.show()

    sys.exit(app.exec_())
