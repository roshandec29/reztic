from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class SMSLog(Base):
    __tablename__ = 'sms_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    phone_number = Column(String)
    message = Column(Text)
    message_type = Column(String, comment='OTP, Notification, etc.')
    status = Column(String, comment='sent, failed, delivered')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
