#!/usr/bin/env python3
"""Initialize database with proper async support."""

import asyncio
import os
from pathlib import Path

async def init_database():
    """Initialize the database with proper admin role support."""
    print("🔄 Initializing database with admin role support...")
    
    # Remove existing database
    db_path = Path("database.db")
    if db_path.exists():
        os.remove(db_path)
        print("✅ Removed existing database")
    
    try:
        # Import after removing old database
        from app.database.session import async_engine
        from app.database.base import Base
        from app.models.user_roles import UserRole
        
        # Create all tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Created all tables with admin role support")
        
        # Verify roles
        print(f"📋 Available roles: {[role.value for role in UserRole]}")
        print("🎉 Database initialization completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(init_database())
    if success:
        print("\n🚀 Database is ready!")
        print("💡 Now restart your FastAPI server:")
        print("   python -m uvicorn app.main:app --reload")
        print("\n🎯 You can now register admin users!")
    else:
        print("\n❌ Database initialization failed!")
