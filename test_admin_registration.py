#!/usr/bin/env python3
"""Test admin registration endpoint."""

import asyncio
import httpx

async def test_admin_registration():
    """Test the admin registration endpoint."""
    
    admin_data = {
        "email": "admin@test.com",
        "password": "testpass123",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin"
    }
    
    print("🔍 Testing admin registration...")
    print(f"Data: {admin_data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/auth/register-with-role",
                json=admin_data
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ Admin registration successful!")
                return True
            else:
                print("❌ Admin registration failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error testing registration: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_admin_registration())
    if success:
        print("\n🎉 Admin registration is working!")
    else:
        print("\n❌ Admin registration still has issues.")
