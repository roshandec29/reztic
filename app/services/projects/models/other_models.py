from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.orm import relationship
from app.db.base import Base


class NearbyLandmark(Base):
    __tablename__ = "nearby_landmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID, ForeignKey("projects.id"), nullable=False)

    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., "hospital", "school", "mall"
    distance_km = Column(Float, nullable=True)
    location_url = Column(String(255), nullable=True)
    icon_url = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    icon_url = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProjectAmenity(Base):
    __tablename__ = "project_amenities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    amenity_id = Column(UUID, ForeignKey("amenities.id"), nullable=False)

    is_available = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    amenity = relationship("Amenity", backref="ProjectAmenity", cascade="all, delete")


class ParkingCharge(Base):
    __tablename__ = 'parking_charges'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID, ForeignKey("projects.id"), nullable=False)

    parking_type = Column(String(20), nullable=False)

    amount_type = Column(String(10), nullable=False)  # fixed, per_sqft, percentage
    amount_value = Column(Float, nullable=False)

    unit_type = Column(String(100), nullable=True)

    max_allowed_per_unit = Column(Integer, nullable=True)

    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
