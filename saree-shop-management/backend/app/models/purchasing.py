from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models import generate_uuid
from app.core.enums import PurchaseOrderStatus, ShipmentStatus


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    gstin = Column(String)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sarees = relationship("Saree", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
    shipments = relationship("Shipment", back_populates="supplier")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(String, primary_key=True, default=generate_uuid)
    order_number = Column(String, unique=True, nullable=False)
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=False)
    status = Column(SQLEnum(PurchaseOrderStatus), default=PurchaseOrderStatus.DRAFT)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery_date = Column(DateTime)
    total_amount = Column(Numeric(12, 2), default=0)
    notes = Column(Text)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseItem", back_populates="purchase_order", cascade="all, delete-orphan")
    receiving = relationship("Receiving", back_populates="purchase_order", uselist=False)
    shipment = relationship("Shipment", back_populates="purchase_order", uselist=False)


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    purchase_order_id = Column(String, ForeignKey("purchase_orders.id"), nullable=False)
    saree_id = Column(String, ForeignKey("sarees.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    received_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    saree = relationship("Saree", back_populates="purchase_items")


class Receiving(Base):
    __tablename__ = "receivings"

    id = Column(String, primary_key=True, default=generate_uuid)
    purchase_order_id = Column(String, ForeignKey("purchase_orders.id"), unique=True, nullable=False)
    receiving_number = Column(String, unique=True, nullable=False)
    received_date = Column(DateTime, default=datetime.utcnow)
    received_by = Column(String, ForeignKey("users.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    purchase_order = relationship("PurchaseOrder", back_populates="receiving")
    items = relationship("ReceivingItem", back_populates="receiving", cascade="all, delete-orphan")


class ReceivingItem(Base):
    __tablename__ = "receiving_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    receiving_id = Column(String, ForeignKey("receivings.id"), nullable=False)
    purchase_item_id = Column(String, ForeignKey("purchase_items.id"), nullable=False)
    quantity_received = Column(Integer, nullable=False)
    condition = Column(String, default="GOOD")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    receiving = relationship("Receiving", back_populates="items")


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(String, primary_key=True, default=generate_uuid)
    purchase_order_id = Column(String, ForeignKey("purchase_orders.id"), unique=True)
    supplier_id = Column(String, ForeignKey("suppliers.id"))
    tracking_number = Column(String)
    carrier = Column(String)
    status = Column(SQLEnum(ShipmentStatus), default=ShipmentStatus.PENDING)
    expected_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    purchase_order = relationship("PurchaseOrder", back_populates="shipment")
    supplier = relationship("Supplier", back_populates="shipments")
