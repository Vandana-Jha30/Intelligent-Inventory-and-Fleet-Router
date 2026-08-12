import math
import pytest

from app.optimization.inventory_optimizer import (
    calculate_average_demand,
    calculate_annual_demand,
    calculate_demand_std,
    calculate_eoq,
    calculate_safety_stock,
    calculate_reorder_point,
    calculate_inventory_position,
)


def test_average_demand():
    demand = [95, 105, 98, 110, 102]

    result = calculate_average_demand(demand)

    assert result == 102


def test_annual_demand():
    result = calculate_annual_demand(102)

    assert result == 37230


def test_demand_std():
    demand = [95, 105, 98, 110, 102]

    result = calculate_demand_std(demand)

    expected = 5.873670062235365

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-9
    )


def test_eoq():
    result = calculate_eoq(
        annual_demand=12000,
        ordering_cost=500,
        holding_cost=20
    )

    expected = math.sqrt(600000)

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-9
    )


def test_safety_stock():
    result = calculate_safety_stock(
        z_score=1.645,
        demand_std=10,
        lead_time_days=5
    )

    expected = 1.645 * 10 * math.sqrt(5)

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-9
    )


def test_reorder_point():
    result = calculate_reorder_point(
        average_daily_demand=100,
        lead_time_days=5,
        safety_stock=37
    )

    assert result == 537


def test_inventory_position():
    result = calculate_inventory_position(
        on_hand=500,
        on_order=300,
        reserved=100
    )

    assert result == 700


def test_eoq_rejects_negative_demand():
    with pytest.raises(ValueError):
        calculate_eoq(
            annual_demand=-100,
            ordering_cost=500,
            holding_cost=20
        )


def test_eoq_rejects_zero_holding_cost():
    with pytest.raises(ValueError):
        calculate_eoq(
            annual_demand=12000,
            ordering_cost=500,
            holding_cost=0
        )


def test_average_demand_rejects_empty_history():
    with pytest.raises(ValueError):
        calculate_average_demand([])


def test_safety_stock_rejects_negative_lead_time():
    with pytest.raises(ValueError):
        calculate_safety_stock(
            z_score=1.645,
            demand_std=10,
            lead_time_days=-5
        )


def test_inventory_position_rejects_negative_stock():
    with pytest.raises(ValueError):
        calculate_inventory_position(
            on_hand=-10,
            on_order=100,
            reserved=20
        )