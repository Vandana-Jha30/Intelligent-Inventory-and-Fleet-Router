from sqlalchemy.orm import Session

from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory

from app.optimization.distance_calculator import calculate_distance
from app.optimization.min_cost_flow_solver import solve_min_cost_flow
from app.optimization.vehicle_routing_solver import solve_vehicle_routing_optimized

from app.schemas.min_cost_flow import (
    FlowNodeRequest,
    FlowArcRequest,
)

from app.services.inventory_service import analyze_inventory_with_forecast

from app.optimization.warehouse_allocation import (
    nearest_warehouse_allocation,
)


def create_supply_chain_plan(
    db: Session,
    product_id: int,
    warehouse_id: int,
    depot_id: int,
    delivery_location_ids=None,
    window: int = 3,
):
    """Create an integrated inventory and distribution plan.

    Inventory replenishment is evaluated for the selected warehouse.

    Distribution uses available inventory for the selected product
    across all warehouses and allocates it to customer locations
    using minimum-cost flow.

    Vehicle routing then creates the last-mile delivery routes.
    """

    # ---------------------------------------------------------
    # Inventory analysis for the requested warehouse
    # ---------------------------------------------------------

    inventory_analysis = analyze_inventory_with_forecast(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        window=window,
    )

    warehouse = db.query(Warehouse).filter(
        Warehouse.warehouse_id == warehouse_id
    ).first()

    if warehouse is None:
        raise ValueError("Warehouse not found")

    # ---------------------------------------------------------
    # Depot
    # ---------------------------------------------------------

    depot = db.query(Depot).filter(
        Depot.depot_id == depot_id
    ).first()

    if depot is None:
        raise ValueError("Depot not found")

    # ---------------------------------------------------------
    # Delivery locations
    # ---------------------------------------------------------

    query = db.query(DeliveryLocation)

    if delivery_location_ids is not None:

        if len(delivery_location_ids) != len(
            set(delivery_location_ids)
        ):
            raise ValueError(
                "Each delivery location can appear only once"
            )

        locations = query.filter(
            DeliveryLocation.location_id.in_(
                delivery_location_ids
            )
        ).all()

        locations_by_id = {
            location.location_id: location
            for location in locations
        }

        missing_ids = [
            location_id
            for location_id in delivery_location_ids
            if location_id not in locations_by_id
        ]

        if missing_ids:
            raise ValueError(
                f"Delivery location not found: {missing_ids[0]}"
            )

        # Preserve the order requested by the caller.
        locations = [
            locations_by_id[location_id]
            for location_id in delivery_location_ids
        ]

    else:
        locations = query.order_by(
            DeliveryLocation.location_id
        ).all()

    if not locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    # ---------------------------------------------------------
    # Vehicles
    # ---------------------------------------------------------

    vehicles = db.query(Vehicle).all()

    if not vehicles:
        raise ValueError(
            "At least one vehicle is required"
        )

    # ---------------------------------------------------------
    # Customer demand
    # ---------------------------------------------------------

    delivery_demand = sum(
        float(location.demand_quantity)
        for location in locations
    )

    # ---------------------------------------------------------
    # Available inventory across all warehouses
    # ---------------------------------------------------------

    inventory_records = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).all()

    if not inventory_records:
        raise ValueError("Inventory record not found")

    inventory_by_warehouse = {}

    for record in inventory_records:
        available = max(
            0.0,
            float(record.on_hand)
            - float(record.reserved),
        )

        if available > 0:
            inventory_by_warehouse[
                record.warehouse_id
            ] = available

    if not inventory_by_warehouse:
        raise ValueError(
            "Insufficient available inventory to satisfy delivery demand"
        )

    total_available_inventory = sum(
        inventory_by_warehouse.values()
    )

    if total_available_inventory < delivery_demand:
        raise ValueError(
            "Insufficient available inventory to satisfy delivery demand"
        )

    # ---------------------------------------------------------
    # Load warehouses participating in the flow
    # ---------------------------------------------------------

    warehouse_ids = list(
        inventory_by_warehouse.keys()
    )

    warehouses = db.query(Warehouse).filter(
        Warehouse.warehouse_id.in_(warehouse_ids)
    ).all()

    warehouses_by_id = {
        item.warehouse_id: item
        for item in warehouses
    }

    # ---------------------------------------------------------
    # Minimum-Cost Flow
    # ---------------------------------------------------------

    flow_nodes = []

    # Warehouse supply nodes
    for (
        current_warehouse_id,
        available_inventory,
    ) in inventory_by_warehouse.items():

        current_warehouse = warehouses_by_id.get(
            current_warehouse_id
        )

        if current_warehouse is None:
            continue

        flow_nodes.append(
            FlowNodeRequest(
                node_id=current_warehouse_id,
                name=current_warehouse.name,
                supply=available_inventory,
                demand=0,
            )
        )

    # Customer demand nodes
    #
    # Use a separate namespace so warehouse IDs and customer IDs
    # cannot accidentally collide.
    customer_node_ids = {}

    for index, location in enumerate(
        locations,
        start=1,
    ):

        node_id = 1_000_000 + index

        customer_node_ids[
            location.location_id
        ] = node_id

        flow_nodes.append(
            FlowNodeRequest(
                node_id=node_id,
                name=location.location_name,
                supply=0,
                demand=float(
                    location.demand_quantity
                ),
            )
        )

    # Unused inventory node
    unused_inventory = (
        total_available_inventory
        - delivery_demand
    )

    if unused_inventory > 0:

        unused_node_id = 2_000_000

        flow_nodes.append(
            FlowNodeRequest(
                node_id=unused_node_id,
                name="Unused Inventory",
                supply=0,
                demand=unused_inventory,
            )
        )

    # ---------------------------------------------------------
    # Warehouse → Customer arcs
    # ---------------------------------------------------------

    flow_arcs = []

    for (
        current_warehouse_id,
        available_inventory,
    ) in inventory_by_warehouse.items():

        current_warehouse = warehouses_by_id.get(
            current_warehouse_id
        )

        if current_warehouse is None:
            continue

        for location in locations:

            distance = calculate_distance(
                current_warehouse.latitude,
                current_warehouse.longitude,
                location.latitude,
                location.longitude,
            )

            customer_node_id = customer_node_ids[
                location.location_id
            ]

            flow_arcs.append(
                FlowArcRequest(
                    from_node=current_warehouse_id,
                    to_node=customer_node_id,
                    capacity=min(
                        available_inventory,
                        float(
                            location.demand_quantity
                        ),
                    ),
                    cost=distance,
                )
            )

    # ---------------------------------------------------------
    # Unused inventory arcs
    # ---------------------------------------------------------

    if unused_inventory > 0:

        for (
            current_warehouse_id,
            available_inventory,
        ) in inventory_by_warehouse.items():

            flow_arcs.append(
                FlowArcRequest(
                    from_node=current_warehouse_id,
                    to_node=unused_node_id,
                    capacity=available_inventory,
                    cost=0,
                )
            )

    min_cost_flow = solve_min_cost_flow(
        flow_nodes,
        flow_arcs,
    )

    # ---------------------------------------------------------
    # Build human-readable warehouse → customer allocation
    # ---------------------------------------------------------

    allocation = []

    for item in min_cost_flow["flow_plan"]:

        from_node = item["from_node"]
        to_node = item["to_node"]

        # Ignore the unused-inventory flow.
        if to_node == 2_000_000:
            continue

        current_warehouse = warehouses_by_id[
            from_node
        ]

        location = next(
            location
            for location in locations
            if customer_node_ids[
                location.location_id
            ] == to_node
        )

        allocation.append(
            {
                "warehouse_id":
                    current_warehouse.warehouse_id,
                "warehouse_name":
                    current_warehouse.name,
                "location_id":
                    location.location_id,
                "location_name":
                    location.location_name,
                "quantity":
                    item["flow"],
                "distance_km":
                    item["unit_cost"],
                "transportation_cost":
                    item["total_cost"],
            }
        )

    # ---------------------------------------------------------
    # Baseline Allocation
    # ---------------------------------------------------------

    baseline_allocation = nearest_warehouse_allocation(
        warehouses=warehouses,
        inventory_by_warehouse=inventory_by_warehouse,
        delivery_locations=locations,
    )

    baseline_cost = baseline_allocation[
        "total_cost"
    ]

    optimized_cost = min_cost_flow[
        "total_cost"
    ]

    if baseline_cost > 0:
        cost_improvement = (
            (baseline_cost - optimized_cost)
            / baseline_cost
        ) * 100
    else:
        cost_improvement = 0.0

    # ---------------------------------------------------------
    # Vehicle Routing
    # ---------------------------------------------------------

    routing = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles,
    )

    return {
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "depot_id": depot_id,
        "delivery_demand": delivery_demand,
        "available_inventory":
            total_available_inventory,
        "inventory_analysis":
            inventory_analysis,
        "min_cost_flow":
            min_cost_flow,
        "allocation":
            allocation,
        "baseline_allocation":
            baseline_allocation,
        "baseline_cost":
            baseline_cost,
        "optimized_cost":
            optimized_cost,
        "cost_improvement_percent":
            cost_improvement,
        "routing":
            routing,
    }