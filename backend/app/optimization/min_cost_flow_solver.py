from ortools.linear_solver import pywraplp


def solve_min_cost_flow(nodes, arcs):
    """Solve a minimum-cost flow problem on a directed network.

    Each node must provide:
        node_id, supply, demand

    Each arc must provide:
        from_node, to_node, capacity, cost

    Positive node supply means available flow.
    Positive node demand means required flow.
    Flow conservation is enforced at every node.
    """
    if not nodes:
        raise ValueError("At least one node is required")

    if not arcs:
        raise ValueError("At least one arc is required")

    node_ids = [node.node_id for node in nodes]

    if len(node_ids) != len(set(node_ids)):
        raise ValueError("Each node can appear only once")

    node_map = set(node_ids)

    total_supply = 0.0
    total_demand = 0.0

    for node in nodes:
        supply = float(node.supply)
        demand = float(node.demand)

        if supply < 0:
            raise ValueError("Node supply cannot be negative")

        if demand < 0:
            raise ValueError("Node demand cannot be negative")

        if supply > 0 and demand > 0:
            raise ValueError("A node cannot have both supply and demand")

        total_supply += supply
        total_demand += demand

    if abs(total_supply - total_demand) > 1e-9:
        raise ValueError("Total supply must equal total demand")

    # Validate arcs
    for arc in arcs:
        if arc.from_node not in node_map:
            raise ValueError(f"Unknown source node: {arc.from_node}")

        if arc.to_node not in node_map:
            raise ValueError(f"Unknown destination node: {arc.to_node}")

        if arc.from_node == arc.to_node:
            raise ValueError("An arc cannot connect a node to itself")

        if float(arc.capacity) < 0:
            raise ValueError("Arc capacity cannot be negative")

        if float(arc.cost) < 0:
            raise ValueError("Arc cost cannot be negative")

    solver = pywraplp.Solver.CreateSolver("SCIP")

    if solver is None:
        raise RuntimeError("SCIP solver is not available")

    flow_variables = []

    outgoing = {node_id: [] for node_id in node_ids}
    incoming = {node_id: [] for node_id in node_ids}

    for index, arc in enumerate(arcs):
        variable = solver.NumVar(
            0.0,
            float(arc.capacity),
            f"flow_{index}",
        )

        flow_variables.append(variable)

        outgoing[arc.from_node].append(variable)
        incoming[arc.to_node].append(variable)

    # Flow conservation
    for node in nodes:
        net_supply = float(node.supply) - float(node.demand)

        solver.Add(
            solver.Sum(outgoing[node.node_id])
            - solver.Sum(incoming[node.node_id])
            == net_supply
        )

    # Minimize total transportation cost
    objective = solver.Objective()

    for variable, arc in zip(flow_variables, arcs):
        objective.SetCoefficient(variable, float(arc.cost))

    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.INFEASIBLE:
        raise ValueError("No feasible flow exists for the supplied network")

    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError(
            "Minimum-cost flow solver did not find an optimal solution"
        )

    flow_plan = []

    for variable, arc in zip(flow_variables, arcs):
        flow = variable.solution_value()

        if flow > 1e-9:
            flow_plan.append(
                {
                    "from_node": arc.from_node,
                    "to_node": arc.to_node,
                    "flow": flow,
                    "capacity": float(arc.capacity),
                    "unit_cost": float(arc.cost),
                    "total_cost": flow * float(arc.cost),
                }
            )

    return {
        "total_supply": total_supply,
        "total_demand": total_demand,
        "total_flow": total_supply,
        "total_cost": objective.Value(),
        "flow_plan": flow_plan,
    }
