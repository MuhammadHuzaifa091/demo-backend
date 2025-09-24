from typing import TYPE_CHECKING, List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String, Text, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base
from app.models.user_roles import UserRole

if TYPE_CHECKING:
    from app.models.repair_requests import RepairRequest
    from app.models.service_providers import ServiceProvider
    from app.models.services import Service


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # Role-based fields
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), 
        default=UserRole.USER, 
        nullable=False
    )
    
    # Service Provider specific fields
    service_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Organization specific fields
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    team_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    repair_requests: Mapped[List["RepairRequest"]] = relationship(
        "RepairRequest", back_populates="user", cascade="all, delete-orphan"
    )
    service_providers: Mapped[List["ServiceProvider"]] = relationship(
        "ServiceProvider", back_populates="user", cascade="all, delete-orphan"
    )
    services: Mapped[List["Service"]] = relationship(
        "Service", back_populates="provider", cascade="all, delete-orphan"
    )
