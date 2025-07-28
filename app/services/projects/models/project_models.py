from sqlalchemy import Column, String, Text, Date, DECIMAL, JSON, ForeignKey, Integer, Boolean, DateTime, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    developer_id = Column(UUID(as_uuid=True), ForeignKey("developers.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    development_stage = Column(String, nullable=False)  # "launched", "under_construction"
    is_featured = Column(Boolean, default=False)  # for highlighting on homepage
    badges = Column(ARRAY(String), default=[])  # ["New Project", "5% Commission"]
    possession_date = Column(Date)
    project_type = Column(String, nullable=False)
    property_type = Column(String, nullable=False)
    rera_number = Column(String)
    furnishing_status = Column(String, default="NA")
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    units = relationship("ProjectUnit", backref="project", cascade="all, delete-orphan")
    media = relationship("ProjectMedia", backref="project", cascade="all, delete-orphan")
    locality = relationship("Locality", backref="project")
    commissions = relationship("ProjectCommission", back_populates="project", cascade="all, delete-orphan")
    nearby_landmarks = relationship("NearbyLandmark", backref="project", cascade="all, delete-orphan")
    additional_charges = relationship("AdditionalCharge", backref="project", cascade="all, delete-orphan")
    payment_plan = relationship("PaymentPlan", backref="project", cascade="all, delete-orphan")
    parking = relationship("ParkingCharge", backref="project", cascade="all, delete-orphan")
    amenities = relationship("ProjectAmenity", backref="project", cascade="all, delete-orphan")


class ProjectUnit(Base):
    __tablename__ = "project_units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    unit_type = Column(String, nullable=False)  # "2 BHK", "Studio"
    layout_name = Column(String, nullable=True)
    carpet_area_value = Column(Float, nullable=False)
    super_area_value = Column(Float, nullable=False)
    area_unit = Column(String(10), default="sqft")  # Enum: sqft, sqm, acres, etc.
    bedrooms = Column(Integer, nullable=True)
    balconies = Column(Integer, nullable=True)
    total_units = Column(Integer)
    available_units = Column(Integer)
    base_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    eoi_amount = Column(Float, default=0)
    floor_plan_media_url = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProjectMedia(Base):
    __tablename__ = "project_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    type = Column(String, nullable=False)  # image, video, pdf
    content_type = Column(String, nullable=True)
    is_featured = Column(Boolean, default=False)
    media_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)
    meta_json = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)


class ResaleListing(Base):
    __tablename__ = "resale_listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_unit_id = Column(UUID(as_uuid=True), ForeignKey("project_units.id"), nullable=False)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    unit_type = Column(String)
    size_sqft = Column(Integer)
    asking_price = Column(DECIMAL)
    floor = Column(Integer)
    description = Column(Text)
    possession_status = Column(String)  # ready_to_move, under_construction
    verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Developer(Base):
    __tablename__ = "developers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    website = Column(String)
    logo_url = Column(Text)
    rera_number = Column(String, unique=True)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProjectCommission(Base):
    __tablename__ = "project_commissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    commission_type = Column(String, nullable=False)  # 'fixed' or '%'
    calculation_type = Column(String(10), nullable=False)  # "flat" or "slab"
    range_min_value = Column(Integer, nullable=True)  # applicable for slab
    range_max_value = Column(Integer, nullable=True)
    amount = Column(Float, nullable=False)  # amount or percent
    meta_json = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    project = relationship("Project", back_populates="commissions")
