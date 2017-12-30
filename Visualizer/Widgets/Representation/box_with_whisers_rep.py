import sys

from PyQt4.QtGui import QApplication

from DataStructures.splitting import Splitting
from GUI.Representation.rep_widget import RepWidget


class BoxWithWhiskers(RepWidget):
    def __init__(self, splitting, parent=None):
        super(BoxWithWhiskers, self).__init__(splitting, parent)

    def plot(self):
        """
        Examples:
            http://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
            http://matplotlib.org/examples/pylab_examples/boxplot_demo.html
            https://edunow.su/site/content/python-matplotlib
            http://4answered.com/questions/view/1359643/python-matplotlib-filled-boxplots
            https://pythonspot.com/en/matplotlib/
            https://plot.ly/matplotlib/box-plots/
        """
        data, widths = self.splitting.get_box_with_whiskers_rep()

        """
        widths = []
        for clust in self.splitting.clusters:
            width = clust.capacity/self.splitting.elements_amount()
            widths.append(width)
        """

        bplot = self.ax.boxplot(data, widths=widths,
                                vert=True,   # vertical box aligmnent
                                patch_artist=True)   # fill with color

        """
        # fill with colors
        colors = ['pink', 'lightblue', 'lightgreen']
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
        """

        # adding horizontal grid lines
        self.ax.yaxis.grid(True)
        self.ax.set_xticks([y + 1 for y in range(len(data))], )
        self.ax.set_xlabel('xlabel')
        self.ax.set_ylabel('ylabel')

        # add x-tick labels
        #plt.setp(axes, xticks=[y + 1 for y in range(len(all_data))],
        #         xticklabels=['x1', 'x2', 'x3', 'x4'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rep = BoxWithWhiskers(Splitting())
    rep.show()
    sys.exit(app.exec_())
