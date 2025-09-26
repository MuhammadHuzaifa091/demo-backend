#!/usr/bin/env python3

# Direct database inspection and fix
# Run this: python fix_registration_issue.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, inspect
from app.core.config import settings

async def fix_registration_issue():
    print("🔧 Fixing Registration Issue - Direct Database Analysis\n")
    
    # Create database connection
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("📋 Analyzing database structure...")
        
        # Check if users table exists and its structure
        try:
            result = await session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            table_exists = result.fetchone()
            
            if table_exists:
                print("✅ Users table exists")
                
                # Get table schema
                result = await session.execute(text("PRAGMA table_info(users)"))
                columns = result.fetchall()
                print("📋 Users table columns:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]}) - Nullable: {not col[3]}")
                
                # Check for any constraints
                result = await session.execute(text("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='users'"))
                indexes = result.fetchall()
                if indexes:
                    print("📋 Users table indexes:")
                    for idx in indexes:
                        print(f"  - {idx[0]}")
                
                # Check current data
                result = await session.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"👥 Current user count: {count}")
                
                if count > 0:
                    result = await session.execute(text("SELECT id, email, role FROM users LIMIT 5"))
                    users = result.fetchall()
                    print("📋 Sample users:")
                    for user in users:
                        print(f"  - {user[1]} ({user[2]})")
                
                # Try to find any hidden/cached data
                print("\n🔍 Checking for potential caching issues...")
                
                # Check if there are any transactions in progress
                result = await session.execute(text("BEGIN IMMEDIATE"))
                await session.execute(text("ROLLBACK"))
                print("✅ No blocking transactions found")
                
                # Force a fresh count
                await session.execute(text("VACUUM"))
                result = await session.execute(text("SELECT COUNT(*) FROM users"))
                fresh_count = result.scalar()
                print(f"👥 Fresh user count after VACUUM: {fresh_count}")
                
            else:
                print("❌ Users table does not exist!")
                
        except Exception as e:
            print(f"❌ Database analysis error: {str(e)}")
    
    # Test a simple insert to see what happens
    print("\n🧪 Testing direct user insertion...")
    async with async_session() as session:
        try:
            # Try to insert a test user directly
            test_email = f"directtest{int(asyncio.get_event_loop().time())}@example.com"
            
            insert_sql = text("""
                INSERT INTO users (id, email, hashed_password, is_active, is_superuser, is_verified, first_name, last_name, role)
                VALUES (:id, :email, :password, :active, :superuser, :verified, :first_name, :last_name, 'USER')
            """)
            
            import uuid
            from passlib.context import CryptContext
            
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash("testpassword")
            
            await session.execute(insert_sql, {
                "id": str(uuid.uuid4()),
                "email": test_email,
                "password": hashed_password,
                "active": True,
                "superuser": False,
                "verified": True,
                "first_name": "Direct",
                "last_name": "Test"
            })
            
            await session.commit()
            print(f"✅ Direct insertion successful for: {test_email}")
            
            # Verify it was inserted
            result = await session.execute(text("SELECT email FROM users WHERE email = :email"), {"email": test_email})
            found_user = result.fetchone()
            
            if found_user:
                print(f"✅ User verified in database: {found_user[0]}")
            else:
                print("❌ User not found after insertion!")
                
        except Exception as e:
            print(f"❌ Direct insertion failed: {str(e)}")
            await session.rollback()
    
    await engine.dispose()
    
    print("\n💡 DIAGNOSIS:")
    print("1. If direct insertion works but API fails, the issue is in the API layer")
    print("2. If direct insertion fails, there's a database constraint issue")
    print("3. Check for unique constraints or triggers causing the problem")

if __name__ == "__main__":
    asyncio.run(fix_registration_issue())
