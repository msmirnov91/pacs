import copy

import pandas as pd
import numpy as np
from numpy import linalg as la
from scipy.spatial.distance import squareform, pdist

from Common.metrics import euclidean_distance


class Data(object):
    LABELS_COLUMN_NAME = 'cls'
    DISTANCES_COLUMN_NAME = 'dist'
    NAMES_COLUMN_NAME = 'name'

    def __init__(self, name, comment='', alg_name='', alg_params=''):
        self._data = pd.DataFrame()
        self.data_name = name
        self.user_comment = comment
        self.clustering_alg_name = alg_name
        self.clustering_alg_params = alg_params

    def __str__(self):
        return "===DATA OBJECT===\n" + str(self._data) + "\n=================\n" + str(id(self))

    def copy(self, data):
        self._data = copy.deepcopy(data.get_data())
        self.data_name = data.data_name
        self.user_comment = data.user_comment
        self.clustering_alg_name = data.clustering_alg_name
        self.clustering_alg_params = data.clustering_alg_params

    def set_data(self, new_data):
        self._data = new_data

    def get_data(self):
        return self._data

    def get_dataframe(self):
        # this method is used by
        # clustering and validation algorithms
        # so it does not need name column
        if self.has_names():
            new_df = self._data.drop(self.NAMES_COLUMN_NAME, axis=1)
            return new_df
        else:
            return self._data

    def set_dataframe(self, new_dataframe):
        # this method is needed for
        # making data modifications
        if not isinstance(new_dataframe, pd.DataFrame):
            new_dataframe = pd.DataFrame(new_dataframe)
        names = self.get_element_names()
        coordinates = self.get_coords_list()
        self._data = new_dataframe
        self._data.columns = coordinates
        self._data[self.NAMES_COLUMN_NAME] = names

    def _drop_labels(self):
        # TODO: check this code. may contain mistakes
        if self.LABELS_COLUMN_NAME in self._data.columns:
            self._data.drop(self.LABELS_COLUMN_NAME)

        if self.is_clusterized():
            self._data.reset_index()

    def order_by_labels(self):
        self._data.sort_index(inplace=True)

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

    def cluster(self, label, with_names=False):
        if with_names:
            cluster = self._data.loc[label]
        else:
            cluster = self.get_dataframe().loc[label]

        if isinstance(cluster, pd.Series):
            cluster = pd.DataFrame([cluster])
        return cluster

    def remove_cluster(self, label):
        self._data = self._data.loc[~self._data.index.isin([label])]

    def join(self, label_1, label_2):
        if label_1 == label_2 or not self.is_clusterized():
            return

        index_as_list = self.get_data_labels().tolist()
        new_index = list(map(lambda x: label_1 if x == label_2 else x, index_as_list))
        self.set_labels(new_index)

    def select_coordinates(self, coordinates):
        if self.has_names():
            coordinates.append(self.NAMES_COLUMN_NAME)
        self._data = self._data[coordinates]

    def select_elements(self, elements_list):
        if not self.has_names():
            return
        self._data = self._data.loc[self._data[self.NAMES_COLUMN_NAME].isin(elements_list)]

    def is_clusterized(self):
        return self._data.index.name == self.LABELS_COLUMN_NAME

    def is_empty(self):
        return self._data.shape[0] == 0

    def has_names(self):
        return self.NAMES_COLUMN_NAME in self._data.columns

    def get_labels_list(self):
        return self.get_data_labels().unique()

    def get_coords_list(self):
        return list(self.get_dataframe())

    def get_elements_names_string(self):
        if not self.has_names():
            return "No element numbers set for this data"

        element_names = sorted(list(self.get_element_names()))
        result = ""

        def get_last_range_index(array, first_element_index):
            i = first_element_index
            length = len(array)

            while i < length - 1:
                if array[i+1] - array[i] == 1:
                    # next element is next in range
                    i += 1
                else:
                    break

            return i

        i = 0
        while i < len(element_names) - 1:
            if element_names[i+1] - element_names[i] == 1:
                # we have range here
                last_index = get_last_range_index(element_names, i)
                range_str = "{}-{}, ".format(element_names[i], element_names[last_index])
                i = last_index
                result += range_str
            else:
                # we have single element
                i += 1
                result += "{}, ".format(element_names[i])

        # lack_of_the_time
        if result.endswith(", "):
            result = result[:-2]

        return result

    def get_data_labels(self):
        return self._data.index

    def get_element_names(self, cluster=None):
        if cluster is None:
            return self._data[self.NAMES_COLUMN_NAME]
        else:
            return self.cluster(cluster, with_names=True)[self.NAMES_COLUMN_NAME]

    def set_labels(self, labels):
        self._drop_labels()
        self._data[self.LABELS_COLUMN_NAME] = labels
        self._data = self._data.set_index(self.LABELS_COLUMN_NAME)

    @property
    def amount_of_elements(self):
        return self._data.shape[0]

    @property
    def dimension(self):
        # except names column
        return self._data.shape[1] - 1

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

        # TODO: use Pandas to calculate center
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
        elements_in_range = elements.loc[(elements[self.DISTANCES_COLUMN_NAME] > dist_range[0]) &
                                         (elements[self.DISTANCES_COLUMN_NAME] <= dist_range[1])]

        del elements_in_range[self.DISTANCES_COLUMN_NAME]
        return elements_in_range

    def get_label_of_element(self, element):
        if not self.is_clusterized():
            return None

        for index, data_element in self._data.iterrows():
            if np.allclose(data_element.values, element.values):
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

    def get_distance(self, label_1, label_2):
        center_1 = self.get_cluster_center(label_1).as_matrix()
        center_2 = self.get_cluster_center(label_2).as_matrix()
        return la.norm(center_1 - center_2)

    def get_cluster_column(self, label, coord):
        cluster = self.cluster(label)
        return cluster[coord]

    def get_sigma(self, label, coord):
        return self.get_cluster_column(label, coord).std() ** 2

    def get_mean(self, label, coord):
        return self.get_cluster_column(label, coord).mean()

    def get_peak_sigma(self, label, peak_type):
        sigmas = []
        coords = self.get_coords_list()
        for i in range(0, len(coords)):
            sigmas.append(self.get_sigma(label, coords[i]))
        return peak_type(sigmas)

    def get_distance_matrix(self):
        return squareform(pdist(self.get_dataframe()))

    def save_to_file(self, file_path):
        self._data.to_csv(file_path)

    def load_from_file(self, path, has_headers=False):
        if path is None or path == "":
            return

        if has_headers:
            # NOW IT IS ACTUALLY LOADING STORED DATA

            self._data = pd.read_csv(path)

            headers = list(self._data)
            bad_header = "Unnamed: 0"

            if self.LABELS_COLUMN_NAME in headers:
                self._data = self._data.set_index(self.LABELS_COLUMN_NAME)
            if bad_header in headers:
                self._data = self._data.loc[:, ~self._data.columns.str.contains('^Unnamed')]

        else:
            # NOW IT IS ACTUALLY LOADING RAW DATA
            self._data = pd.read_csv(path, header=None)
            column_names = []
            for i in range(0, len(self._data.columns)):
                column_names.append("x{}".format(i))
            self._data.columns = column_names

            self._data[self.NAMES_COLUMN_NAME] = self._data.index.values


