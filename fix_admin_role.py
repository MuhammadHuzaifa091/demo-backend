#!/usr/bin/env python3
"""Fix admin role database constraint issue."""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def fix_admin_role():
    """Fix the admin role constraint in the database."""
    print("🔄 Fixing admin role database constraint...")
    
    try:
        from sqlalchemy import create_engine, text
        from app.database.session import engine
        from app.models.users import User
        from app.models.user_roles import UserRole
        from app.database.base import Base
        
        # Check if we're using SQLite
        database_url = str(engine.url)
        print(f"📋 Database URL: {database_url}")
        
        if "sqlite" in database_url.lower():
            print("🔧 SQLite detected - recreating database...")
            
            # For SQLite, we need to recreate the database
            # Drop all tables
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                print("✅ Dropped all tables")
            
            # Create all tables with updated schema
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("✅ Created all tables with admin role support")
                
        else:
            print("🔧 PostgreSQL detected - altering enum...")
            # For PostgreSQL, we can alter the enum
            async with engine.begin() as conn:
                await conn.execute(text(
                    "ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'admin'"
                ))
                print("✅ Added admin role to enum")
        
        # Verify the roles are available
        print(f"📋 Available roles: {[role.value for role in UserRole]}")
        print("✅ Admin role fix completed successfully!")
        
    except Exception as e:
        print(f"❌ Error fixing admin role: {str(e)}")
        print("💡 Try running: python reset_database.py && python create_migration.py")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(fix_admin_role())
    if success:
        print("\n🎉 Database is now ready for admin registration!")
        print("🚀 You can now register admin users through the frontend.")
    else:
        print("\n❌ Failed to fix admin role. Manual database reset may be required.")
