"""Seed script to create initial admin user and roles."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import User, Role, Permission, user_roles, Base
from app.security.password_hashing import hash_password

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

def seed_roles_and_permissions(db: Session):
    """Create default roles and permissions."""
    # Create permissions
    permissions_data = [
        {"name": "view_dashboard", "resource": "dashboard", "action": "view"},
        {"name": "manage_products", "resource": "products", "action": "manage"},
        {"name": "manage_inventory", "resource": "inventory", "action": "manage"},
        {"name": "manage_sales", "resource": "sales", "action": "manage"},
        {"name": "manage_purchases", "resource": "purchases", "action": "manage"},
        {"name": "manage_customers", "resource": "customers", "action": "manage"},
        {"name": "manage_suppliers", "resource": "suppliers", "action": "manage"},
        {"name": "manage_reports", "resource": "reports", "action": "manage"},
        {"name": "manage_users", "resource": "users", "action": "manage"},
        {"name": "manage_settings", "resource": "settings", "action": "manage"},
        {"name": "manage_pos", "resource": "pos", "action": "manage"},
        {"name": "manage_returns", "resource": "returns", "action": "manage"},
    ]
    
    permissions = {}
    for perm_data in permissions_data:
        perm = db.query(Permission).filter_by(name=perm_data["name"]).first()
        if not perm:
            perm = Permission(**perm_data)
            db.add(perm)
            db.flush()
        permissions[perm_data["name"]] = perm
    
    print(f"✓ Created {len(permissions)} permissions")
    
    # Create roles
    roles_data = {
        "ADMIN": {
            "description": "Full system access",
            "permission_names": list(permissions.keys())
        },
        "MANAGER": {
            "description": "Operations and reports access",
            "permission_names": ["view_dashboard", "manage_products", "manage_inventory", 
                                "manage_sales", "manage_purchases", "manage_customers",
                                "manage_suppliers", "manage_reports", "manage_returns", "manage_pos"]
        },
        "STAFF": {
            "description": "POS and basic operations",
            "permission_names": ["view_dashboard", "manage_pos", "manage_sales", 
                                "manage_customers", "manage_returns"]
        }
    }
    
    roles = {}
    for role_name, role_data in roles_data.items():
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, description=role_data["description"])
            db.add(role)
            db.flush()
            
            # Assign permissions
            for perm_name in role_data["permission_names"]:
                if perm_name in permissions:
                    role.permissions.append(permissions[perm_name])
        roles[role_name] = role
    
    print(f"✓ Created {len(roles)} roles")
    db.commit()
    return roles

def seed_admin_user(db: Session, roles: dict):
    """Create default admin user."""
    admin = db.query(User).filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@sareeshop.com",
            password_hash=hash_password("admin123"),
            full_name="System Administrator",
            is_active=True
        )
        db.add(admin)
        db.flush()
        
        # Assign ADMIN role
        admin.roles.append(roles["ADMIN"])
        db.commit()
        print("✓ Created admin user (username: admin, password: admin123)")
    else:
        print("ℹ Admin user already exists")

def main():
    """Run seed script."""
    print("Starting database seeding...")
    
    # Create tables first
    create_tables()
    
    # Get DB session
    db = SessionLocal()
    try:
        # Seed roles and permissions
        roles = seed_roles_and_permissions(db)
        
        # Seed admin user
        seed_admin_user(db, roles)
        
        print("\n✓ Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"✗ Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
