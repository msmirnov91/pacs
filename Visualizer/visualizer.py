import matplotlib.cm as cm
import numpy as np

# TODO: put them all in one file!
from Visualizer.Widgets.Plot.cluster_plot import ClusterPlot
from Visualizer.Widgets.Representation.box_with_whisers_rep import BoxWithWhiskers
from Visualizer.Widgets.Representation.bar_rep import Bar
from Visualizer.Widgets.Representation.color_distance_matrix_rep import ColorMatrix
from Visualizer.Widgets.Representation.validity_vector_rep import ValidityVectorRep


class Visualizer(object):
    def get_bww(self, data):
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

    def get_dense_distribution(self, data):
        pass

    def get_color_matrix(self, data):
        pass

    def get_validity_vector(self, data):
        pass

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
            plot.plot_one_cluster(data.get_data()[x], data.get_data()[y], 'black', 'data')

        return plot

