#!/usr/bin/env python3

# Test registration issue with direct database check
# Run this: python test_registration_direct.py

import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings

async def test_registration_direct():
    print("🔍 Testing Registration Issue with Direct Database Check\n")
    
    # Create database connection
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Check current database state
    print("📋 Checking current database state...")
    async with async_session() as session:
        # Check users table
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"👥 Users in database: {user_count}")
        
        if user_count > 0:
            # Get all users
            result = await session.execute(text("SELECT id, email, role FROM users"))
            users = result.fetchall()
            print("📋 Existing users:")
            for user in users:
                print(f"  - ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")
    
    # Test API registration
    print(f"\n🧪 Testing API registration...")
    
    unique_email = f"testuser{int(asyncio.get_event_loop().time())}@example.com"
    print(f"📧 Using email: {unique_email}")
    
    registration_data = {
        "email": unique_email,
        "password": "admin123",
        "first_name": "Test",
        "last_name": "User",
        "role": "admin"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://demo.publicvm.com/api/v1/auth/register-with-role",
                json=registration_data,
                timeout=15.0
            )
            
            if response.status_code == 201:
                print("✅ Registration successful!")
                print("Response:", response.json())
            else:
                print(f"❌ Registration failed with status: {response.status_code}")
                print("Error:", response.text)
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
    
    # Check database again after registration attempt
    print(f"\n📋 Checking database after registration attempt...")
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        user_count_after = result.scalar()
        print(f"👥 Users in database after attempt: {user_count_after}")
        
        if user_count_after > user_count:
            print("✅ New user was created!")
        else:
            print("❌ No new user was created")
    
    await engine.dispose()
    
    print("\n💡 ANALYSIS:")
    print("1. If database shows 0 users but registration fails, there's a caching issue")
    print("2. If database shows users that shouldn't exist, there's a cleanup issue")
    print("3. Check backend server logs for detailed error messages")

if __name__ == "__main__":
    asyncio.run(test_registration_direct())
