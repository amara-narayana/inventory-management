from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models import generate_uuid


class Saree(Base):
    __tablename__ = "sarees"

    id = Column(String, primary_key=True, default=generate_uuid)
    sku = Column(String, unique=True, index=True, nullable=False)
    barcode = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    
    # Foreign keys
    brand_id = Column(String, ForeignKey("brands.id"))
    category_id = Column(String, ForeignKey("categories.id"))
    fabric_id = Column(String, ForeignKey("fabrics.id"))
    color_id = Column(String, ForeignKey("colors.id"))
    design_id = Column(String, ForeignKey("designs.id"))
    collection_id = Column(String, ForeignKey("collections.id"))
    supplier_id = Column(String, ForeignKey("suppliers.id"))
    
    # Attributes
    occasion = Column(String)
    season = Column(String)
    weave = Column(String)
    pattern = Column(String)
    border = Column(String)
    blouse_included = Column(Boolean, default=False)
    length = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    origin = Column(String)
    handloom = Column(Boolean, default=False)
    
    # Pricing
    purchase_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    mrp = Column(Numeric(10, 2))
    discount_percent = Column(Numeric(5, 2), default=0)
    tax_percent = Column(Numeric(5, 2), default=0)
    
    # Inventory
    description = Column(Text)
    reorder_level = Column(Integer, default=5)
    current_stock = Column(Integer, default=0)
    status = Column(String, default="ACTIVE")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    brand = relationship("Brand", back_populates="sarees")
    category = relationship("Category", back_populates="sarees")
    fabric = relationship("Fabric", back_populates="sarees")
    color = relationship("Color", back_populates="sarees")
    design = relationship("Design", back_populates="sarees")
    collection = relationship("Collection", back_populates="sarees")
    supplier = relationship("Supplier", back_populates="sarees")
    images = relationship("SareeImage", back_populates="saree", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="saree", uselist=False)
    sale_items = relationship("SaleItem", back_populates="saree")
    purchase_items = relationship("PurchaseItem", back_populates="saree")
    stock_transactions = relationship("StockTransaction", back_populates="saree")


class SareeImage(Base):
    __tablename__ = "saree_images"

    id = Column(String, primary_key=True, default=generate_uuid)
    saree_id = Column(String, ForeignKey("sarees.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    saree = relationship("Saree", back_populates="images")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, default=generate_uuid)
    saree_id = Column(String, ForeignKey("sarees.id"), unique=True, nullable=False)
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    location = Column(String, default="MAIN")
    last_counted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    saree = relationship("Saree", back_populates="inventory")


class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(String, primary_key=True, default=generate_uuid)
    saree_id = Column(String, ForeignKey("sarees.id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    previous_quantity = Column(Integer)
    new_quantity = Column(Integer)
    reference_type = Column(String)
    reference_id = Column(String)
    notes = Column(Text)
    performed_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    saree = relationship("Saree", back_populates="stock_transactions")


class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    id = Column(String, primary_key=True, default=generate_uuid)
    saree_id = Column(String, ForeignKey("sarees.id"), nullable=False)
    adjustment_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    notes = Column(Text)
    performed_by = Column(String, ForeignKey("users.id"))
    approved_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
