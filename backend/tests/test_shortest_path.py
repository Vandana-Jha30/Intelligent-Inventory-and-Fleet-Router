import pytest

from app.optimization.shortest_path import find_shortest_path


def test_origin_equals_destination():
    graph = {
        "A": {
            "B": 5
        },
        "B": {}
    }

    result = find_shortest_path(
        graph,
        "A",
        "A"
    )

    assert result["distance"] == 0
    assert result["path"] == ["A"]


def test_direct_path():
    graph = {
        "A": {
            "B": 10
        },
        "B": {}
    }

    result = find_shortest_path(
        graph,
        "A",
        "B"
    )

    assert result["distance"] == 10
    assert result["path"] == ["A", "B"]


def test_indirect_path_shorter_than_direct_path():
    graph = {
        "A": {
            "B": 2,
            "D": 10
        },
        "B": {
            "C": 3
        },
        "C": {
            "D": 2
        },
        "D": {}
    }

    result = find_shortest_path(
        graph,
        "A",
        "D"
    )

    assert result["distance"] == 7
    assert result["path"] == [
        "A",
        "B",
        "C",
        "D"
    ]


def test_multiple_routes_choose_shortest_total_distance():
    graph = {
        "A": {
            "B": 4,
            "C": 1
        },
        "B": {
            "D": 5
        },
        "C": {
            "D": 2
        },
        "D": {}
    }

    result = find_shortest_path(
        graph,
        "A",
        "D"
    )

    assert result["distance"] == 3
    assert result["path"] == [
        "A",
        "C",
        "D"
    ]


def test_shortest_path_requires_combining_multiple_edges():
    graph = {
        "A": {
            "B": 2,
            "C": 8
        },
        "B": {
            "C": 2,
            "D": 10
        },
        "C": {
            "D": 2
        },
        "D": {}
    }

    result = find_shortest_path(
        graph,
        "A",
        "D"
    )

    assert result["distance"] == 6
    assert result["path"] == [
        "A",
        "B",
        "C",
        "D"
    ]


def test_origin_not_in_graph():
    graph = {
        "A": {
            "B": 5
        },
        "B": {}
    }

    with pytest.raises(
        ValueError,
        match="Origin node is not present in graph"
    ):
        find_shortest_path(
            graph,
            "X",
            "B"
        )


def test_destination_not_in_graph():
    graph = {
        "A": {
            "B": 5
        },
        "B": {}
    }

    with pytest.raises(
        ValueError,
        match="Destination node is not present in graph"
    ):
        find_shortest_path(
            graph,
            "A",
            "X"
        )


def test_empty_graph():
    with pytest.raises(
        ValueError,
        match="Graph is required"
    ):
        find_shortest_path(
            {},
            "A",
            "B"
        )


def test_unreachable_destination():
    graph = {
        "A": {
            "B": 5
        },
        "B": {},
        "C": {}
    }

    with pytest.raises(
        ValueError,
        match="Destination is unreachable from origin"
    ):
        find_shortest_path(
            graph,
            "A",
            "C"
        )


def test_unknown_neighbor_is_rejected():
    graph = {
        "A": {
            "B": 5
        },
        "B": {
            "C": 2
        }
    }

    with pytest.raises(
        ValueError,
        match="Graph contains an unknown neighboring node"
    ):
        find_shortest_path(
            graph,
            "A",
            "B"
        )


def test_negative_edge_cost_is_rejected():
    graph = {
        "A": {
            "B": -5
        },
        "B": {}
    }

    with pytest.raises(
        ValueError,
        match="Edge costs must be non-negative"
    ):
        find_shortest_path(
            graph,
            "A",
            "B"
        )


def test_directed_graph():
    graph = {
        "A": {
            "B": 5
        },
        "B": {
            "C": 3
        },
        "C": {}
    }

    result = find_shortest_path(
        graph,
        "A",
        "C"
    )

    assert result["distance"] == 8
    assert result["path"] == [
        "A",
        "B",
        "C"
    ]


def test_reverse_direction_is_not_automatically_created():
    graph = {
        "A": {
            "B": 5
        },
        "B": {}
    }

    with pytest.raises(
        ValueError,
        match="Destination is unreachable from origin"
    ):
        find_shortest_path(
            graph,
            "B",
            "A"
        )