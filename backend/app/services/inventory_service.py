from statistics import NormalDist

from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.demand import DemandHistory

from app.schemas.inventory import InventoryCreate

from app.optimization.inventory_optimizer import (
    calculate_average_demand,
    calculate_annual_demand,
    calculate_demand_std,
    calculate_eoq,
    calculate_safety_stock,
    calculate_reorder_point,
    calculate_inventory_position,
)

from app.optimization.demand_forecaster import (
    moving_average_forecast
)

def create_inventory(
    db: Session,
    inventory_data: InventoryCreate
):
    existing_inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == inventory_data.warehouse_id,
        Inventory.product_id == inventory_data.product_id
    ).first()

    if existing_inventory is not None:
        raise ValueError(
            "Inventory already exists for this product and warehouse"
        )

    inventory = Inventory(
        warehouse_id=inventory_data.warehouse_id,
        product_id=inventory_data.product_id,
        on_hand=inventory_data.on_hand,
        reserved=inventory_data.reserved,
        on_order=inventory_data.on_order
    )

    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory


def get_inventories(db: Session):
    return db.query(Inventory).all()


def get_inventory(
    db: Session,
    inventory_id: int
):
    return db.query(Inventory).filter(
        Inventory.inventory_id == inventory_id
    ).first()


def update_inventory(
    db: Session,
    inventory_id: int,
    inventory_data: InventoryCreate
):
    inventory = get_inventory(db, inventory_id)

    if inventory is None:
        return None

    existing_inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == inventory_data.warehouse_id,
        Inventory.product_id == inventory_data.product_id,
        Inventory.inventory_id != inventory_id
    ).first()

    if existing_inventory is not None:
        raise ValueError(
            "Inventory already exists for this product and warehouse"
        )

    inventory.warehouse_id = inventory_data.warehouse_id
    inventory.product_id = inventory_data.product_id
    inventory.on_hand = inventory_data.on_hand
    inventory.reserved = inventory_data.reserved
    inventory.on_order = inventory_data.on_order

    db.commit()
    db.refresh(inventory)

    return inventory


def delete_inventory(
    db: Session,
    inventory_id: int
):
    inventory = get_inventory(db, inventory_id)

    if inventory is None:
        return False

    db.delete(inventory)
    db.commit()

    return True


def analyze_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int
):
    # 1. Get product
    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if product is None:
        raise ValueError("Product not found")

    # 2. Get warehouse
    warehouse = db.query(Warehouse).filter(
        Warehouse.warehouse_id == warehouse_id
    ).first()

    if warehouse is None:
        raise ValueError("Warehouse not found")

    # 3. Get demand history
    demand_records = db.query(DemandHistory).filter(
        DemandHistory.product_id == product_id,
        DemandHistory.warehouse_id == warehouse_id
    ).order_by(
        DemandHistory.demand_date
    ).all()

    if len(demand_records) < 2:
        raise ValueError(
            "At least two demand records are required"
        )

    demand_history = [
        record.quantity
        for record in demand_records
    ]

    # 4. Calculate demand statistics
    average_daily_demand = calculate_average_demand(
        demand_history
    )

    annual_demand = calculate_annual_demand(
        average_daily_demand
    )

    demand_std = calculate_demand_std(
        demand_history
    )

    # 5. Calculate EOQ
    eoq = calculate_eoq(
        annual_demand=annual_demand,
        ordering_cost=product.ordering_cost,
        holding_cost=product.holding_cost
    )

    # 6. Convert service level to Z-score
    z_score = NormalDist().inv_cdf(
        product.service_level
    )

    # 7. Calculate Safety Stock
    safety_stock = calculate_safety_stock(
        z_score=z_score,
        demand_std=demand_std,
        lead_time_days=product.lead_time_days
    )

    # 8. Calculate Reorder Point
    reorder_point = calculate_reorder_point(
        average_daily_demand=average_daily_demand,
        lead_time_days=product.lead_time_days,
        safety_stock=safety_stock
    )

    # 9. Get inventory
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).first()

    if inventory is None:
        raise ValueError(
            "Inventory record not found"
        )

    # 10. Calculate inventory position
    inventory_position = calculate_inventory_position(
        on_hand=inventory.on_hand,
        on_order=inventory.on_order,
        reserved=inventory.reserved
    )

    # 11. Replenishment decision
    replenishment_required = (
    inventory_position <= reorder_point
    )

    if replenishment_required:
        recommended_order_quantity = eoq
    else:
        recommended_order_quantity = 0

    return {
        "product_id": product_id,
        "warehouse_id": warehouse_id,

        "average_daily_demand": average_daily_demand,
        "annual_demand": annual_demand,
        "demand_std": demand_std,

        "eoq": eoq,
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,

        "on_hand": inventory.on_hand,
        "reserved": inventory.reserved,
        "on_order": inventory.on_order,
        "inventory_position": inventory_position,

        "replenishment_required": replenishment_required,
        "recommended_order_quantity": recommended_order_quantity
    }


