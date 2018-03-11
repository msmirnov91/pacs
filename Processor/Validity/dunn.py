from numpy import linalg as la


def calculate_dunn(data):
    """
    eexample: https://simple.wikipedia.org/wiki/Dunn_index
    :param data:
    :return:
    """
    if not data.is_clusterized():
        return -1

    if data.clusters_amount() == 1:
        return 0

    # calculate maximum diameter
    diameters = []
    cluster_labels = data.get_labels_list()
    for label in cluster_labels:
        diameters.append(data.get_cluster_radius(label) * 2)

    max_diam = max(diameters)

    # calculate all distances between clusters in data
    # we assume that the distance between clusters is the distance
    # between clusters centers
    distances = []
    for label_1 in cluster_labels:
        for label_2 in cluster_labels:
            center_1 = data.get_cluster_center(label_1).as_matrix()
            center_2 = data.get_cluster_center(label_2).as_matrix()
            distance = la.norm(center_1-center_2)
            distances.append(distance)

    distances = list(filter((0.0).__ne__, distances))

    return min(distances) / max_diam



