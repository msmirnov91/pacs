from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget, plt


class BoxWithWhiskers(MatplotlibWidget):
    def __init__(self, parent=None):
        super(BoxWithWhiskers, self).__init__(parent)
        self.set_image_name("bww")

    def plot_bww(self, data, widths):
        """
        Examples:
            http://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
            http://matplotlib.org/examples/pylab_examples/boxplot_demo.html
            https://edunow.su/site/content/python-matplotlib
            http://4answered.com/questions/view/1359643/python-matplotlib-filled-boxplots
            https://pythonspot.com/en/matplotlib/
            https://plot.ly/matplotlib/box-plots/
        """
        plt.boxplot(data, widths=widths,
                    vert=True,  # vertical box alignment
                    patch_artist=True)  # fill with color

        # adding horizontal grid lines
        self.ax.yaxis.grid(True)
        self.ax.set_xticks([y + 1 for y in range(len(data))], )

        # add x-tick labels
        # plt.setp(axes, xticks=[y + 1 for y in range(len(all_data))],
        #         xticklabels=['x1', 'x2', 'x3', 'x4'])

