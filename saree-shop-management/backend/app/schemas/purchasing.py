from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    gstin: Optional[str] = None
    notes: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    gstin: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierResponse(SupplierBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PurchaseOrderBase(BaseModel):
    supplier_id: str
    status: str = "DRAFT"
    expected_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    items: List["PurchaseItemCreate"] = []


class PurchaseOrderUpdate(BaseModel):
    supplier_id: Optional[str] = None
    status: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: str
    order_number: str
    order_date: datetime
    total_amount: Decimal
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PurchaseItemBase(BaseModel):
    saree_id: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)


class PurchaseItemCreate(PurchaseItemBase):
    pass


class PurchaseItemResponse(PurchaseItemBase):
    id: str
    purchase_order_id: str
    total_price: Decimal
    received_quantity: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReceivingBase(BaseModel):
    purchase_order_id: str
    notes: Optional[str] = None


class ReceivingCreate(ReceivingBase):
    items: List["ReceivingItemCreate"] = []


class ReceivingResponse(ReceivingBase):
    id: str
    receiving_number: str
    received_date: datetime
    received_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReceivingItemBase(BaseModel):
    purchase_item_id: str
    quantity_received: int = Field(..., gt=0)
    condition: str = "GOOD"
    notes: Optional[str] = None


class ReceivingItemCreate(ReceivingItemBase):
    pass


class ReceivingItemResponse(ReceivingItemBase):
    id: str
    receiving_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ShipmentBase(BaseModel):
    purchase_order_id: Optional[str] = None
    supplier_id: Optional[str] = None
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    status: str = "PENDING"
    expected_delivery: Optional[datetime] = None
    notes: Optional[str] = None


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    status: Optional[str] = None
    expected_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    notes: Optional[str] = None


class ShipmentResponse(ShipmentBase):
    id: str
    actual_delivery: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
