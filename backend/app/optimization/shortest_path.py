def find_shortest_path(graph, origin, destination):
    """

    Parameters
    ----------
    graph : dict
        Directed graph represented as:
        {
            "A": {"B": 4, "C": 2},
            "B": {"C": 1, "D": 5},
            ...
        }

        The values represent the distance/cost of each arc.

    origin : hashable
        Starting node.

    destination : hashable
        Destination node.

    Returns
    -------
    dict
        {
            "distance": shortest distance,
            "path": [origin, ..., destination]
        }

    Raises
    ------
    ValueError
        If the input is invalid or the destination is unreachable.
    """

    # Input validation

    if graph is None or not graph:
        raise ValueError("Graph is required")

    if origin not in graph:
        raise ValueError("Origin node is not present in graph")

    if destination not in graph:
        raise ValueError("Destination node is not present in graph")

    # Validate all neighboring nodes and edge costs
    for node, neighbors in graph.items():

        if neighbors is None:
            raise ValueError(
                "Neighbors must be provided for every node"
            )

        for neighbor, cost in neighbors.items():

            if neighbor not in graph:
                raise ValueError(
                    "Graph contains an unknown neighboring node"
                )

            if cost < 0:
                raise ValueError(
                    "Edge costs must be non-negative"
                )

    # Origin = destination

    if origin == destination:
        return {
            "distance": 0,
            "path": [origin]
        }

    # Initialize labels

    distances = {
        node: float("inf")
        for node in graph
    }

    previous = {
        node: None
        for node in graph
    }

    # Origin has distance zero
    distances[origin] = 0

    # Nodes whose shortest distance is finalized
    solved_nodes = set()

    # Label-setting procedure

    while len(solved_nodes) < len(graph):

        # Find the unsolved node with the
        # smallest temporary distance.
        current_node = None
        current_distance = float("inf")

        for node in graph:

            if node in solved_nodes:
                continue

            if distances[node] < current_distance:
                current_distance = distances[node]
                current_node = node

        # No reachable unsolved node remains.
        if current_node is None:
            break

        # Mark this node as solved.
        solved_nodes.add(current_node)

        # If destination is solved, its shortest
        # distance has been finalized.
        if current_node == destination:
            break


        # Update labels of candidate nodes

        for neighbor, edge_cost in graph[current_node].items():

            if neighbor in solved_nodes:
                continue

            candidate_distance = (
                distances[current_node]
                + edge_cost
            )

            # Improve the temporary label if
            # this route is shorter.
            if candidate_distance < distances[neighbor]:

                distances[neighbor] = candidate_distance

                # Store predecessor for path reconstruction.
                previous[neighbor] = current_node

    # Check reachability

    if distances[destination] == float("inf"):
        raise ValueError(
            "Destination is unreachable from origin"
        )

    # Reconstruct shortest path

    path = []

    current_node = destination

    while current_node is not None:

        path.append(current_node)

        if current_node == origin:
            break

        current_node = previous[current_node]

    # Reverse because reconstruction starts
    # from destination.
    path.reverse()

    return {
        "distance": distances[destination],
        "path": path
    }