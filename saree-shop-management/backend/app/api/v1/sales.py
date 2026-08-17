from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.schemas.sales import (
    CustomerCreate, CustomerResponse, CustomerUpdate,
    SaleCreate, SaleResponse, SaleUpdate,
    PaymentCreate, PaymentResponse,
    ReturnCreate, ReturnResponse
)
from app.models.sales import Customer, Sale, SaleItem, Payment, Return, ReturnItem
from app.models.inventory import Saree, Inventory, StockTransaction
from decimal import Decimal

router = APIRouter(prefix="/sales", tags=["Sales"])


def generate_invoice_number(db: Session) -> str:
    """Generate unique invoice number."""
    today = datetime.now().strftime("%Y%m%d")
    last_sale = db.query(Sale).filter(
        Sale.invoice_number.like(f"INV-{today}-%")
    ).order_by(Sale.created_at.desc()).first()
    
    if last_sale:
        last_num = int(last_sale.invoice_number.split("-")[-1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f"INV-{today}-{new_num:06d}"


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db)):
    """Create a new sale (POS transaction)."""
    # Generate invoice number
    invoice_number = generate_invoice_number(db)
    
    # Calculate totals
    subtotal = Decimal("0")
    discount_amount = Decimal("0")
    tax_amount = Decimal("0")
    total_amount = Decimal("0")
    
    # Process items
    db_items = []
    for item_data in sale_data.items:
        saree = db.query(Saree).filter(Saree.id == item_data.saree_id).first()
        if not saree:
            raise HTTPException(status_code=404, detail=f"Saree {item_data.saree_id} not found")
        
        # Check stock
        inventory = db.query(Inventory).filter(Inventory.saree_id == item_data.saree_id).first()
        if not inventory or inventory.quantity < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {saree.name}")
        
        # Calculate item totals
        item_subtotal = item_data.unit_price * item_data.quantity
        item_discount = item_subtotal * (item_data.discount_percent / Decimal("100"))
        item_tax = (item_subtotal - item_discount) * (item_data.tax_percent / Decimal("100"))
        item_total = item_subtotal - item_discount + item_tax
        
        # Create sale item
        db_item = SaleItem(
            saree_id=item_data.saree_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            discount_percent=item_data.discount_percent,
            tax_percent=item_data.tax_percent,
            subtotal=item_subtotal,
            discount_amount=item_discount,
            tax_amount=item_tax,
            total=item_total
        )
        db_items.append(db_item)
        
        # Update totals
        subtotal += item_subtotal
        discount_amount += item_discount
        tax_amount += item_tax
        total_amount += item_total
        
        # Update inventory
        inventory.quantity -= item_data.quantity
        saree.current_stock = inventory.quantity
        
        # Create stock transaction
        stock_txn = StockTransaction(
            saree_id=item_data.saree_id,
            transaction_type="SALE",
            quantity=-item_data.quantity,
            previous_quantity=inventory.quantity + item_data.quantity,
            new_quantity=inventory.quantity,
            reference_type="SALE",
            notes=f"Sale {invoice_number}"
        )
        db.add(stock_txn)
    
    # Create sale
    db_sale = Sale(
        invoice_number=invoice_number,
        customer_id=sale_data.customer_id,
        cashier_id=sale_data.cashier_id,
        status=sale_data.status,
        is_held=sale_data.is_held,
        notes=sale_data.notes,
        subtotal=subtotal,
        discount_amount=discount_amount,
        tax_amount=tax_amount,
        total_amount=total_amount,
        amount_paid=Decimal("0"),
        balance_due=total_amount
    )
    
    db_sale.items = db_items
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    return db_sale


@router.get("/", response_model=List[SaleResponse])
def list_sales(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all sales."""
    return db.query(Sale).order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: str, db: Session = Depends(get_db)):
    """Get a specific sale."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.post("/{sale_id}/payment", response_model=PaymentResponse)
def add_payment(sale_id: str, payment_data: PaymentCreate, db: Session = Depends(get_db)):
    """Add payment to a sale."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Create payment
    db_payment = Payment(
        sale_id=sale_id,
        payment_method=payment_data.payment_method,
        amount=payment_data.amount,
        transaction_id=payment_data.transaction_id,
        reference_id=payment_data.reference_id,
        provider=payment_data.provider,
        notes=payment_data.notes,
        status="PAID",
        paid_at=datetime.utcnow()
    )
    
    # Update sale
    sale.amount_paid += payment_data.amount
    sale.balance_due = sale.total_amount - sale.amount_paid
    
    if sale.balance_due <= 0:
        sale.status = "COMPLETED"
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    return db_payment


# Customer endpoints
@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer."""
    db_customer = Customer(**customer_data.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/customers", response_model=List[CustomerResponse])
def list_customers(db: Session = Depends(get_db)):
    """List all customers."""
    return db.query(Customer).filter(Customer.is_active == True).all()


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get a specific customer."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
