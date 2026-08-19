import pytest

from app.optimization.distance_matrix import (
    build_distance_matrix
)


class Location:
    def __init__(
        self,
        latitude,
        longitude
    ):
        self.latitude = latitude
        self.longitude = longitude


def test_empty_locations():
    matrix = build_distance_matrix([])

    assert matrix == []


def test_single_location():
    locations = [
        Location(12.9716, 77.5946)
    ]

    matrix = build_distance_matrix(locations)

    assert len(matrix) == 1
    assert len(matrix[0]) == 1
    assert matrix[0][0] == pytest.approx(0.0)


def test_matrix_dimensions():
    locations = [
        Location(12.9716, 77.5946),
        Location(13.0827, 80.2707),
        Location(28.6139, 77.2090)
    ]

    matrix = build_distance_matrix(locations)

    assert len(matrix) == 3

    for row in matrix:
        assert len(row) == 3


def test_diagonal_values_are_zero():
    locations = [
        Location(12.9716, 77.5946),
        Location(13.0827, 80.2707),
        Location(28.6139, 77.2090)
    ]

    matrix = build_distance_matrix(locations)

    for i in range(len(locations)):
        assert matrix[i][i] == pytest.approx(0.0)


def test_matrix_is_symmetric():
    locations = [
        Location(12.9716, 77.5946),
        Location(13.0827, 80.2707),
        Location(28.6139, 77.2090)
    ]

    matrix = build_distance_matrix(locations)

    for i in range(len(locations)):
        for j in range(len(locations)):
            assert matrix[i][j] == pytest.approx(
                matrix[j][i]
            )


def test_known_distance_in_matrix():
    locations = [
        Location(12.9716, 77.5946),
        Location(13.0827, 80.2707)
    ]

    matrix = build_distance_matrix(locations)

    assert matrix[0][1] == pytest.approx(
        290,
        abs=5
    )