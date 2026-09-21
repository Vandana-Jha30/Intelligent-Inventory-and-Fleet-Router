from app.optimization.routing_benchmark import (
    generate_benchmark_data,
    benchmark_routing_scenario,
    run_routing_benchmark
)


def test_generate_benchmark_data():

    (
        depot,
        delivery_locations,
        vehicles
    ) = generate_benchmark_data(
        number_of_locations=3,
        number_of_vehicles=2,
        seed=42
    )

    assert depot is not None

    assert len(delivery_locations) == 3
    assert len(vehicles) == 2

    assert all(
        location.demand_quantity > 0
        for location in delivery_locations
    )

    assert all(
        vehicle.capacity > 0
        for vehicle in vehicles
    )


def test_benchmark_routing_scenario():

    (
        depot,
        delivery_locations,
        vehicles
    ) = generate_benchmark_data(
        number_of_locations=3,
        number_of_vehicles=2,
        seed=42
    )

    result = benchmark_routing_scenario(
        depot=depot,
        delivery_locations=delivery_locations,
        vehicles=vehicles,
        time_limit_seconds=1
    )

    assert "heuristic" in result
    assert "ortools" in result
    assert "comparison" in result

    for method in [
        "heuristic",
        "ortools"
    ]:

        assert (
            result[method]["vehicles_used"]
            >= 1
        )

        assert (
            result[method]["total_distance"]
            > 0
        )

        assert (
            result[method]["total_cost"]
            > 0
        )

        assert (
            result[method]["execution_time_ms"]
            >= 0
        )


def test_run_routing_benchmark():

    results = run_routing_benchmark(
        scenarios=[3],
        time_limit_seconds=1
    )

    assert len(results) == 1

    result = results[0]

    assert result["number_of_locations"] == 3
    assert result["number_of_vehicles"] >= 2

    assert "heuristic" in result
    assert "ortools" in result
    assert "comparison" in result