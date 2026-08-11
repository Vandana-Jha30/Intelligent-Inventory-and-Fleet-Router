from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    capacity = Column(Integer, nullable=False)

    operating_cost = Column(Float, nullable=False)