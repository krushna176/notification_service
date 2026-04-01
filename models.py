from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)

    pref_email = Column(Boolean, default=False)
    pref_sms = Column(Boolean, default=False)
    pref_push = Column(Boolean, default=False)
    pushover_user_key = Column(String, nullable=False)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    message = Column(String, nullable=False)
    priority = Column(String, default="medium")

    status = Column(String, default="queued")  # queued, sent, failed
    created_at = Column(DateTime, server_default=func.now())