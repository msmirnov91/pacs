from Visualizer.Widgets.matplotlib_widget import MatplotlibWidget, plt
import numpy as np


class Bar(MatplotlibWidget):
    saved_images = 0

    def __init__(self, parent=None):
        super(Bar, self).__init__(parent)
        self.image_name = "bar"

    def make_bars(self, bar_representation):
        """
        Examples:
            https://matplotlib.org/devdocs/gallery/misc/table_demo.html#sphx-glr-gallery-misc-table-demo-py
        """

        colors = plt.cm.BuPu(np.linspace(0, 0.5, 4))  # 4 means amount of rows

        if bar_representation is None:
            heights = []
            for j in range(0, 2):
                heights.append(2)
            plt.bar(np.arange(2), heights, 0.35)
            return

        rows_amount = bar_representation.shape[0]
        cluster_amount = bar_representation.shape[1]
        ind = np.arange(cluster_amount)  # the x locations for the groups
        y_offset = np.zeros(cluster_amount)
        width = 0.35  # the width of the bars: can also be len(x) sequence

        for i in range(0, rows_amount):
            plt.bar(ind, bar_representation[i], width, bottom=y_offset, color=colors[i])
            y_offset = y_offset + bar_representation[i]

    def _get_saved_images_amount(self):
        Bar.saved_images += 1
        return self.saved_images
