import pandas as pd

from Common.metrics import euclidean_distance


class Data(object):
    LABELS_COLUMN_NAME = 'cls'
    _data = None

    def __init__(self, name, comment='', alg_name='', alg_params=''):
        self.set_data(None)
        self.data_name = name
        self.user_comment = comment
        self.clustering_alg_name = alg_name
        self.clustering_alg_params = alg_params

    def set_data(self, new_data):
        self._data = new_data

    def get_data(self):
        return self._data

    def clusterize(self, algorithm):
        pass

    def _drop_labels(self):
        if self.LABELS_COLUMN_NAME in self._data.columns:
            self._data.drop(self.LABELS_COLUMN_NAME)

        if self.is_clusterized():
            self._data.reset_index()

    def clusters_amount(self):
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

    def is_clusterized(self):
        return self._data.index.name == self.LABELS_COLUMN_NAME

    def get_labels_list(self):
        return self.get_data_labels().unique()

    def get_data_labels(self):
        return self._data.index

    @property
    def amount_of_elements(self):
        return self._data.shape[0]

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

    def save_to_file(self, file_path):
        self._data.to_csv(file_path)

    def load_from_file(self, path, has_headers=False):
        if path is None or path == "":
            return

        if has_headers:
            self._data = pd.read_csv(path)
            if self.LABELS_COLUMN_NAME in list(self._data):
                self._data = self._data.set_index(self.LABELS_COLUMN_NAME)
        else:
            self._data = pd.read_csv(path, header=None)
            column_names = []
            for i in range(0, len(self._data.columns)):
                column_names.append("x{}".format(i))
            self._data.columns = column_names



