import pytest

from app.optimization.demand_forecaster import (
    moving_average_forecast
)


def test_moving_average_forecast():
    demand = [95, 105, 98, 110, 102]

    result = moving_average_forecast(
        demand,
        window=3
    )

    assert result == pytest.approx(103.3333333333)


def test_moving_average_with_window_one():
    demand = [100, 120, 140]

    result = moving_average_forecast(
        demand,
        window=1
    )

    assert result == 140


def test_empty_demand_history():
    with pytest.raises(
        ValueError,
        match="Demand history cannot be empty"
    ):
        moving_average_forecast([], 3)


def test_invalid_window():
    with pytest.raises(
        ValueError,
        match="Window must be greater than zero"
    ):
        moving_average_forecast([100, 110], 0)


def test_insufficient_history():
    with pytest.raises(
        ValueError,
        match="Not enough demand history"
    ):
        moving_average_forecast([100, 110], 3)