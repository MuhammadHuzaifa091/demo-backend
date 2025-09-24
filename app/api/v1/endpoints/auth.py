"""Custom authentication endpoints with role support."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users import get_user_manager
from app.database.session import get_db
from app.models.users import User
from app.schemas.user import RoleBasedRegistration, UserRead, UserCreate
from app.users.manager import UserManager

router = APIRouter()


@router.get("/test-roles")
async def test_roles():
    """Test endpoint to check if roles are working."""
    from app.models.user_roles import UserRole
    return {
        "roles": [role.value for role in UserRole],
        "message": "Role system is working"
    }


@router.post("/register-with-role", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_with_role(
    user_data: RoleBasedRegistration,
    session: AsyncSession = Depends(get_db),
    user_manager: UserManager = Depends(get_user_manager),
):
    """Register a new user with role-specific fields."""
    try:
        # Convert to UserCreate schema
        user_create = UserCreate(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
            service_type=user_data.service_type,
            experience=user_data.experience,
            contact_info=user_data.contact_info,
            company_name=user_data.company_name,
            team_size=user_data.team_size,
        )
        
        # Create user with role-specific data
        user = await user_manager.create(user_create)
        return UserRead.model_validate(user)
    
    except Exception as e:
        print(f"Registration error: {str(e)}")  # Debug logging
        if "email" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )
