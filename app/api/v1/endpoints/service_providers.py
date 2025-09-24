"""ServiceProvider endpoints with role-based access control."""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.permissions import require_provider_role, require_user_role, require_any_authenticated_user
from app.database.session import get_db
from app.models.users import User
from app.models.service_providers import ServiceProvider
from app.schemas.service_provider import (
    ServiceProviderCreate,
    ServiceProviderUpdate,
    ServiceProvider as ServiceProviderSchema,
)

router = APIRouter()


@router.post("/", response_model=ServiceProviderSchema, status_code=status.HTTP_201_CREATED)
async def create_service_provider(
    service_provider_in: ServiceProviderCreate,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> ServiceProvider:
    """Create a new service provider (Providers only)."""
    service_provider = ServiceProvider(
        name=service_provider_in.name,
        service_type=service_provider_in.service_type,
        description=service_provider_in.description,
        contact_info=service_provider_in.contact_info,
        user_id=current_user.id,
    )
    session.add(service_provider)
    await session.commit()
    await session.refresh(service_provider)
    return service_provider


@router.get("/", response_model=List[ServiceProviderSchema])
async def get_service_providers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_user_role),
    session: AsyncSession = Depends(get_db),
) -> List[ServiceProvider]:
    """Get all service providers (Users only - for browsing)."""
    result = await session.execute(
        select(ServiceProvider)
        .options(selectinload(ServiceProvider.user))
        .offset(skip)
        .limit(limit)
        .order_by(ServiceProvider.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{service_provider_id}", response_model=ServiceProviderSchema)
async def get_service_provider(
    service_provider_id: uuid.UUID,
    current_user: User = Depends(require_any_authenticated_user),
    session: AsyncSession = Depends(get_db),
) -> ServiceProvider:
    """Get a single service provider by ID (Any authenticated user)."""
    result = await session.execute(
        select(ServiceProvider)
        .options(selectinload(ServiceProvider.user))
        .where(ServiceProvider.id == service_provider_id)
    )
    service_provider = result.scalar_one_or_none()

    if not service_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider not found"
        )

    return service_provider


@router.put("/{service_provider_id}", response_model=ServiceProviderSchema)
async def update_service_provider(
    service_provider_id: uuid.UUID,
    service_provider_update: ServiceProviderUpdate,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> ServiceProvider:
    """Update a service provider (Providers only - owner can update)."""
    result = await session.execute(
        select(ServiceProvider).where(
            ServiceProvider.id == service_provider_id)
    )
    service_provider = result.scalar_one_or_none()

    if not service_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider not found"
        )

    if service_provider.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this service provider"
        )

    update_data = service_provider_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service_provider, field, value)

    await session.commit()
    await session.refresh(service_provider)
    return service_provider


@router.delete("/{service_provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_provider(
    service_provider_id: uuid.UUID,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> None:
    """Delete a service provider (Providers only - owner can delete)."""
    result = await session.execute(
        select(ServiceProvider).where(
            ServiceProvider.id == service_provider_id)
    )
    service_provider = result.scalar_one_or_none()

    if not service_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider not found"
        )

    if service_provider.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this service provider"
        )

    await session.delete(service_provider)
    await session.commit()


@router.get("/my/providers", response_model=List[ServiceProviderSchema])
async def get_my_service_providers(
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> List[ServiceProvider]:
    """Get current provider's service provider listings."""
    result = await session.execute(
        select(ServiceProvider)
        .where(ServiceProvider.user_id == current_user.id)
        .order_by(ServiceProvider.created_at.desc())
    )
    return result.scalars().all()
