#!/usr/bin/env python3
"""Reset database with admin role support."""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from app.database.base import Base
from app.database.session import engine
from app.models.users import User
from app.models.user_roles import UserRole


async def reset_database():
    """Reset the database and recreate all tables."""
    print("🔄 Resetting database...")
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ Dropped all tables")
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Created all tables")
    
    print("✅ Database reset complete!")
    print(f"📋 Available roles: {[role.value for role in UserRole]}")


if __name__ == "__main__":
    asyncio.run(reset_database())
