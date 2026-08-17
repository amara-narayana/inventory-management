from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, get_db
from app.api.v1 import auth, inventory, sales, reports
from app.core.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Saree Shop Management System API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}


# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(sales.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Create default admin user if not exists."""
    from app.models.user import User, Role
    from app.core.security import get_password_hash
    from sqlalchemy.orm import Session
    
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # Create admin role
            admin_role = Role(name="ADMIN", description="Administrator")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@sareeshop.com",
                password_hash=get_password_hash("admin123"),
                full_name="Administrator",
                is_active=True
            )
            admin_user.roles.append(admin_role)
            db.add(admin_user)
            db.commit()
            print("Default admin user created: admin / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
