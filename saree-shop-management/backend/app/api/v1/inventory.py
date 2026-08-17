from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.inventory import (
    SareeCreate, SareeResponse, SareeUpdate,
    BrandCreate, BrandResponse, BrandUpdate,
    CategoryCreate, CategoryResponse, CategoryUpdate,
    StockAdjustmentCreate, StockTransactionResponse
)
from app.models.inventory import Saree, Brand, Category, Inventory, StockTransaction
from app.core.security import get_password_hash
from datetime import datetime
import uuid

router = APIRouter(prefix="/sarees", tags=["Sarees"])


def generate_sku() -> str:
    """Generate unique SKU for saree."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = uuid.uuid4().hex[:6].upper()
    return f"SAR-{timestamp}-{random_part}"


@router.post("/", response_model=SareeResponse, status_code=status.HTTP_201_CREATED)
def create_saree(saree_data: SareeCreate, db: Session = Depends(get_db)):
    """Create a new saree product."""
    # Generate SKU if not provided
    if not saree_data.sku:
        saree_data.sku = generate_sku()
    
    # Check if SKU already exists
    existing = db.query(Saree).filter(Saree.sku == saree_data.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    # Create saree
    db_saree = Saree(**saree_data.model_dump())
    db.add(db_saree)
    
    # Create inventory record
    db_inventory = Inventory(
        saree_id=db_saree.id,
        quantity=0,
        reserved_quantity=0
    )
    db.add(db_inventory)
    
    db.commit()
    db.refresh(db_saree)
    
    return db_saree


@router.get("/", response_model=List[SareeResponse])
def list_sarees(
    skip: int = 0,
    limit: int = 50,
    search: str = None,
    brand_id: str = None,
    category_id: str = None,
    db: Session = Depends(get_db)
):
    """List all sarees with optional filtering."""
    query = db.query(Saree)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Saree.name.ilike(search_filter)) |
            (Saree.sku.ilike(search_filter)) |
            (Saree.barcode.ilike(search_filter))
        )
    
    if brand_id:
        query = query.filter(Saree.brand_id == brand_id)
    
    if category_id:
        query = query.filter(Saree.category_id == category_id)
    
    sarees = query.offset(skip).limit(limit).all()
    return sarees


@router.get("/{saree_id}", response_model=SareeResponse)
def get_saree(saree_id: str, db: Session = Depends(get_db)):
    """Get a specific saree by ID."""
    saree = db.query(Saree).filter(Saree.id == saree_id).first()
    if not saree:
        raise HTTPException(status_code=404, detail="Saree not found")
    return saree


@router.get("/barcode/{barcode}", response_model=SareeResponse)
def get_saree_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """Get saree by barcode (for POS scanning)."""
    saree = db.query(Saree).filter(Saree.barcode == barcode).first()
    if not saree:
        raise HTTPException(status_code=404, detail="Saree not found")
    return saree


@router.put("/{saree_id}", response_model=SareeResponse)
def update_saree(saree_id: str, saree_data: SareeUpdate, db: Session = Depends(get_db)):
    """Update a saree."""
    saree = db.query(Saree).filter(Saree.id == saree_id).first()
    if not saree:
        raise HTTPException(status_code=404, detail="Saree not found")
    
    update_data = saree_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(saree, key, value)
    
    db.commit()
    db.refresh(saree)
    return saree


@router.delete("/{saree_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saree(saree_id: str, db: Session = Depends(get_db)):
    """Delete a saree."""
    saree = db.query(Saree).filter(Saree.id == saree_id).first()
    if not saree:
        raise HTTPException(status_code=404, detail="Saree not found")
    
    db.delete(saree)
    db.commit()
    return None


# Brand endpoints
@router.post("/brands", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
def create_brand(brand_data: BrandCreate, db: Session = Depends(get_db)):
    """Create a new brand."""
    db_brand = Brand(**brand_data.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.get("/brands", response_model=List[BrandResponse])
def list_brands(db: Session = Depends(get_db)):
    """List all brands."""
    return db.query(Brand).filter(Brand.is_active == True).all()


# Category endpoints
@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """List all categories."""
    return db.query(Category).filter(Category.is_active == True).all()
