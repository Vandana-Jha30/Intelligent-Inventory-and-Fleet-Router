from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from app.database.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint(
            "warehouse_id",
            "product_id",
            name="uq_inventory_warehouse_product"
        ),
    )

    inventory_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

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

    on_hand = Column(
        Integer,
        nullable=False,
        default=0
    )

    reserved = Column(
        Integer,
        nullable=False,
        default=0
    )

    on_order = Column(
        Integer,
        nullable=False,
        default=0
    )