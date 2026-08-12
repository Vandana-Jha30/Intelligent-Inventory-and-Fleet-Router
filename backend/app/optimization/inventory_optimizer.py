import math
import statistics


def calculate_average_demand(demand_history):
    if not demand_history:
        raise ValueError("Demand history cannot be empty")

    return sum(demand_history) / len(demand_history)


def calculate_annual_demand(average_daily_demand):
    return average_daily_demand * 365


def calculate_demand_std(demand_history):
    if len(demand_history) < 2:
        raise ValueError(
            "At least two demand values are required"
        )

    return statistics.stdev(demand_history)

def calculate_eoq(
    annual_demand,
    ordering_cost,
    holding_cost
):
    if annual_demand <= 0:
        raise ValueError("Annual demand must be positive")

    if ordering_cost <= 0:
        raise ValueError("Ordering cost must be positive")

    if holding_cost <= 0:
        raise ValueError("Holding cost must be positive")

    eoq = math.sqrt(
        (2 * annual_demand * ordering_cost)
        / holding_cost
    )

    return eoq


def calculate_safety_stock(
    z_score,
    demand_std,
    lead_time_days
):
    if z_score < 0:
        raise ValueError("Z-score cannot be negative")

    if demand_std < 0:
        raise ValueError(
            "Demand standard deviation cannot be negative"
        )

    if lead_time_days <= 0:
        raise ValueError(
            "Lead time must be positive"
        )

    return (
        z_score
        * demand_std
        * math.sqrt(lead_time_days)
    )


def calculate_reorder_point(
    average_daily_demand,
    lead_time_days,
    safety_stock
):
    if average_daily_demand < 0:
        raise ValueError(
            "Average demand cannot be negative"
        )

    if lead_time_days <= 0:
        raise ValueError(
            "Lead time must be positive"
        )

    if safety_stock < 0:
        raise ValueError(
            "Safety stock cannot be negative"
        )

    return (
        average_daily_demand * lead_time_days
        + safety_stock
    )


def calculate_inventory_position(
    on_hand,
    on_order,
    reserved
):
    if on_hand < 0:
        raise ValueError(
            "On-hand inventory cannot be negative"
        )

    if on_order < 0:
        raise ValueError(
            "On-order inventory cannot be negative"
        )

    if reserved < 0:
        raise ValueError(
            "Reserved inventory cannot be negative"
        )

    return on_hand + on_order - reserved