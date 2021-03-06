import matplotlib.cm as cm
import numpy as np

from Processor.processor import Processor
# TODO: put them all in one module!
from Visualizer.Widgets.Plot.cluster_plot import ClusterPlot
from Visualizer.Widgets.Representation.box_with_whisers_rep import BoxWithWhiskers
from Visualizer.Widgets.Representation.bar_rep import Bar
from Visualizer.Widgets.Representation.matrix_rep import MatrixRep
from Visualizer.Widgets.Representation.vector_rep import VectorRep
from Visualizer.Widgets.Comparison.pie_representations import PieDiagramm


# TODO: make decorators!
class Visualizer(object):
    @classmethod
    def add_standard_title(cls, widget, data, additional_info=None):
        title = "data: '{}', coordinates: {}, elements: {}".format(data.data_name,
                                                                   data.get_coords_list(),
                                                                   data.get_elements_names_string())
        if additional_info:
            title += " "
            title += additional_info
        widget.set_title(title)

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
        Visualizer.add_standard_title(bww, data)
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
        Visualizer.add_standard_title(dense_distribution, data)
        dense_distribution.make_bars(np.asarray(bar_rep))
        return dense_distribution

    @classmethod
    def get_color_matrix(cls, data):
        matrix = MatrixRep()

        if not data.is_clusterized():
            return matrix

        data.order_by_labels()

        x_labels = y_labels = data.get_data_labels().tolist()

        Visualizer.add_standard_title(matrix, data)
        matrix.plot_matrix(data.get_distance_matrix(), x_labels, y_labels)
        return matrix

    @classmethod
    def get_validity_vector(cls, data):
        vector = VectorRep()

        if not data.is_clusterized():
            return vector

        matrix = []
        for label in data.get_labels_list():
            matrix.append(Processor().get_db_for_cluster(data, label))

        x_labels = data.get_labels_list().tolist()
        y_labels = []

        Visualizer.add_standard_title(vector, data)
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
                # lack_of_the_time
                cluster = data.cluster(label)
                if x != y:
                    cluster_y = cluster[y]
                else:
                    cluster_y = np.zeros(cluster[x].shape)

                plot.plot_one_cluster(cluster[x], cluster_y, color, label)
        else:
            # lack_of_the_time
            if x != y:
                data_y = data.get_dataframe()[y]
            else:
                data_y = np.zeros(data.get_dataframe()[x].shape)
            plot.plot_one_cluster(data.get_dataframe()[x], data_y, 'black', 'data')

        additional_info = "X: {}, Y: {}".format(x, y)
        Visualizer.add_standard_title(plot, data, additional_info)
        return plot

    @classmethod
    def get_pie(cls, data1, data2, cluster_label):
        if not data2.is_clusterized() or not data1.is_clusterized():
            return PieDiagramm()

        cluster = data1.cluster(cluster_label)

        amounts = []
        unmatched = 0

        # lack_of_the_time
        for i in data2.get_labels_list():
            amounts.append(0)

        for _, element in cluster.iterrows():
            label = data2.get_label_of_element(element)

            if label is None:
                unmatched += 1
            else:
                amounts[label] += 1

        pie = PieDiagramm()
        title = "Data1: {}, Data2: {}, cluster: {}".format(data1.data_name,
                                                           data2.data_name,
                                                           cluster_label)
        pie.set_title(title)
        pie.plot_pie(amounts, unmatched)
        return pie

