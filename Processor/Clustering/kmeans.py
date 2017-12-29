import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from Algorithms.clustering.abstract_clustering_algorithm import AbstractClusteringAlgorithm


class AlgKMEANS(AbstractClusteringAlgorithm):
    def __init__(self):
        super(AlgKMEANS, self).__init__()
        self.name = "k-means"
        self.fake_settings = {'num_clusters': 2}

    def generate_fake_data(self):
        return pd.DataFrame(np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]]), columns=['x0', 'x1'])

    def _perform(self, data, settings):
        """
        examples:
            http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html#sphx-glr-auto-examples-cluster-plot-kmeans-digits-py
            http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
        """
        clusters_amount = settings['num_clusters']

        x = np.array(data)
        k_means = KMeans(n_clusters=clusters_amount, random_state=0).fit(x)

        return k_means.labels_


if __name__ == '__main__':
    alg = AlgKMEANS()
    result = alg.perform(alg.generate_fake_data(), alg.fake_settings)
    pass
