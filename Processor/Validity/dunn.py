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
            distances.append(data.get_distance(label_1, label_2))

    distances = list(filter((0.0).__ne__, distances))

    return min(distances) / max_diam



