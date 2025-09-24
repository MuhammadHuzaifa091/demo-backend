"""Service schemas for API."""

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.schemas.user import UserRead


class ServiceBase(BaseModel):
    """Base Service schema."""
    name: str
    service_type: str
    description: str
    contact_info: str


class ServiceCreate(ServiceBase):
    """Schema for creating a service."""
    pass


class ServiceUpdate(BaseModel):
    """Schema for updating a service."""
    name: Optional[str] = None
    service_type: Optional[str] = None
    description: Optional[str] = None
    contact_info: Optional[str] = None


class ServiceInDBBase(ServiceBase):
    """Base schema for Service in database."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    provider_id: uuid.UUID


class Service(ServiceInDBBase):
    """Service schema for API responses."""
    provider: Optional["UserRead"] = None


class ServiceInDB(ServiceInDBBase):
    """Schema for Service in database."""
    pass
