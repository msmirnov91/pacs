import numpy as np

from sklearn.metrics import silhouette_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score

from Processor.Validity.Davies_Bouldin_Index_KMeans.index import compute_DB_index
from Processor.Validity.Dunn.dunn_sklearn import dunn


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

    @classmethod
    def get_ari(cls, data1, data2):
        if not data1.is_clusterized() or not data2.is_clusterized():
            return 0

        return adjusted_rand_score(data1.get_data_labels(), data2.get_data_labels())

    @classmethod
    def get_ami(cls, data1, data2):
        if not data1.is_clusterized() or not data2.is_clusterized():
            return 0

        return adjusted_mutual_info_score(data1.get_data_labels(), data2.get_data_labels())
