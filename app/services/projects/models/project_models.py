from sqlalchemy import Column, String, Text, Date, DECIMAL, JSON, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    developer_id = Column(UUID(as_uuid=True), ForeignKey("developers.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    status = Column(String, nullable=False)  # "launched", "under_construction"
    possession_date = Column(Date)
    project_type = Column(String)
    rera_number = Column(String)
    starting_price = Column(DECIMAL)
    price_range = Column(JSON)
    commission_structure = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProjectUnit(Base):
    __tablename__ = "project_units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    locality_id = Column(UUID(as_uuid=True), ForeignKey("localities.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    unit_type = Column(String, nullable=False)  # "2 BHK", "Studio"
    size_sqft = Column(Integer)
    total_units = Column(Integer)
    available_units = Column(Integer)
    price = Column(DECIMAL)


class ProjectMedia(Base):
    __tablename__ = "project_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    type = Column(String, nullable=False)  # image, video, pdf
    media_url = Column(Text, nullable=False)
    meta_json = Column(JSON)


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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
