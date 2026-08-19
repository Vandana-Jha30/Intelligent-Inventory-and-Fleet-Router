from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_number = Column(
        String,
        unique=True,
        nullable=False
    )

    capacity = Column(
        Float,
        nullable=False
    )

    fixed_cost = Column(
        Float,
        nullable=False,
        default=0
    )

    cost_per_km = Column(
        Float,
        nullable=False
    )