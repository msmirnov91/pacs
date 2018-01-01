from sklearn.cluster import KMeans

from Processor.Clustering.abstract_clustering_algorithm import AbstractClusteringAlgorithm


class AlgKMEANS(AbstractClusteringAlgorithm):
    def __init__(self):
        super(AlgKMEANS, self).__init__()
        self.name = "k-means"

    def _get_labels(self, data_as_matrix, settings):
        """
        examples:
            http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html#sphx-glr-auto-examples-cluster-plot-kmeans-digits-py
            http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
        """
        clusters_amount = settings['num_clusters']

        k_means = KMeans(n_clusters=clusters_amount, random_state=0).fit(data_as_matrix)

        return k_means.labels_

