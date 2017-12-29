"""
def euclidean_distance(first_element, second_element):
    dimension = len(first_element.coordinates)

    if dimension != len(second_element.coordinates):
        return None

    square_sums = 0
    for i in range(0, dimension):
        square_sums += (second_element.coordinates[i] - first_element.coordinates[i])**2
    result = pow(square_sums, 1/2)
    return float(result)
"""


def euclidean_distance(first_element, second_element):
    dimension = first_element.shape[0]

    if dimension != second_element.shape[0]:
        return None

    square_sums = 0
    for i in range(0, dimension):
        square_sums += (second_element.values[i] - first_element.values[i])**2
    result = pow(square_sums, 1/2)
    return float(result)
