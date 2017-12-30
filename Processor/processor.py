import numpy as np

from Processor.Validity.Davies_Bouldin_Index_KMeans.index import compute_DB_index
from Processor.Validity.Dunn.dunn_sklearn import dunn
from sklearn.metrics import silhouette_score


# TODO: make decorators!
class Processor(object):
    @classmethod
    def get_dunn(cls, data):
        if not data.is_clusterized():
            return 0

        return dunn(data.get_data_labels(), data.get_distance_matrix())

    @classmethod
    def get_db(cls, data):
        if not data.is_clusterized():
            return 0

        n_clusters = data.clusters_amount()
        centers = np.ndarray((n_clusters, data.dimension))
        for label in data.get_labels_list():
            np.append(centers, data.get_cluster_center(label).as_matrix())

        labels = data.get_data_labels()
        print(labels)
        return compute_DB_index(data, labels, centers, n_clusters)

    @classmethod
    def get_silhouette(cls, data):
        if not data.is_clusterized():
            return 0

        return silhouette_score(data.get_dataframe().as_matrix(),
                                data.get_data_labels())
