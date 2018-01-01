class AbstractClusteringAlgorithm(object):
    def __init__(self):
        # allows to find needed algorithm
        self.name = None
        # need for testing
        self.fake_settings = {}

    def get_labels(self, data, settings):
        data_matrix = data.get_dataframe().as_matrix()
        labels = self._get_labels(data_matrix, settings)
        return labels

    def _get_labels(self, data_as_matrix, settings):
        """
        this method must return set of cluster labels
        """
        return []


