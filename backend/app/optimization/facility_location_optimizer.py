from ortools.linear_solver import pywraplp

from app.optimization.distance_calculator import calculate_distance


def solve_facility_location(
    candidate_warehouses,
    delivery_locations,
    fixed_opening_costs=None,
    capacity_limits=None,
):
    """
    Solve the Capacitated Facility Location Problem.

    Decision variables:

        y[i] = 1 if candidate warehouse i is opened
               0 otherwise

        x[i][j] = quantity of customer j's demand
                  served by warehouse i

    Objective:

        Minimize:

            facility opening costs
            +
            warehouse-to-customer transportation costs

    Constraints:

        1. Every customer's demand must be completely satisfied.
        2. A warehouse can serve demand only if it is opened.
        3. Total demand assigned to a warehouse cannot exceed
           its capacity.
        4. Shipments must be non-negative.
        5. At least one facility must be opened.
    """

    # -----------------------------
    # Input validation
    # -----------------------------

    if not candidate_warehouses:
        raise ValueError(
            "At least one candidate warehouse is required"
        )

    if not delivery_locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    if fixed_opening_costs is None:
        fixed_opening_costs = [
            float(warehouse.operating_cost)
            for warehouse in candidate_warehouses
        ]

    if len(fixed_opening_costs) != len(candidate_warehouses):
        raise ValueError(
            "Number of fixed opening costs must match "
            "number of candidate warehouses"
        )

    if capacity_limits is None:
        capacity_limits = [
            float(warehouse.capacity)
            for warehouse in candidate_warehouses
        ]

    if len(capacity_limits) != len(candidate_warehouses):
        raise ValueError(
            "Number of capacity limits must match "
            "number of candidate warehouses"
        )

    for cost in fixed_opening_costs:
        if cost < 0:
            raise ValueError(
                "Facility opening costs cannot be negative"
            )

    for capacity in capacity_limits:
        if capacity < 0:
            raise ValueError(
                "Facility capacity cannot be negative"
            )

    demands = []

    for location in delivery_locations:

        demand = float(location.demand_quantity)

        if demand < 0:
            raise ValueError(
                "Delivery demand cannot be negative"
            )

        demands.append(demand)

    total_demand = sum(demands)

    total_capacity = sum(capacity_limits)

    if total_capacity < total_demand:
        raise ValueError(
            "Total facility capacity is insufficient "
            "for customer demand"
        )

    # -----------------------------
    # Calculate transportation costs
    # -----------------------------

    transportation_costs = []

    for warehouse in candidate_warehouses:

        row = []

        for location in delivery_locations:

            distance = calculate_distance(
                warehouse.latitude,
                warehouse.longitude,
                location.latitude,
                location.longitude
            )

            row.append(distance)

        transportation_costs.append(row)

    # -----------------------------
    # Create solver
    # -----------------------------

    solver = pywraplp.Solver.CreateSolver(
        "SCIP"
    )

    if solver is None:
        raise ValueError(
            "Unable to create OR-Tools facility location solver"
        )

    # -----------------------------
    # Decision variables
    # -----------------------------

    # y[i] = whether warehouse i is opened
    open_facility = []

    for i in range(len(candidate_warehouses)):

        variable = solver.IntVar(
            0,
            1,
            f"open_{i}"
        )

        open_facility.append(variable)

    # x[i][j] = demand served by warehouse i
    # for customer j
    shipments = []

    for i in range(len(candidate_warehouses)):

        row = []

        for j in range(len(delivery_locations)):

            variable = solver.NumVar(
                0,
                solver.infinity(),
                f"x_{i}_{j}"
            )

            row.append(variable)

        shipments.append(row)

    # -----------------------------
    # Demand constraints
    # -----------------------------

    for j in range(len(delivery_locations)):

        solver.Add(
            sum(
                shipments[i][j]
                for i in range(
                    len(candidate_warehouses)
                )
            )
            == demands[j]
        )

    # -----------------------------
    # Capacity constraints
    # -----------------------------

    for i in range(len(candidate_warehouses)):

        solver.Add(
            sum(
                shipments[i][j]
                for j in range(
                    len(delivery_locations)
                )
            )
            <= capacity_limits[i] * open_facility[i]
        )

    # -----------------------------
    # At least one facility
    # -----------------------------

    solver.Add(
        sum(open_facility) >= 1
    )

    # -----------------------------
    # Objective
    #
    # Fixed facility opening cost
    # +
    # transportation distance cost
    # -----------------------------

    objective = solver.Objective()

    for i in range(len(candidate_warehouses)):

        objective.SetCoefficient(
            open_facility[i],
            fixed_opening_costs[i]
        )

        for j in range(len(delivery_locations)):

            objective.SetCoefficient(
                shipments[i][j],
                transportation_costs[i][j]
            )

    objective.SetMinimization()

    # -----------------------------
    # Solve
    # -----------------------------

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:

        if status == pywraplp.Solver.INFEASIBLE:
            raise ValueError(
                "Facility location problem is infeasible"
            )

        raise ValueError(
            "Unable to find an optimal facility location solution"
        )

    # -----------------------------
    # Extract opened facilities
    # -----------------------------

    opened_facilities = []

    for i, warehouse in enumerate(candidate_warehouses):

        if open_facility[i].solution_value() > 0.5:

            opened_facilities.append({
                "warehouse_id": warehouse.warehouse_id,
                "warehouse_name": warehouse.name,
                "fixed_opening_cost": fixed_opening_costs[i],
                "capacity": capacity_limits[i]
            })

    # -----------------------------
    # Extract allocation
    # -----------------------------

    allocation_plan = []

    total_transportation_cost = 0.0

    for i, warehouse in enumerate(candidate_warehouses):

        for j, location in enumerate(delivery_locations):

            quantity = shipments[i][j].solution_value()

            if abs(quantity) < 1e-9:
                quantity = 0.0

            if quantity > 0:

                distance = transportation_costs[i][j]

                transportation_cost = (
                    quantity * distance
                )

                allocation_plan.append({
                    "warehouse_id": warehouse.warehouse_id,
                    "location_id": location.location_id,
                    "quantity": quantity,
                    "distance": distance,
                    "transportation_cost": transportation_cost
                })

                total_transportation_cost += (
                    transportation_cost
                )

    # -----------------------------
    # Cost calculation
    # -----------------------------

    total_fixed_cost = sum(
        fixed_opening_costs[i]
        for i in range(len(candidate_warehouses))
        if open_facility[i].solution_value() > 0.5
    )

    total_cost = (
        total_fixed_cost
        + total_transportation_cost
    )

    # -----------------------------
    # Facility summary
    # -----------------------------

    facility_summary = []

    for i, warehouse in enumerate(candidate_warehouses):

        assigned_quantity = sum(
            shipments[i][j].solution_value()
            for j in range(len(delivery_locations))
        )

        facility_summary.append({
            "warehouse_id": warehouse.warehouse_id,
            "opened": (
                open_facility[i].solution_value() > 0.5
            ),
            "capacity": capacity_limits[i],
            "assigned_quantity": assigned_quantity,
            "remaining_capacity": (
                capacity_limits[i] - assigned_quantity
            )
        })

    return {
        "total_demand": total_demand,
        "facilities_opened": len(opened_facilities),
        "total_fixed_cost": total_fixed_cost,
        "total_transportation_cost": total_transportation_cost,
        "total_cost": total_cost,
        "opened_facilities": opened_facilities,
        "allocation_plan": allocation_plan,
        "facility_summary": facility_summary
    }