from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.exceptions import UserAlreadyExists
from app.models.users import User
from app.core.config import settings
from app.users.dependencies import get_user_db
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

SECRET = settings.SECRET_KEY


class UserManager(UUIDIDMixin, BaseUserManager[User, str]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request = None,
    ) -> User:
        """Create user with enhanced error handling and debugging."""
        print(f"🔍 UserManager.create called with email: {user_create.email}")
        
        try:
            # Check if user already exists
            existing_user = await self.user_db.get_by_email(user_create.email)
            if existing_user:
                print(f"❌ User already exists with email: {user_create.email}")
                raise UserAlreadyExists()
            
            print(f"✅ No existing user found, proceeding with creation")
            
            # Call parent create method
            user = await super().create(user_create, safe, request)
            print(f"✅ User created successfully: {user.email}")
            return user
            
        except UserAlreadyExists:
            print(f"❌ UserAlreadyExists exception for: {user_create.email}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error in UserManager.create: {str(e)}")
            print(f"❌ Error type: {type(e).__name__}")
            raise


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
