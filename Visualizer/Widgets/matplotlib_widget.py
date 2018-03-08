import sys
import os

import matplotlib.pyplot as plt
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(QWidget):
    saved_images = 0

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.ax = None

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = self.figure.add_subplot(1, 1, 1)

        self.image_name = None
        # self.saved_images = 0

        # self.redraw()

    def redraw(self):
        # discards the old graph
        if self.ax is not None:
            self.ax.clear()

        # create an axis
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.plot()

        # refresh canvas
        self.canvas.draw()

    def deleteLater(self):
        plt.close(self.figure)
        super().deleteLater()

    def save_image(self, report_dir, fig_name):
        self.figure.savefig(os.path.join(report_dir, fig_name))

    def set_title(self, title):
        self.figure.suptitle(title)

    def get_image_name(self):
        return "{}{}.png".format(self.image_name, self._get_saved_images_amount())

    def _get_saved_images_amount(self):
        type(self).saved_images += 1
        return self.saved_images


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MatplotlibWidget()
    main.show()

    sys.exit(app.exec_())
