from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BrandResponse(BrandBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SareeBase(BaseModel):
    sku: str = Field(..., min_length=1)
    barcode: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200)
    brand_id: Optional[str] = None
    category_id: Optional[str] = None
    fabric_id: Optional[str] = None
    color_id: Optional[str] = None
    design_id: Optional[str] = None
    collection_id: Optional[str] = None
    supplier_id: Optional[str] = None
    occasion: Optional[str] = None
    season: Optional[str] = None
    weave: Optional[str] = None
    pattern: Optional[str] = None
    border: Optional[str] = None
    blouse_included: bool = False
    length: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    origin: Optional[str] = None
    handloom: bool = False
    purchase_price: Decimal = Field(..., ge=0)
    selling_price: Decimal = Field(..., ge=0)
    mrp: Optional[Decimal] = None
    discount_percent: Decimal = Field(default=0, ge=0, le=100)
    tax_percent: Decimal = Field(default=0, ge=0, le=100)
    description: Optional[str] = None
    reorder_level: int = Field(default=5, ge=0)
    status: str = "ACTIVE"


class SareeCreate(SareeBase):
    pass


class SareeUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    brand_id: Optional[str] = None
    category_id: Optional[str] = None
    fabric_id: Optional[str] = None
    color_id: Optional[str] = None
    design_id: Optional[str] = None
    collection_id: Optional[str] = None
    supplier_id: Optional[str] = None
    occasion: Optional[str] = None
    season: Optional[str] = None
    weave: Optional[str] = None
    pattern: Optional[str] = None
    border: Optional[str] = None
    blouse_included: Optional[bool] = None
    length: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    origin: Optional[str] = None
    handloom: Optional[bool] = None
    purchase_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None
    mrp: Optional[Decimal] = None
    discount_percent: Optional[Decimal] = None
    tax_percent: Optional[Decimal] = None
    description: Optional[str] = None
    reorder_level: Optional[int] = None
    status: Optional[str] = None


class SareeResponse(SareeBase):
    id: str
    current_stock: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SareeImageBase(BaseModel):
    image_url: str
    is_primary: bool = False
    display_order: int = 0


class SareeImageCreate(SareeImageBase):
    saree_id: str


class SareeImageResponse(SareeImageBase):
    id: str
    saree_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class InventoryResponse(BaseModel):
    id: str
    saree_id: str
    quantity: int
    reserved_quantity: int
    location: str
    last_counted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StockTransactionResponse(BaseModel):
    id: str
    saree_id: str
    transaction_type: str
    quantity: int
    previous_quantity: Optional[int] = None
    new_quantity: Optional[int] = None
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    performed_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockAdjustmentCreate(BaseModel):
    saree_id: str
    adjustment_type: str
    quantity: int
    reason: str
    notes: Optional[str] = None
