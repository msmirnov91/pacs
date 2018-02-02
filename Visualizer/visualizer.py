import matplotlib.cm as cm
import numpy as np

from Processor.processor import Processor
# TODO: put them all in one module!
from Visualizer.Widgets.Plot.cluster_plot import ClusterPlot
from Visualizer.Widgets.Representation.box_with_whisers_rep import BoxWithWhiskers
from Visualizer.Widgets.Representation.bar_rep import Bar
from Visualizer.Widgets.Representation.matrix_rep import MatrixRep
from Visualizer.Widgets.Comparison.pie_representations import PieDiagramm


# TODO: make decorators!
class Visualizer(object):
    @classmethod
    def get_bww(cls, data):
        if not data.is_clusterized():
            return BoxWithWhiskers()

        # bww represents two quartiles, max and min element and median
        # in this rep, min and max values must be the radius of sphere
        # contains 90% elements, second quartile must be minimum sigma,
        # third quartile must be maximum sigma, median must be "zero"
        # So, data must look like: -r90 -minsigma -minsigma 0  maxsigma maxsigma r90
        total_elements = data.amount_of_elements
        representation = []
        widths = []
        for label in data.get_labels_list():
            curr_cluster_elements = data.amount_of_elements_in_cluster(label)
            widths.append(curr_cluster_elements / total_elements)

            cluster_rep = [
                -1 * data.get_cluster_radius(label),
                -1 * data.get_peak_sigma(label, min),
                -1 * data.get_peak_sigma(label, min),
                0,
                data.get_peak_sigma(label, max),
                data.get_peak_sigma(label, max),
                data.get_cluster_radius(label),
            ]
            representation.append(cluster_rep)

        bww = BoxWithWhiskers()
        bww.plot_bww(representation, widths)
        return bww

    @classmethod
    def get_dense_distribution(cls, data):
        if not data.is_clusterized() or data.amount_of_elements == 1:
            return Bar()

        dist_ranges = [[0, 0.25],
                       [0.25, 0.5],
                       [0.5, 0.75],
                       [0.75, 1]]

        bar_rep = []
        for dist_range in dist_ranges:
            row = []
            for label in data.get_labels_list():
                elements = data.get_elements_in_range(label, dist_range)
                relative_elements_amount = elements.shape[0] / data.amount_of_elements_in_cluster(label)
                row.append(relative_elements_amount)
            bar_rep.append(row)

        dense_distribution = Bar()
        dense_distribution.make_bars(np.asarray(bar_rep))
        return dense_distribution

    @classmethod
    def get_color_matrix(cls, data):
        matrix = MatrixRep()

        if not data.is_clusterized():
            return matrix

        data.order_by_labels()

        x_labels = y_labels = data.get_data_labels().tolist()

        matrix.plot_matrix(data.get_distance_matrix(), x_labels, y_labels)
        return matrix

    @classmethod
    def get_validity_vector(cls, data):
        if not data.is_clusterized():
            return MatrixRep()
        vector = MatrixRep()

        matrix = []
        for i in range(0, data.clusters_amount()):
            matrix.append(Processor().get_db_for_cluster(data, i))

        x_labels = data.get_labels_list().tolist()
        y_labels = []

        vector.plot_matrix([matrix], x_labels, y_labels)
        return vector

    def visualize_representation(self, data):
        pass

    @classmethod
    def get_cluster_plot(cls, data, x, y):
        plot = ClusterPlot()

        if data.is_clusterized():
            labels = data.get_labels_list()
            colors = cm.rainbow(np.linspace(0, 1, len(labels) + 1))
            for label, color in zip(labels, colors):
                cluster = data.cluster(label)

                plot.plot_one_cluster(cluster[x], cluster[y], color, label)
        else:
            plot.plot_one_cluster(data.get_dataframe()[x], data.get_dataframe()[y], 'black', 'data')

        return plot

    @classmethod
    def get_pie(cls, cluster, data):
        if not data.is_clusterized():
            return PieDiagramm()

        amounts = []
        unmatched = 0

        # lack_of_the_time
        for i in data.get_labels_list():
            amounts.append(0)

        for _, element in cluster.iterrows():
            label = data.get_label_of_element(element)

            if label is None:
                unmatched += 1
            else:
                amounts[label] += 1

        pie = PieDiagramm()
        pie.plot_pie(amounts, unmatched)
        return pie

