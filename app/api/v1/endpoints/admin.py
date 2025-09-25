"""Admin endpoints for system management and analytics."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.core.permissions import require_admin_role
from app.database.session import get_db
from app.models.users import User
from app.models.repair_requests import RepairRequest
from app.models.service_providers import ServiceProvider
from app.models.services import Service
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/analytics/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Get dashboard analytics for admin panel."""
    
    # Total counts
    total_users = await session.scalar(
        select(func.count(User.id)).where(User.role == "user")
    )
    total_providers = await session.scalar(
        select(func.count(User.id)).where(
            User.role.in_(["provider_individual", "provider_organization"])
        )
    )
    total_requests = await session.scalar(select(func.count(RepairRequest.id)))
    total_services = await session.scalar(select(func.count(Service.id)))
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    new_users_30d = await session.scalar(
        select(func.count(User.id)).where(
            User.role == "user",
            # Note: We'd need a created_at field on User for this to work properly
        )
    )
    
    new_requests_30d = await session.scalar(
        select(func.count(RepairRequest.id)).where(
            RepairRequest.created_at >= thirty_days_ago
        )
    )
    
    # User role distribution
    user_roles = await session.execute(
        select(User.role, func.count(User.id).label('count'))
        .group_by(User.role)
    )
    role_distribution = {role: count for role, count in user_roles.all()}
    
    # Recent repair requests
    recent_requests = await session.execute(
        select(RepairRequest)
        .options(selectinload(RepairRequest.user))
        .order_by(desc(RepairRequest.created_at))
        .limit(10)
    )
    
    # Service type distribution
    service_types = await session.execute(
        select(Service.service_type, func.count(Service.id).label('count'))
        .group_by(Service.service_type)
    )
    service_distribution = {service_type: count for service_type, count in service_types.all()}
    
    return {
        "totals": {
            "users": total_users or 0,
            "providers": total_providers or 0,
            "repair_requests": total_requests or 0,
            "services": total_services or 0,
        },
        "recent_activity": {
            "new_users_30d": new_users_30d or 0,
            "new_requests_30d": new_requests_30d or 0,
        },
        "distributions": {
            "user_roles": role_distribution,
            "service_types": service_distribution,
        },
        "recent_requests": [
            {
                "id": str(req.id),
                "title": req.title,
                "user_name": f"{req.user.first_name} {req.user.last_name}",
                "created_at": req.created_at.isoformat(),
                "has_voice": bool(req.voice_file),
            }
            for req in recent_requests.scalars().all()
        ],
    }


@router.get("/users", response_model=List[UserRead])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
) -> List[User]:
    """Get all users for admin management."""
    result = await session.execute(
        select(User)
        .offset(skip)
        .limit(limit)
        .order_by(desc(User.email))
    )
    return result.scalars().all()


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    new_role: str,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """Update a user's role."""
    # Validate role
    valid_roles = ["user", "provider_individual", "provider_organization", "admin"]
    if new_role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {valid_roles}"
        )
    
    # Get user
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update role
    user.role = new_role
    await session.commit()
    
    return {"message": f"User role updated to {new_role}"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """Delete a user (admin only)."""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    await session.delete(user)
    await session.commit()
    
    return {"message": "User deleted successfully"}


@router.get("/repair-requests")
async def get_all_repair_requests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
):
    """Get all repair requests for admin management."""
    result = await session.execute(
        select(RepairRequest)
        .options(selectinload(RepairRequest.user))
        .offset(skip)
        .limit(limit)
        .order_by(desc(RepairRequest.created_at))
    )
    return result.scalars().all()


@router.delete("/repair-requests/{request_id}")
async def delete_repair_request(
    request_id: str,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """Delete a repair request (admin only)."""
    result = await session.execute(
        select(RepairRequest).where(RepairRequest.id == request_id)
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repair request not found"
        )
    
    await session.delete(request)
    await session.commit()
    
    return {"message": "Repair request deleted successfully"}


@router.get("/services")
async def get_all_services(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
):
    """Get all services for admin management."""
    result = await session.execute(
        select(Service)
        .options(selectinload(Service.provider))
        .offset(skip)
        .limit(limit)
        .order_by(desc(Service.created_at))
    )
    return result.scalars().all()


@router.delete("/services/{service_id}")
async def delete_service(
    service_id: str,
    current_user: User = Depends(require_admin_role),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """Delete a service (admin only)."""
    result = await session.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    await session.delete(service)
    await session.commit()
    
    return {"message": "Service deleted successfully"}
