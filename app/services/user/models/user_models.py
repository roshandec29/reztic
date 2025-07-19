from sqlalchemy import (
    Column, String, Boolean, Date, DateTime, Integer, ForeignKey, Text, JSON, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    password_hash = Column(String)
    dob = Column(Date)
    gender = Column(String)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True)
    pan_number = Column(String, unique=True)
    rera_number = Column(String)
    profile_pic_url = Column(Text)
    kyc_status = Column(String, default=False)
    profile_complete_pct = Column(Integer, default=10)
    languages = Column(Text)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    addresses = relationship("UserAddress", back_populates="user")
    roles = relationship("UserRole", back_populates="user")
    devices = relationship("DeviceLogin", back_populates="user")
    preferences = relationship("UserPreference", uselist=False, back_populates="user")
    kyc_docs = relationship("UserKYCDoc", back_populates="user")

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "dob": self.dob.isoformat() if self.dob else None,
            "gender": self.gender,
            "company_id": str(self.company_id) if self.company_id else None,
            "pan_number": self.pan_number,
            "rera_number": self.rera_number,
            "profile_pic_url": self.profile_pic_url,
            "kyc_status": self.kyc_status,
            "profile_complete_pct": self.profile_complete_pct,
            "roles": [
                        {
                            "role_id": role.role_id,
                            "permissions": role.role.permissions if role.role and role.role.permissions else []
                        }
                        for role in self.roles
                    ] if self.roles else [],
            "languages": self.languages,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserAddress(Base):
    __tablename__ = 'user_addresses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    address_type = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    locality_id = Column(UUID(as_uuid=True))
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="addresses")


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    role_id = Column(String, ForeignKey('roles.id'), nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Roles")


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(String, primary_key=True)
    permissions = Column(JSON)


class DeviceLogin(Base):
    __tablename__ = 'device_logins'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    device_type = Column(String)
    ip_address = Column(String)
    login_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="devices")


class UserPreference(Base):
    __tablename__ = 'user_preferences'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    preferences = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="preferences")


class UserKYCDoc(Base):
    __tablename__ = 'user_kyc_docs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    type = Column(String)
    file_url = Column(Text)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="kyc_docs")


class Company(Base):
    __tablename__ = 'companies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, comment="e.g., Square Yards, BetterHomes")
    type = Column(String(50), nullable=False, comment="Agency, Brokerage, Enterprise")
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    logo_url = Column(Text, nullable=True)
    locality_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Company(name={self.name}, type={self.type})>"