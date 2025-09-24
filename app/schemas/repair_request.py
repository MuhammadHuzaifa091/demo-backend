"""RepairRequest schemas."""

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.schemas.user import UserRead


class RepairRequestBase(BaseModel):
    """Base RepairRequest schema."""
    title: str
    description: str


class RepairRequestCreate(BaseModel):
    """Schema for creating a repair request."""
    title: str
    description: Optional[str] = None
    voice_file: Optional[str] = None


class RepairRequestUpdate(BaseModel):
    """Schema for updating a repair request."""
    title: Optional[str] = None
    description: Optional[str] = None
    voice_file: Optional[str] = None


class RepairRequestInDBBase(RepairRequestBase):
    """Base schema for RepairRequest in database."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID


class RepairRequest(RepairRequestInDBBase):
    """RepairRequest schema for API responses."""
    title: str
    description: Optional[str] = None
    voice_file: Optional[str] = None
    user: Optional["UserRead"] = None


class RepairRequestInDB(RepairRequestInDBBase):
    """Schema for RepairRequest in database."""
    pass
