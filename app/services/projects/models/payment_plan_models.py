from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.orm import relationship
from app.db.base import Base


class PaymentPlan(Base):
    __tablename__ = 'payment_plans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    plan_name = Column(String(255), nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    breakups = relationship('PaymentPlanBreakup', back_populates='payment_plan', cascade="all, delete-orphan")


class PaymentPlanBreakup(Base):
    __tablename__ = 'payment_plan_breakups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    payment_plan_id = Column(UUID, ForeignKey('payment_plans.id'), nullable=False)
    milestone = Column(String(255), nullable=False)   # e.g., "On Booking", "On Slab Completion"
    percentage = Column(Float, nullable=False)        # Total must sum to 100
    due_days = Column(Integer, nullable=True)         # From booking/previous milestone
    notes = Column(String)

    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    payment_plan = relationship('PaymentPlan', back_populates='breakups')


class AdditionalCharge(Base):
    __tablename__ = 'additional_charges'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    charge_name = Column(String(255), nullable=False)             # e.g., PLC, Clubhouse
    amount_type = Column(String(10), nullable=False)    # fixed / per_sqft / percentage
    amount_value = Column(Float, nullable=False)                  # value according to amount_type
    applicable_on_unit_type = Column(String(100), nullable=True)  # Optional (e.g., 2BHK, 3BHK), if applicable

    is_mandatory = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
