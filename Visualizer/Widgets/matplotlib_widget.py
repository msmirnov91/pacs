from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from PyQt4.QtGui import *

import sys


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.ax = None

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = self.figure.add_subplot(1, 1, 1)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MatplotlibWidget()
    main.show()

    sys.exit(app.exec_())
