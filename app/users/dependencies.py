from app.models.users import User
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi import Depends
from app.database.session import get_db


class DebugSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    """Enhanced SQLAlchemyUserDatabase with debugging."""
    
    async def get_by_email(self, email: str):
        """Get user by email with debugging."""
        print(f"🔍 DebugSQLAlchemyUserDatabase.get_by_email called with: {email}")
        
        try:
            result = await super().get_by_email(email)
            if result:
                print(f"❌ Found existing user with email: {email}")
                print(f"❌ Existing user ID: {result.id}")
            else:
                print(f"✅ No existing user found with email: {email}")
            return result
        except Exception as e:
            print(f"❌ Error in get_by_email: {str(e)}")
            raise


async def get_user_db(session=Depends(get_db)):
    yield DebugSQLAlchemyUserDatabase(session, User)
