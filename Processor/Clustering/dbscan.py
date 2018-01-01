from sklearn.cluster import DBSCAN

from Processor.Clustering.abstract_clustering_algorithm import AbstractClusteringAlgorithm


class AlgDBSCAN(AbstractClusteringAlgorithm):
    def __init__(self):
        super(AlgDBSCAN, self).__init__()
        self.name = "dbscan"

    def _get_labels(self, data_as_matrix, settings):
        """
        examples:
            http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
        """
        eps = settings['eps']  # default 0.3
        min_samples = settings['min_samples']  # default 10

        db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_as_matrix)

        return db.labels_

