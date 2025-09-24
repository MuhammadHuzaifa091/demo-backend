"""Role-based permission guards for endpoints."""

from typing import List
from fastapi import Depends, HTTPException, status
from app.core.users import current_active_user
from app.models.users import User
from app.models.user_roles import UserRole


def require_roles(allowed_roles: List[UserRole]):
    """
    Dependency factory that creates a role-based guard.
    
    Args:
        allowed_roles: List of roles that are allowed to access the endpoint
    
    Returns:
        Dependency function that checks user role
    """
    def role_guard(current_user: User = Depends(current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    
    return role_guard


# Specific role guards for common use cases
def require_user_role(current_user: User = Depends(current_active_user)) -> User:
    """Guard that only allows users with 'user' role."""
    if current_user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only users can access this endpoint."
        )
    return current_user


def require_provider_role(current_user: User = Depends(current_active_user)) -> User:
    """Guard that only allows users with provider roles."""
    if current_user.role not in [UserRole.PROVIDER_INDIVIDUAL, UserRole.PROVIDER_ORGANIZATION]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only service providers can access this endpoint."
        )
    return current_user


def require_any_authenticated_user(current_user: User = Depends(current_active_user)) -> User:
    """Guard that allows any authenticated user (for general endpoints)."""
    return current_user
