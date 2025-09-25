#!/usr/bin/env python3
"""Quick test of admin registration."""

import requests
import json

def test_admin_registration():
    """Test admin registration endpoint."""
    
    url = "http://127.0.0.1:8000/api/v1/auth/register-with-role"
    
    data = {
        "email": "newadmin@example.com",
        "password": "testpass123",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin"
    }
    
    print("🔍 Testing admin registration endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        print(f"\n📊 Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Body: {response.text}")
        
        if response.status_code == 201:
            print("\n✅ SUCCESS: Admin registration worked!")
            return True
        elif response.status_code == 422:
            print("\n❌ VALIDATION ERROR: Still getting validation error")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
            return False
        else:
            print(f"\n❌ ERROR: Unexpected status code {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ CONNECTION ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_admin_registration()
    if success:
        print("\n🎉 Admin registration is working! You can now register admin users.")
    else:
        print("\n🔧 There's still an issue with admin registration.")
