def moving_average_forecast(
    demand_values: list[float],
    window: int
) -> float:

    if not demand_values:
        raise ValueError("Demand history cannot be empty")

    if window <= 0:
        raise ValueError("Window must be greater than zero")

    if len(demand_values) < window:
        raise ValueError(
            "Not enough demand history for the selected window"
        )

    recent_values = demand_values[-window:]

    return sum(recent_values) / window