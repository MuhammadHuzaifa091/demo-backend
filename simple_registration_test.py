#!/usr/bin/env python3

# Simple registration test to identify the exact issue
# Run this: python simple_registration_test.py

import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings

async def simple_registration_test():
    print("🔍 Simple Registration Test - Finding the Root Cause\n")
    
    # Create database connection
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Check database state
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"👥 Current users in database: {user_count}")
        
        if user_count > 0:
            result = await session.execute(text("SELECT email, role FROM users"))
            users = result.fetchall()
            print("📋 Existing users:")
            for user in users:
                print(f"  - {user[0]} ({user[1]})")
    
    # Test with debug endpoint first
    print(f"\n🧪 Testing debug endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            debug_data = {
                "email": f"debug{int(asyncio.get_event_loop().time())}@example.com",
                "password": "debug123",
                "first_name": "Debug",
                "last_name": "User",
                "role": "user"
            }
            
            response = await client.post(
                "https://demo.publicvm.com/api/v1/auth/debug-registration",
                json=debug_data,
                timeout=10.0
            )
            
            print(f"Debug endpoint status: {response.status_code}")
            if response.status_code == 200:
                print("Debug response:", response.json())
            else:
                print("Debug error:", response.text)
                
        except Exception as e:
            print(f"❌ Debug endpoint failed: {str(e)}")
    
    # Test actual registration
    print(f"\n🧪 Testing actual registration...")
    async with httpx.AsyncClient() as client:
        try:
            reg_data = {
                "email": f"test{int(asyncio.get_event_loop().time())}@example.com",
                "password": "test123",
                "first_name": "Test",
                "last_name": "User",
                "role": "user"
            }
            
            print(f"📧 Attempting registration with: {reg_data['email']}")
            
            response = await client.post(
                "https://demo.publicvm.com/api/v1/auth/register-with-role",
                json=reg_data,
                timeout=15.0
            )
            
            print(f"Registration status: {response.status_code}")
            if response.status_code == 201:
                print("✅ Registration successful!")
                print("Response:", response.json())
            else:
                print("❌ Registration failed")
                print("Error:", response.text)
                
        except Exception as e:
            print(f"❌ Registration request failed: {str(e)}")
    
    # Check database after attempt
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        final_count = result.scalar()
        print(f"\n👥 Final users in database: {final_count}")
    
    await engine.dispose()
    
    print("\n🔍 ROOT CAUSE ANALYSIS:")
    print("The issue appears to be that the API is incorrectly reporting")
    print("'User with this email already exists' even when the database is empty.")
    print("This suggests a problem in the user lookup logic or caching.")

if __name__ == "__main__":
    asyncio.run(simple_registration_test())
