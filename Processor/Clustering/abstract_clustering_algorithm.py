from DataStructures.cluster import Cluster
from DataStructures.element import Element


class AbstractClusteringAlgorithm:
    def __init__(self):
        # allows to find needed algorithm
        self.name = None
        # need for testing
        self.fake_settings = {}

        self.raw_elements = []
        self.resulting_clusters = None

    def generate_fake_data(self):
        """
        just for testing. must be overrided in each algorithm to match the data in examples
        """
        return 0

    def perform(self, elements, settings):
        # self.resulting_clusters = []
        # self.raw_elements = elements
        # data = self.make_data_from_elements(elements)
        data = elements.as_matrix()
        labels = self._perform(data, settings)
        # self.assign_elements(labels, data)
        # return self.resulting_clusters
        return labels

    def _perform(self, elements, settings):
        """
        this method must return set of cluster labels
        """
        return self.resulting_clusters

    def make_data_from_elements(self, elements):
        """
        makes data for clustering algorithms from instances of Element class
        """
        result = []
        for element in elements:
            result.append(element.coordinates)
        return result

    def assign_elements(self, cluster_labels, data_set):
        """
        this method assigns elements to clusters using labels obtained while clustering
        """
        # get unique elements
        cluster_numbers = list(set(cluster_labels))

        clusters_amount = len(cluster_numbers)
        for i in range(0, clusters_amount):
            self.resulting_clusters.append(Cluster())

        for label, element_coords in zip(cluster_labels, data_set):
            element = Element()
            element.coordinates = element_coords

            # TODO: looks like BAD solution!!
            for old_element in self.raw_elements:
                if old_element.coordinates == element_coords:
                    element.identification_sign = old_element.identification_sign
                    break

            self.resulting_clusters[label].label = label
            self.resulting_clusters[label].append_element(element)

        for cluster in self.resulting_clusters:
            cluster.calculate_parameters()

