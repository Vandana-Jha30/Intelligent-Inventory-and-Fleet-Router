from sqlalchemy import Column, Integer, ForeignKey

from app.database.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True)

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.warehouse_id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    on_hand = Column(Integer, nullable=False, default=0)

    reserved = Column(Integer, nullable=False, default=0)

    on_order = Column(Integer, nullable=False, default=0)