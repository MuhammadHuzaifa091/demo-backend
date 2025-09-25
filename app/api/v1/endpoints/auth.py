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


@router.post("/debug-registration")
async def debug_registration(user_data: RoleBasedRegistration):
    """Debug endpoint to test registration data validation."""
    return {
        "received_role": user_data.role,
        "role_type": type(user_data.role).__name__,
        "role_value": user_data.role.value if hasattr(user_data.role, 'value') else str(user_data.role),
        "all_roles": [role.value for role in UserRole],
        "message": "Registration data received successfully"
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
        error_str = str(e).lower()
        if "email" in error_str and ("already" in error_str or "exists" in error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        elif "password" in error_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password validation failed"
            )
        elif "role" in error_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role specified"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration failed: {str(e)}"
            )
