from types import SimpleNamespace

import pytest

from app.optimization.min_cost_flow_solver import solve_min_cost_flow


def node(node_id, supply=0, demand=0):
    return SimpleNamespace(
        node_id=node_id,
        supply=supply,
        demand=demand,
    )


def arc(source, destination, capacity, cost):
    return SimpleNamespace(
        from_node=source,
        to_node=destination,
        capacity=capacity,
        cost=cost,
    )


def test_min_cost_flow_chooses_cheapest_path():
    nodes = [
        node(1, supply=10),
        node(2, demand=10),
        node(3),
    ]

    arcs = [
        arc(1, 2, 10, 10),
        arc(1, 3, 10, 2),
        arc(3, 2, 10, 3),
    ]

    result = solve_min_cost_flow(nodes, arcs)

    assert result["total_supply"] == 10
    assert result["total_demand"] == 10
    assert result["total_flow"] == pytest.approx(10)
    assert result["total_cost"] == pytest.approx(50)

    assert result["flow_plan"] == [
        {
            "from_node": 1,
            "to_node": 3,
            "flow": pytest.approx(10),
            "capacity": 10.0,
            "unit_cost": 2.0,
            "total_cost": pytest.approx(20),
        },
        {
            "from_node": 3,
            "to_node": 2,
            "flow": pytest.approx(10),
            "capacity": 10.0,
            "unit_cost": 3.0,
            "total_cost": pytest.approx(30),
        },
    ]


def test_min_cost_flow_splits_flow_when_capacity_requires_it():
    nodes = [node(1, supply=10), node(2, demand=10)]
    arcs = [
        arc(1, 2, 6, 2),
        arc(1, 2, 4, 5),
    ]

    result = solve_min_cost_flow(nodes, arcs)

    assert result["total_flow"] == pytest.approx(10)
    assert result["total_cost"] == pytest.approx(32)


def test_min_cost_flow_rejects_unbalanced_supply_and_demand():
    nodes = [node(1, supply=10), node(2, demand=9)]
    arcs = [arc(1, 2, 10, 1)]

    with pytest.raises(ValueError, match="Total supply must equal total demand"):
        solve_min_cost_flow(nodes, arcs)


def test_min_cost_flow_rejects_unknown_node():
    nodes = [node(1, supply=10), node(2, demand=10)]
    arcs = [arc(1, 3, 10, 1)]

    with pytest.raises(ValueError, match="Unknown destination node: 3"):
        solve_min_cost_flow(nodes, arcs)


def test_min_cost_flow_rejects_negative_cost():
    nodes = [node(1, supply=10), node(2, demand=10)]
    arcs = [arc(1, 2, 10, -1)]

    with pytest.raises(ValueError, match="Arc cost cannot be negative"):
        solve_min_cost_flow(nodes, arcs)
