from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from app.database.database import Base


class DemandHistory(Base):
    __tablename__ = "demand_history"

    demand_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.warehouse_id"),
        nullable=False
    )

    demand_date = Column(
        Date,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )