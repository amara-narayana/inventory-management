from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models import generate_uuid


class CashRegister(Base):
    __tablename__ = "cash_registers"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CashTransaction(Base):
    __tablename__ = "cash_transactions"

    id = Column(String, primary_key=True, default=generate_uuid)
    register_id = Column(String, ForeignKey("cash_registers.id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(Text)
    reference_type = Column(String)
    reference_id = Column(String)
    performed_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    register = relationship("CashRegister")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=generate_uuid)
    expense_number = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(Text)
    payment_method = Column(String)
    vendor = Column(String)
    notes = Column(Text)
    expense_date = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    resource = Column(String)
    resource_id = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    before_values = Column(Text)
    after_values = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="audit_logs")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, default="INFO")
    is_read = Column(Boolean, default=False)
    recipient_user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class ApplicationSetting(Base):
    __tablename__ = "application_settings"

    id = Column(String, primary_key=True, default=generate_uuid)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BackupRecord(Base):
    __tablename__ = "backup_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    backup_path = Column(String, nullable=False)
    backup_size = Column(Numeric(15, 2))
    status = Column(String, default="COMPLETED")
    notes = Column(Text)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
