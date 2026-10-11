from ortools.linear_solver import pywraplp

from app.optimization.distance_calculator import (
    calculate_distance
)


def solve_transportation(
    warehouses,
    delivery_locations
):
    """
    Solve the classical Transportation Problem.

    Decision variable:
        x[i][j] = quantity shipped from warehouse i
                  to delivery location j.

    Objective:
        Minimize total transportation cost.

    Supply:
        Available warehouse inventory is calculated as:
            on_hand - reserved

    Demand:
        demand_quantity of each delivery location.

    Constraints:
        1. Shipments cannot exceed warehouse supply.
        2. Every customer demand must be completely satisfied.
        3. Shipment quantities must be non-negative.

    Transportation cost:
        Distance between warehouse and customer.

    Notes:
        Vehicle routing is intentionally handled separately.
        This solver determines WHAT quantity should move
        between warehouses and customers.
    """

    # ---------------------------------
    # Input validation
    # ---------------------------------

    if not warehouses:
        raise ValueError(
            "At least one warehouse is required"
        )

    if not delivery_locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    # ---------------------------------
    # Calculate warehouse supply
    # ---------------------------------

    supplies = []

    for warehouse in warehouses:

        supply = (
            warehouse.on_hand
            - warehouse.reserved
        )

        if supply < 0:
            raise ValueError(
                "Warehouse available inventory cannot be negative"
            )

        supplies.append(float(supply))

    # ---------------------------------
    # Calculate customer demand
    # ---------------------------------

    demands = []

    for location in delivery_locations:

        demand = float(
            location.demand_quantity
        )

        if demand < 0:
            raise ValueError(
                "Delivery demand cannot be negative"
            )

        demands.append(demand)

    total_supply = sum(supplies)
    total_demand = sum(demands)

    # ---------------------------------
    # Feasibility check
    # ---------------------------------

    if total_supply < total_demand:
        raise ValueError(
            "Total warehouse supply is insufficient "
            "for customer demand"
        )

    # ---------------------------------
    # Create cost matrix
    #
    # Cost currently represents geographic
    # distance between warehouse and customer.
    #
    # Vehicle-specific routing costs are handled
    # later by the fleet-routing layer.
    # ---------------------------------

    cost_matrix = []

    for warehouse in warehouses:

        row = []

        for location in delivery_locations:

            distance = calculate_distance(
                warehouse.latitude,
                warehouse.longitude,
                location.latitude,
                location.longitude
            )

            row.append(distance)

        cost_matrix.append(row)

    # ---------------------------------
    # Create linear programming solver
    # ---------------------------------

    solver = pywraplp.Solver.CreateSolver(
        "SCIP"
    )

    if solver is None:
        raise ValueError(
            "Unable to create OR-Tools linear solver"
        )

    # ---------------------------------
    # Decision variables
    #
    # x[i][j] =
    # quantity shipped from warehouse i
    # to delivery location j
    # ---------------------------------

    shipments = []

    for i in range(len(warehouses)):

        row = []

        for j in range(len(delivery_locations)):

            variable = solver.NumVar(
                0,
                solver.infinity(),
                f"x_{i}_{j}"
            )

            row.append(variable)

        shipments.append(row)

    # ---------------------------------
    # Supply constraints
    #
    # Total shipped from a warehouse
    # cannot exceed available supply.
    # ---------------------------------

    for i in range(len(warehouses)):

        solver.Add(
            sum(
                shipments[i][j]
                for j in range(
                    len(delivery_locations)
                )
            )
            <= supplies[i]
        )

    # ---------------------------------
    # Demand constraints
    #
    # Every delivery location must receive
    # exactly its required demand.
    # ---------------------------------

    for j in range(len(delivery_locations)):

        solver.Add(
            sum(
                shipments[i][j]
                for i in range(len(warehouses))
            )
            == demands[j]
        )

    # ---------------------------------
    # Objective
    #
    # Minimize total transportation distance.
    # ---------------------------------

    objective = solver.Objective()

    for i in range(len(warehouses)):

        for j in range(len(delivery_locations)):

            objective.SetCoefficient(
                shipments[i][j],
                cost_matrix[i][j]
            )

    objective.SetMinimization()

    # ---------------------------------
    # Solve
    # ---------------------------------

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:

        if status == pywraplp.Solver.INFEASIBLE:
            raise ValueError(
                "Transportation problem is infeasible"
            )

        raise ValueError(
            "Unable to find an optimal transportation solution"
        )

    # ---------------------------------
    # Extract solution
    # ---------------------------------

    shipment_plan = []

    total_distance = 0.0

    for i, warehouse in enumerate(warehouses):

        warehouse_total = 0.0

        for j, location in enumerate(
            delivery_locations
        ):

            quantity = shipments[i][j].solution_value()

            # Ignore numerical noise.
            if abs(quantity) < 1e-9:
                quantity = 0.0

            if quantity > 0:

                distance = cost_matrix[i][j]

                shipment_cost = (
                    quantity * distance
                )

                shipment_plan.append({
                    "warehouse_id": warehouse.warehouse_id,
                    "location_id": location.location_id,
                    "quantity": quantity,
                    "distance": distance,
                    "transportation_cost": shipment_cost
                })

                warehouse_total += quantity

                total_distance += shipment_cost

    # ---------------------------------
    # Calculate utilization
    # ---------------------------------

    warehouse_summary = []

    for i, warehouse in enumerate(warehouses):

        shipped_quantity = sum(
            shipments[i][j].solution_value()
            for j in range(
                len(delivery_locations)
            )
        )

        warehouse_summary.append({
            "warehouse_id": warehouse.warehouse_id,
            "available_supply": supplies[i],
            "shipped_quantity": shipped_quantity,
            "remaining_supply": (
                supplies[i] - shipped_quantity
            )
        })

    return {
        "total_supply": total_supply,
        "total_demand": total_demand,
        "total_transportation_cost": total_distance,
        "shipment_plan": shipment_plan,
        "warehouse_summary": warehouse_summary
    }