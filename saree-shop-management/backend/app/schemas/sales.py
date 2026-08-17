from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class CustomerResponse(CustomerBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SaleItemBase(BaseModel):
    saree_id: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)
    discount_percent: Decimal = Field(default=0, ge=0, le=100)
    tax_percent: Decimal = Field(default=0, ge=0, le=100)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemResponse(SaleItemBase):
    id: str
    sale_id: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    customer_id: Optional[str] = None
    cashier_id: Optional[str] = None
    status: str = "COMPLETED"
    is_held: bool = False
    notes: Optional[str] = None


class SaleCreate(SaleBase):
    items: List[SaleItemCreate] = []


class SaleUpdate(BaseModel):
    customer_id: Optional[str] = None
    status: Optional[str] = None
    is_held: Optional[bool] = None
    notes: Optional[str] = None


class SaleResponse(SaleBase):
    id: str
    invoice_number: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    balance_due: Decimal
    sale_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    sale_id: str
    payment_method: str
    amount: Decimal = Field(..., gt=0)
    transaction_id: Optional[str] = None
    reference_id: Optional[str] = None
    provider: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: str
    status: str
    metadata_: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReturnItemBase(BaseModel):
    sale_item_id: str
    quantity: int = Field(..., gt=0)
    condition: str
    refund_amount: Decimal = Field(..., ge=0)


class ReturnItemCreate(ReturnItemBase):
    pass


class ReturnItemResponse(ReturnItemBase):
    id: str
    return_id: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReturnBase(BaseModel):
    sale_id: str
    customer_id: Optional[str] = None
    reason: str
    notes: Optional[str] = None


class ReturnCreate(ReturnBase):
    items: List[ReturnItemCreate] = []


class ReturnResponse(ReturnBase):
    id: str
    return_number: str
    total_refund_amount: Decimal
    refund_status: str
    return_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
