from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class Depot(Base):
    __tablename__ = "depots"

    depot_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    depot_name = Column(
        String,
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )