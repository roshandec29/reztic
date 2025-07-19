from sqlalchemy import Column, String, Text, Date, DECIMAL, JSON, ForeignKey, Integer, Boolean, DateTime, ARRAY
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
    status = Column(String, nullable=False)  # "launched", "under_construction"
    is_featured = Column(Boolean, default=False)  # for highlighting on homepage
    badges = Column(ARRAY(String), default=[])  # ["New Project", "5% Commission"]
    possession_date = Column(Date)
    project_type = Column(String)
    rera_number = Column(String)
    starting_price = Column(DECIMAL)
    price_range = Column(JSON)
    commission_structure = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    units = relationship("ProjectUnit", backref="project", cascade="all, delete-orphan")
    media = relationship("ProjectMedia", backref="project", cascade="all, delete-orphan")
    locality = relationship("Locality", backref="project")


class ProjectUnit(Base):
    __tablename__ = "project_units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    unit_type = Column(String, nullable=False)  # "2 BHK", "Studio"
    size_sqft = Column(Integer)
    total_units = Column(Integer)
    available_units = Column(Integer)
    price = Column(DECIMAL)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProjectMedia(Base):
    __tablename__ = "project_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    type = Column(String, nullable=False)  # image, video, pdf
    is_featured = Column(Boolean, default=False)
    media_url = Column(Text, nullable=False)
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