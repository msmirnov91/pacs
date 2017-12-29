class Data(object):
    LABELS_COLUMN_NAME = 'cls'
    _data = None

    def __init__(self, data, name, comment='', alg_name='', alg_params=''):
        self.set_data(data)
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
        return self._data.loc[label]

    def is_clusterized(self):
        return self._data.index.name == self.LABELS_COLUMN_NAME

    def get_labels_list(self):
        return self.get_data_labels().unique()

    def get_data_labels(self):
        return self._data.index
