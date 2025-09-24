"""Service endpoints with role-based access control."""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.permissions import require_user_role, require_provider_role
from app.database.session import get_db
from app.models.users import User
from app.models.services import Service
from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
    Service as ServiceSchema,
)

router = APIRouter()


@router.post("/", response_model=ServiceSchema, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_in: ServiceCreate,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> Service:
    """Create a new service (Providers only)."""
    service = Service(
        name=service_in.name,
        service_type=service_in.service_type,
        description=service_in.description,
        contact_info=service_in.contact_info,
        provider_id=current_user.id,
    )
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


@router.get("/", response_model=List[ServiceSchema])
async def get_services(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_user_role),
    session: AsyncSession = Depends(get_db),
) -> List[Service]:
    """Get all services (Users only)."""
    result = await session.execute(
        select(Service)
        .options(selectinload(Service.provider))
        .offset(skip)
        .limit(limit)
        .order_by(Service.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{service_id}", response_model=ServiceSchema)
async def get_service(
    service_id: uuid.UUID,
    current_user: User = Depends(require_user_role),
    session: AsyncSession = Depends(get_db),
) -> Service:
    """Get a single service by ID (Users only)."""
    result = await session.execute(
        select(Service)
        .options(selectinload(Service.provider))
        .where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return service


@router.put("/{service_id}", response_model=ServiceSchema)
async def update_service(
    service_id: uuid.UUID,
    service_update: ServiceUpdate,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> Service:
    """Update a service (Owner only)."""
    result = await session.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    if service.provider_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own services"
        )
    
    # Update fields
    update_data = service_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    await session.commit()
    await session.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: uuid.UUID,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
):
    """Delete a service (Owner only)."""
    result = await session.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    if service.provider_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own services"
        )
    
    await session.delete(service)
    await session.commit()


@router.get("/my/services", response_model=List[ServiceSchema])
async def get_my_services(
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> List[Service]:
    """Get current provider's services."""
    result = await session.execute(
        select(Service)
        .where(Service.provider_id == current_user.id)
        .order_by(Service.created_at.desc())
    )
    return result.scalars().all()