def analyze_inventory_with_forecast(
    db: Session,
    product_id: int,
    warehouse_id: int,
    window: int = 3
):
    # 1. Get product
    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if product is None:
        raise ValueError("Product not found")

    # 2. Get warehouse
    warehouse = db.query(Warehouse).filter(
        Warehouse.warehouse_id == warehouse_id
    ).first()

    if warehouse is None:
        raise ValueError("Warehouse not found")

    # 3. Get demand history
    demand_records = db.query(DemandHistory).filter(
        DemandHistory.product_id == product_id,
        DemandHistory.warehouse_id == warehouse_id
    ).order_by(
        DemandHistory.demand_date
    ).all()

    if len(demand_records) < 2:
        raise ValueError(
            "At least two demand records are required"
        )

    demand_history = [
        record.quantity
        for record in demand_records
    ]

    # 4. Calculate forecast
    forecast_daily_demand = moving_average_forecast(
        demand_history,
        window
    )

    # 5. Calculate annual demand from forecast
    annual_demand = calculate_annual_demand(
        forecast_daily_demand
    )

    # 6. Historical demand variation for safety stock
    demand_std = calculate_demand_std(
        demand_history
    )

    # 7. Calculate EOQ
    eoq = calculate_eoq(
        annual_demand=annual_demand,
        ordering_cost=product.ordering_cost,
        holding_cost=product.holding_cost
    )

    # 8. Convert service level to Z-score
    z_score = NormalDist().inv_cdf(
        product.service_level
    )

    # 9. Calculate Safety Stock
    safety_stock = calculate_safety_stock(
        z_score=z_score,
        demand_std=demand_std,
        lead_time_days=product.lead_time_days
    )

    # 10. Calculate Reorder Point using forecast
    reorder_point = calculate_reorder_point(
        average_daily_demand=forecast_daily_demand,
        lead_time_days=product.lead_time_days,
        safety_stock=safety_stock
    )

    # 11. Get inventory
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).first()

    if inventory is None:
        raise ValueError(
            "Inventory record not found"
        )

    # 12. Calculate inventory position
    inventory_position = calculate_inventory_position(
        on_hand=inventory.on_hand,
        on_order=inventory.on_order,
        reserved=inventory.reserved
    )

    # 13. Replenishment decision
    replenishment_required = (
        inventory_position <= reorder_point
    )

    if replenishment_required:
        recommended_order_quantity = eoq
    else:
        recommended_order_quantity = 0

    return {
        "product_id": product_id,
        "warehouse_id": warehouse_id,

        "forecast_daily_demand": forecast_daily_demand,
        "annual_demand": annual_demand,
        "demand_std": demand_std,

        "eoq": eoq,
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,

        "on_hand": inventory.on_hand,
        "reserved": inventory.reserved,
        "on_order": inventory.on_order,
        "inventory_position": inventory_position,

        "replenishment_required": replenishment_required,
        "recommended_order_quantity": recommended_order_quantity
    }