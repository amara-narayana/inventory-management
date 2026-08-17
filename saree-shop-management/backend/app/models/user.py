"""User model module - re-export from __init__.py for clean imports."""
from app.models import User, Role, Permission, user_roles, role_permissions

__all__ = ["User", "Role", "Permission", "user_roles", "role_permissions"]
