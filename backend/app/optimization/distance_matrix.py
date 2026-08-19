from app.optimization.distance_calculator import (
    calculate_distance
)


def build_distance_matrix(locations):
    """
    Building a distance matrix for a list of locations.

    Each location must contain:
    latitude
    longitude
    """

    number_of_locations = len(locations)

    matrix = []

    for i in range(number_of_locations):

        row = []

        for j in range(number_of_locations):

            distance = calculate_distance(
                locations[i].latitude,
                locations[i].longitude,
                locations[j].latitude,
                locations[j].longitude
            )

            row.append(distance)

        matrix.append(row)

    return matrix