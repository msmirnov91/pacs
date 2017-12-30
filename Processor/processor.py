import numpy as np

from sklearn.metrics import silhouette_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score

from Processor.Validity.Davies_Bouldin_Index_KMeans.index import compute_DB_index, compute_R
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
        centers = data.get_cluster_centers()
        labels = data.get_data_labels()
        return compute_DB_index(data, labels, centers, n_clusters)

    @classmethod
    def get_db_for_cluster(cls, data, cluster_number):
        if not data.is_clusterized():
            return 0
        n_clusters = data.clusters_amount()
        centers = data.get_cluster_centers()
        labels = data.get_data_labels()
        return compute_R(cluster_number, data, labels, centers, n_clusters)

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
