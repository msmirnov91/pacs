from numpy import linalg as la


def calculate_davies_bouldin(data):
    """
    example: https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index
    :param data:
    :return:
    """
    if not data.is_clusterized():
        return -1

    if data.clusters_amount() == 1:
        return 1

    db_for_clusters = []
    for label in data.get_labels_list():
        db_for_clusters.append(calc_davies_bouldin_for_cluster(data, label))

    return sum(db_for_clusters)/data.clusters_amount()


def calc_davies_bouldin_for_cluster(data, cluster_label):
    # calculating r_ij_values
    r_ij_values = []

    if data.clusters_amount() == 1:
        return 1

    for label in data.get_labels_list():
        if label == cluster_label:
            continue
        r_ij_values.append(r_ij(data, cluster_label, label))

    return max(r_ij_values)


def r_ij(data, ci, cj):
    """
    A measure of similarity of clusters ci and cj
    defined as sum of clusters sparsity divided by
    clusters dissimilarity
    """
    return (s(data, ci) + s(data, cj))/d(data.cluster(ci), data.cluster(cj))


def s(data, cluster_label):
    """
    s identifies sparsity of cluster
    the more average distance between cluster elements is,
    the more is cluster sparsity
    """

    cluster = data.cluster(cluster_label)
    center = data.get_cluster_center(cluster_label).as_matrix()

    # calculate all distances in cluster
    distances = []
    for index, row in cluster.iterrows():
        element = row.as_matrix()
        distances.append(la.norm(center - element))

    return sum(distances) / data.amount_of_elements_in_cluster(cluster_label)


def d(ci, cj):
    """
    function identifies "dissimilarity" of two clusters
    as minimum distance between elements of those clusters
    """
    distances = []

    for index, row in ci.iterrows():
        for another_index, another_row in cj.iterrows():
            dist = la.norm(row.as_matrix() - another_row.as_matrix())
            if dist != 0:
                distances.append(dist)

    return min(distances)
