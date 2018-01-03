import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform, pdist

from Common.metrics import euclidean_distance


class Data(object):
    LABELS_COLUMN_NAME = 'cls'
    DISTANCES_COLUMN_NAME = 'dist'
    _data = None

    def __init__(self, name, comment='', alg_name='', alg_params=''):
        self.set_data(None)
        self.data_name = name
        self.user_comment = comment
        self.clustering_alg_name = alg_name
        self.clustering_alg_params = alg_params

    def set_data(self, new_data):
        self._data = new_data

    def get_dataframe(self):
        return self._data

    def _drop_labels(self):
        if self.LABELS_COLUMN_NAME in self._data.columns:
            self._data.drop(self.LABELS_COLUMN_NAME)

        if self.is_clusterized():
            self._data.reset_index()

    def clusters_amount(self):
        if not self.is_clusterized():
            return 0

        unique_labels = self.get_labels_list()
        # lack_of_the_time
        negative_labels_amount = 0
        for label in unique_labels:
            if label < 0:
                negative_labels_amount += 1
        return len(self.get_labels_list()) - negative_labels_amount

    def cluster(self, label):
        cluster = self._data.loc[label]

        if isinstance(cluster, pd.Series):
            cluster = pd.DataFrame([cluster])
        return cluster

    def remove_cluster(self, label):
        self._data = self._data.loc[~self._data.index.isin([label])]

    def is_clusterized(self):
        return self._data.index.name == self.LABELS_COLUMN_NAME

    def get_labels_list(self):
        return self.get_data_labels().unique()

    def get_coords_list(self):
        return list(self._data)

    def get_data_labels(self):
        return self._data.index

    def set_labels(self, labels):
        self._drop_labels()
        self._data[self.LABELS_COLUMN_NAME] = labels
        self._data = self._data.set_index(self.LABELS_COLUMN_NAME)

    @property
    def amount_of_elements(self):
        return self._data.shape[0]

    @property
    def dimension(self):
        return self._data.shape[1]

    def amount_of_elements_in_cluster(self, label):
        return self.cluster(label).shape[0]

    def get_cluster_radius(self, label):
        cluster = self.cluster(label)

        center = self.get_cluster_center(label)
        distances = []
        for index, row in cluster.iterrows():
            distances.append(euclidean_distance(center, row))

        return max(distances)  # we assume that the radius is max distance (what is wrong)

    def get_cluster_center(self, label):
        cluster = self.cluster(label)

        max_vals = []
        min_vals = []
        for column in cluster.columns:
            max_vals.append(cluster[column].max())
            min_vals.append(cluster[column].min())

        center = []
        for maximum, minimum in zip(max_vals, min_vals):
            center.append((maximum + minimum) / 2)

        return pd.Series(center, index=cluster.columns.values)

    def get_elements_in_range(self, label, dist_range):
        elements = self._add_distances_column(label)
        elements_in_range = elements[elements[self.DISTANCES_COLUMN_NAME].isin(dist_range)]
        del elements_in_range[self.DISTANCES_COLUMN_NAME]
        return elements_in_range

    def get_label_of_element(self, element):
        if not self.is_clusterized():
            return None

        for index, data_element in self._data.iterrows():
            if data_element.equals(element):
                return index

        return None

    def _add_distances_column(self, label=None, normalized=True):
        # this method makes the dataframe from elements
        # with addition column which is distances from
        # the center of given cluster
        if label is None or not self.is_clusterized():
            cluster = self.get_dataframe()
        else:
            cluster = self.cluster(label)

        result = pd.DataFrame(cluster)
        distances = []
        radius = self.get_cluster_radius(label)
        center = self.get_cluster_center(label)
        for _, element in cluster.iterrows():
            if normalized:
                distance = euclidean_distance(center, element) / radius
            else:
                distance = euclidean_distance(center, element)

            distances.append(distance)

        result[self.DISTANCES_COLUMN_NAME] = distances
        return result

    def get_cluster_centers(self):
        centers = np.ndarray((self.clusters_amount(), self.dimension))
        for label in self.get_labels_list():
            np.append(centers, self.get_cluster_center(label).as_matrix())
        return centers

    def get_cluster_column(self, label, coord):
        cluster = self.cluster(label)
        return cluster[coord]

    def get_sigma(self, label, coord):
        return self.get_cluster_column(label, coord).std() ** 2

    def get_mean(self, label, coord):
        return self.get_cluster_column(label, coord).mean()

    def get_peak_sigma(self, label, peak_type):
        sigmas = []
        for i in range(0, len(self._data.columns)):
            sigmas.append(self.get_sigma(label, self._data.columns[i]))
        return peak_type(sigmas)

    def get_distance_matrix(self):
        return squareform(pdist(self._data))

    def save_to_file(self, file_path):
        self._data.to_csv(file_path)

    def load_from_file(self, path, has_headers=False):
        if path is None or path == "":
            return

        if has_headers:

            self._data = pd.read_csv(path)

            headers = list(self._data)
            bad_header = "Unnamed: 0"

            if self.LABELS_COLUMN_NAME in headers:
                self._data = self._data.set_index(self.LABELS_COLUMN_NAME)
            if bad_header in headers:
                self._data = self._data.loc[:, ~self._data.columns.str.contains('^Unnamed')]
        else:
            self._data = pd.read_csv(path, header=None)
            column_names = []
            for i in range(0, len(self._data.columns)):
                column_names.append("x{}".format(i))
            self._data.columns = column_names




