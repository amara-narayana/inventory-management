from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from app.core.database import get_db
from app.models.sales import Sale, SaleItem, Payment, Return
from app.models.inventory import Saree, Inventory, StockTransaction
from app.models.purchasing import PurchaseOrder, Supplier
from app.models.finance import Expense, CashTransaction
from sqlalchemy import func, and_

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/dashboard")
def get_dashboard_data(
    db: Session = Depends(get_db)
):
    """Get dashboard statistics."""
    today = date.today()
    
    # Today's sales
    today_sales = db.query(func.sum(Sale.total_amount)).filter(
        func.date(Sale.sale_date) == today
    ).scalar() or Decimal("0")
    
    # Total sales count today
    today_sales_count = db.query(func.count(Sale.id)).filter(
        func.date(Sale.sale_date) == today
    ).scalar() or 0
    
    # Total products
    total_products = db.query(func.count(Saree.id)).scalar() or 0
    
    # Low stock products
    low_stock = db.query(func.count(Saree.id)).filter(
        Saree.current_stock <= Saree.reorder_level
    ).scalar() or 0
    
    # Inventory value
    inventory_value = db.query(
        func.sum(Saree.purchase_price * Saree.current_stock)
    ).scalar() or Decimal("0")
    
    # Recent sales
    recent_sales = db.query(Sale).order_by(Sale.created_at.desc()).limit(5).all()
    
    return {
        "today_sales": today_sales,
        "today_sales_count": today_sales_count,
        "total_products": total_products,
        "low_stock_count": low_stock,
        "inventory_value": inventory_value,
        "recent_sales": recent_sales
    }


@router.get("/sales")
def get_sales_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get sales report."""
    query = db.query(Sale)
    
    if start_date:
        query = query.filter(func.date(Sale.sale_date) >= start_date)
    if end_date:
        query = query.filter(func.date(Sale.sale_date) <= end_date)
    
    sales = query.all()
    
    total_revenue = sum(s.total_amount for s in sales)
    total_paid = sum(s.amount_paid for s in sales)
    
    return {
        "sales": sales,
        "total_revenue": total_revenue,
        "total_paid": total_paid,
        "count": len(sales)
    }


@router.get("/inventory")
def get_inventory_report(db: Session = Depends(get_db)):
    """Get inventory report."""
    sarees = db.query(Saree).all()
    
    total_items = sum(s.current_stock for s in sarees)
    total_value = sum(s.selling_price * s.current_stock for s in sarees)
    low_stock_items = [s for s in sarees if s.current_stock <= s.reorder_level]
    
    return {
        "total_items": total_items,
        "total_value": total_value,
        "low_stock_items": low_stock_items,
        "products": sarees
    }


@router.get("/low-stock")
def get_low_stock_report(db: Session = Depends(get_db)):
    """Get low stock report."""
    low_stock = db.query(Saree).filter(
        Saree.current_stock <= Saree.reorder_level
    ).all()
    
    return {
        "items": low_stock,
        "count": len(low_stock)
    }


@router.get("/profit")
def get_profit_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get profit report."""
    query = db.query(Sale)
    
    if start_date:
        query = query.filter(func.date(Sale.sale_date) >= start_date)
    if end_date:
        query = query.filter(func.date(Sale.sale_date) <= end_date)
    
    sales = query.all()
    
    total_revenue = sum(s.total_amount for s in sales)
    
    # Calculate COGS
    total_cogs = Decimal("0")
    for sale in sales:
        for item in sale.items:
            saree = db.query(Saree).filter(Saree.id == item.saree_id).first()
            if saree:
                total_cogs += saree.purchase_price * item.quantity
    
    gross_profit = total_revenue - total_cogs
    
    return {
        "total_revenue": total_revenue,
        "cost_of_goods": total_cogs,
        "gross_profit": gross_profit,
        "profit_margin": (gross_profit / total_revenue * 100) if total_revenue > 0 else Decimal("0")
    }
