from sqlalchemy.orm import Session

from app.models.demand import DemandHistory
from app.schemas.demand import DemandCreate


def create_demand(
    db: Session,
    demand_data: DemandCreate
):
    demand = DemandHistory(
        product_id=demand_data.product_id,
        warehouse_id=demand_data.warehouse_id,
        demand_date=demand_data.demand_date,
        quantity=demand_data.quantity
    )

    db.add(demand)
    db.commit()
    db.refresh(demand)

    return demand


def get_demands(db: Session):
    return db.query(DemandHistory).all()


def get_demand(
    db: Session,
    demand_id: int
):
    return db.query(DemandHistory).filter(
        DemandHistory.demand_id == demand_id
    ).first()


def delete_demand(
    db: Session,
    demand_id: int
):
    demand = get_demand(db, demand_id)

    if demand is None:
        return False

    db.delete(demand)
    db.commit()

    return True