from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/saree_shop_db"
    
    # Security
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # Application
    app_name: str = "Saree Shop Management"
    debug: bool = True
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # Payment
    payment_test_mode: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
