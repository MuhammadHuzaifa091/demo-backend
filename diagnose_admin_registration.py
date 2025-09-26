#!/usr/bin/env python3

# Final diagnosis - check what's happening with admin role specifically
# Run this: python diagnose_admin_registration.py

import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings

async def diagnose_admin_registration():
    print("🔍 Diagnosing Admin Registration Issue\n")
    
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
    
    # Test different roles
    roles_to_test = ['user', 'admin', 'provider']
    
    for role in roles_to_test:
        print(f"\n🧪 Testing registration with role: {role}")
        
        async with httpx.AsyncClient() as client:
            try:
                test_data = {
                    "email": f"test{role}{int(asyncio.get_event_loop().time())}@example.com",
                    "password": "test123",
                    "first_name": "Test",
                    "last_name": role.capitalize(),
                    "role": role
                }
                
                print(f"📧 Attempting: {test_data['email']} with role: {role}")
                
                response = await client.post(
                    "https://demo.publicvm.com/api/v1/auth/register-with-role",
                    json=test_data,
                    timeout=15.0
                )
                
                if response.status_code == 201:
                    print(f"✅ {role.upper()} registration successful!")
                    result = response.json()
                    print(f"   Created user: {result['email']} with role: {result['role']}")
                else:
                    print(f"❌ {role.upper()} registration failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ {role.upper()} registration request failed: {str(e)}")
    
    # Check database after all attempts
    print(f"\n📊 Final database state:")
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        final_count = result.scalar()
        print(f"👥 Total users: {final_count}")
        
        if final_count > 0:
            result = await session.execute(text("SELECT email, role FROM users"))
            users = result.fetchall()
            print("📋 All users:")
            for user in users:
                print(f"  - {user[0]} ({user[1]})")
    
    await engine.dispose()
    
    print("\n🎯 CONCLUSION:")
    print("If 'user' role works but 'admin' fails, there's a role-specific issue.")
    print("If all roles fail after the first one, there's a caching/session issue.")
    print("The database shows 0 users but registration fails = API layer problem.")

if __name__ == "__main__":
    asyncio.run(diagnose_admin_registration())
