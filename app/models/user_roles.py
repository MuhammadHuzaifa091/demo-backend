"""User roles enum and related models."""

import enum
from typing import Optional

from sqlalchemy import Enum, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base_class import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    USER = "user"
    PROVIDER_INDIVIDUAL = "provider_individual"
    PROVIDER_ORGANIZATION = "provider_organization"
    ADMIN = "admin"


class UserRoleFields:
    """Mixin for role-specific fields."""

    # Common fields for all users
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    # Service Provider specific fields
    service_type: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Organization specific fields
    company_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    team_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
