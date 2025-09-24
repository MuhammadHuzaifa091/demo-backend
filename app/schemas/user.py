"""User schemas for FastAPI-Users integration."""

import uuid
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel
from app.models.user_roles import UserRole


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole
    service_type: Optional[str] = None
    experience: Optional[str] = None
    contact_info: Optional[str] = None
    company_name: Optional[str] = None
    team_size: Optional[int] = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    role: UserRole = UserRole.USER
    # Service Provider fields
    service_type: Optional[str] = None
    experience: Optional[str] = None
    contact_info: Optional[str] = None
    # Organization fields
    company_name: Optional[str] = None
    team_size: Optional[int] = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str | None = None
    last_name: str | None = None
    role: Optional[UserRole] = None
    service_type: Optional[str] = None
    experience: Optional[str] = None
    contact_info: Optional[str] = None
    company_name: Optional[str] = None
    team_size: Optional[int] = None


class RoleBasedRegistration(BaseModel):
    """Schema for role-based registration with step form data."""
    # Basic info
    email: str
    password: str
    first_name: str
    last_name: str
    role: UserRole
    
    # Service Provider fields (Individual)
    service_type: Optional[str] = None
    experience: Optional[str] = None
    contact_info: Optional[str] = None
    
    # Organization fields
    company_name: Optional[str] = None
    team_size: Optional[int] = None
