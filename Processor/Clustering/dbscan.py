from sklearn.cluster import DBSCAN
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pandas as pd

from Algorithms.clustering.abstract_clustering_algorithm import AbstractClusteringAlgorithm
from DataStructures.element import Element


class AlgDBSCAN(AbstractClusteringAlgorithm):
    def __init__(self):
        super(AlgDBSCAN, self).__init__()
        self.name = "dbscan"
        self.fake_settings = {'eps': 0.3,
                              'min_samples': 10}

    def generate_fake_data(self):
        centers = [[1, 1], [-1, -1], [1, -1]]
        x, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                                    random_state=0)
        return pd.DataFrame(x, columns=['x0', 'x1'])

    def _perform(self, data, settings):
        """
        examples:
        http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
        """
        eps = settings['eps']  # default 0.3
        min_samples = settings['min_samples']  # default 10

        db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)

        return db.labels_


if __name__ == '__main__':
    alg = AlgDBSCAN()
    result = alg.perform(alg.generate_fake_data(), alg.fake_settings)
    pass
