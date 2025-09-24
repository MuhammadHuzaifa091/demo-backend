"""ServiceProvider schemas."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ServiceProviderBase(BaseModel):
    """Base ServiceProvider schema."""
    name: str
    service_type: str
    description: str
    contact_info: str


class ServiceProviderCreate(ServiceProviderBase):
    """Schema for creating a service provider."""
    pass


class ServiceProviderUpdate(BaseModel):
    """Schema for updating a service provider."""
    name: Optional[str] = None
    service_type: Optional[str] = None
    description: Optional[str] = None
    contact_info: Optional[str] = None


class ServiceProviderInDBBase(ServiceProviderBase):
    """Base schema for ServiceProvider in database."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID


class ServiceProvider(ServiceProviderInDBBase):
    """Schema for ServiceProvider response."""
    pass


class ServiceProviderInDB(ServiceProviderInDBBase):
    """Schema for ServiceProvider in database."""
    pass
