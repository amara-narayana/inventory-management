from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models import generate_uuid
from app.core.enums import PaymentMethod, PaymentStatus, ReturnReason, ReturnCondition


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    phone = Column(String, index=True)
    email = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="customer")
    returns = relationship("Return", back_populates="customer")


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    id = Column(String, primary_key=True, default=generate_uuid)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    address_type = Column(String, default="HOME")
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="addresses")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(String, primary_key=True, default=generate_uuid)
    invoice_number = Column(String, unique=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"))
    cashier_id = Column(String, ForeignKey("users.id"))
    
    # Status
    status = Column(String, default="COMPLETED")
    is_held = Column(Boolean, default=False)
    
    # Financials
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    tax_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False, default=0)
    amount_paid = Column(Numeric(12, 2), default=0)
    balance_due = Column(Numeric(12, 2), default=0)
    
    # Notes
    notes = Column(Text)
    
    # Timestamps
    sale_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="sales")
    cashier = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="sale", cascade="all, delete-orphan")
    returns = relationship("Return", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    sale_id = Column(String, ForeignKey("sales.id"), nullable=False)
    saree_id = Column(String, ForeignKey("sarees.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount_percent = Column(Numeric(5, 2), default=0)
    tax_percent = Column(Numeric(5, 2), default=0)
    subtotal = Column(Numeric(12, 2), nullable=False)
    discount_amount = Column(Numeric(12, 2), default=0)
    tax_amount = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sale = relationship("Sale", back_populates="items")
    saree = relationship("Saree", back_populates="sale_items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=generate_uuid)
    sale_id = Column(String, ForeignKey("sales.id"), nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String)
    reference_id = Column(String)
    provider = Column(String)
    notes = Column(Text)
    metadata_ = Column(String)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    sale = relationship("Sale", back_populates="payments")


class Return(Base):
    __tablename__ = "returns"

    id = Column(String, primary_key=True, default=generate_uuid)
    return_number = Column(String, unique=True, nullable=False)
    sale_id = Column(String, ForeignKey("sales.id"), nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"))
    
    # Financials
    total_refund_amount = Column(Numeric(12, 2), default=0)
    refund_status = Column(String, default="PENDING")
    
    # Notes
    reason = Column(SQLEnum(ReturnReason))
    notes = Column(Text)
    
    # Timestamps
    return_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    sale = relationship("Sale", back_populates="returns")
    customer = relationship("Customer", back_populates="returns")
    items = relationship("ReturnItem", back_populates="return_order", cascade="all, delete-orphan")


class ReturnItem(Base):
    __tablename__ = "return_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    return_id = Column(String, ForeignKey("returns.id"), nullable=False)
    sale_item_id = Column(String, ForeignKey("sale_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    condition = Column(SQLEnum(ReturnCondition), nullable=False)
    refund_amount = Column(Numeric(12, 2), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    return_order = relationship("Return", back_populates="items")
