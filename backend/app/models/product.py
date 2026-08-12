from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)

    sku = Column(String, unique=True, nullable=False, index=True)

    name = Column(String, nullable=False)

    unit_cost = Column(Float, nullable=False)

    ordering_cost = Column(Float, nullable=False)

    holding_cost = Column(Float, nullable=False)

    lead_time_days = Column(Integer, nullable=False)

    service_level = Column(Float, nullable=False)