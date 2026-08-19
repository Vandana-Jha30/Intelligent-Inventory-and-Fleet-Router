import pytest

from app.optimization.distance_calculator import (
    calculate_distance
)


def test_same_location_distance_is_zero():
    distance = calculate_distance(
        12.9716,
        77.5946,
        12.9716,
        77.5946
    )

    assert distance == pytest.approx(0.0)


def test_known_distance():
    # Bengaluru to Chennai
    distance = calculate_distance(
        12.9716,
        77.5946,
        13.0827,
        80.2707
    )

    # Approximate straight-line distance is about 290 km
    assert distance == pytest.approx(
        290,
        abs=5
    )


def test_distance_is_symmetric():
    distance_ab = calculate_distance(
        12.9716,
        77.5946,
        13.0827,
        80.2707
    )

    distance_ba = calculate_distance(
        13.0827,
        80.2707,
        12.9716,
        77.5946
    )

    assert distance_ab == pytest.approx(
        distance_ba
    )


def test_distance_is_positive_for_different_locations():
    distance = calculate_distance(
        12.9716,
        77.5946,
        28.6139,
        77.2090
    )

    assert distance > 0


def test_short_distance():
    distance = calculate_distance(
        12.9716,
        77.5946,
        12.9726,
        77.5956
    )

    assert distance > 0
    assert distance < 1