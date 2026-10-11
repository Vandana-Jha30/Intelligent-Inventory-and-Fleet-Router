from pathlib import Path
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

BENCHMARK_FILE = Path(__file__).with_name("A-n32-k5.vrp")
PUBLISHED_OPTIMUM = 784
NUM_VEHICLES = 5
VEHICLE_CAPACITY = 100

def read_vrp_file(path):
    coordinates, demands = {}, {}
    depot = None
    section = None
    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue
            if line == "NODE_COORD_SECTION":
                section = "coordinates"; continue
            if line == "DEMAND_SECTION":
                section = "demands"; continue
            if line == "DEPOT_SECTION":
                section = "depot"; continue
            if line == "EOF":
                break
            if section == "coordinates":
                node, x, y = line.split()
                coordinates[int(node)] = (float(x), float(y))
            elif section == "demands":
                node, demand = line.split()
                demands[int(node)] = int(demand)
            elif section == "depot":
                node = int(line)
                if node == -1:
                    section = None
                else:
                    depot = node
    if depot is None:
        raise ValueError("Depot was not found")
    return coordinates, demands, depot

def euclidean_distance(a, b):
    d = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return int(d + 0.5)

def solve_benchmark(coordinates, demands, depot):
    node_ids = sorted(coordinates)
    depot_index = node_ids.index(depot)

    manager = pywrapcp.RoutingIndexManager(
        len(node_ids), NUM_VEHICLES, depot_index
    )
    routing = pywrapcp.RoutingModel(manager)

    matrix = [
        [euclidean_distance(coordinates[i], coordinates[j]) for j in node_ids]
        for i in node_ids
    ]

    def distance_callback(from_index, to_index):
        return matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    distance_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback_index)

    def demand_callback(index):
        return demands[node_ids[manager.IndexToNode(index)]]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0,
        [VEHICLE_CAPACITY] * NUM_VEHICLES,
        True, "Capacity"
    )

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.seconds = 30

    solution = routing.SolveWithParameters(params)
    if solution is None:
        raise RuntimeError("No feasible CVRP solution found")

    routes, total_distance = [], 0

    for vehicle in range(NUM_VEHICLES):
        index = routing.Start(vehicle)
        customers, route_distance, route_demand = [], 0, 0

        while not routing.IsEnd(index):
            current = manager.IndexToNode(index)
            node = node_ids[current]
            if node != depot:
                customers.append(node)
                route_demand += demands[node]

            previous = index
            index = solution.Value(routing.NextVar(index))
            nxt = manager.IndexToNode(index)
            route_distance += matrix[current][nxt]

        total_distance += route_distance
        routes.append((vehicle + 1, customers, route_demand, route_distance))

    return total_distance, routes

def main():
    coordinates, demands, depot = read_vrp_file(BENCHMARK_FILE)
    total_demand = sum(demands.values()) - demands[depot]
    total_distance, routes = solve_benchmark(coordinates, demands, depot)

    print("=" * 60)
    print("A-n32-k5 CVRPLIB BENCHMARK")
    print("=" * 60)
    print(f"Customers:         {len(coordinates)-1}")
    print(f"Vehicles:          {NUM_VEHICLES}")
    print(f"Capacity/vehicle:  {VEHICLE_CAPACITY}")
    print(f"Total demand:      {total_demand}")
    print(f"Published optimum: {PUBLISHED_OPTIMUM}")
    print(f"Solver distance:   {total_distance}")
    print(f"Absolute gap:      {total_distance - PUBLISHED_OPTIMUM}")
    print(f"Gap percentage:    {(total_distance-PUBLISHED_OPTIMUM)/PUBLISHED_OPTIMUM*100:.2f}%")
    print("-" * 60)

    for vehicle, customers, demand, distance in routes:
        print(
            f"Vehicle {vehicle}: demand={demand}, "
            f"distance={distance}, customers={customers}"
        )

    print("-" * 60)
    if total_distance == PUBLISHED_OPTIMUM:
        print("RESULT: MATCHES PUBLISHED OPTIMUM")
    else:
        print("RESULT: FEASIBLE SOLUTION FOUND; DOES NOT MATCH OPTIMUM")
    print("=" * 60)

if __name__ == "__main__":
    main()
