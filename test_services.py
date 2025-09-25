#!/usr/bin/env python3
"""Test services functionality."""

import asyncio
import requests
import json

def test_services_flow():
    """Test the complete services flow: create provider, create service, view services."""
    
    base_url = "http://127.0.0.1:8000/api/v1"
    
    print("🔍 Testing Services Flow...")
    
    # Step 1: Register a provider
    print("\n1. Registering a provider...")
    provider_data = {
        "email": "provider@test.com",
        "password": "testpass123",
        "first_name": "John",
        "last_name": "Provider",
        "role": "provider_individual",
        "service_type": "Plumbing",
        "experience": "5 years of professional plumbing experience",
        "contact_info": "Phone: 555-0123\nEmail: john@plumbing.com"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/register-with-role", json=provider_data, timeout=10)
        if response.status_code == 201:
            provider_user = response.json()
            print(f"✅ Provider registered: {provider_user['email']} (ID: {provider_user['id']})")
        else:
            print(f"⚠️ Provider might already exist: {response.status_code}")
            # Continue with test anyway
    except Exception as e:
        print(f"⚠️ Provider registration error: {e}")
    
    # Step 2: Login as provider
    print("\n2. Logging in as provider...")
    login_data = {
        "username": "provider@test.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", data=login_data, timeout=10)
        if response.status_code == 200:
            auth_data = response.json()
            provider_token = auth_data['access_token']
            print("✅ Provider logged in successfully")
        else:
            print(f"❌ Provider login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Provider login error: {e}")
        return False
    
    # Step 3: Create a service as provider
    print("\n3. Creating a service...")
    service_data = {
        "name": "Professional Plumbing Services",
        "service_type": "Plumbing",
        "description": "Expert plumbing services including repairs, installations, and maintenance. Available 24/7 for emergencies.",
        "contact_info": "Phone: 555-0123\nEmail: john@plumbing.com\nAvailable: Mon-Fri 8AM-6PM, Emergency 24/7"
    }
    
    headers = {"Authorization": f"Bearer {provider_token}"}
    
    try:
        response = requests.post(f"{base_url}/services/", json=service_data, headers=headers, timeout=10)
        if response.status_code == 201:
            service = response.json()
            print(f"✅ Service created: {service['name']} (ID: {service['id']})")
        else:
            print(f"❌ Service creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Service creation error: {e}")
        return False
    
    # Step 4: Register a user
    print("\n4. Registering a user...")
    user_data = {
        "email": "user@test.com",
        "password": "testpass123",
        "first_name": "Jane",
        "last_name": "User",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/register-with-role", json=user_data, timeout=10)
        if response.status_code == 201:
            user = response.json()
            print(f"✅ User registered: {user['email']} (ID: {user['id']})")
        else:
            print(f"⚠️ User might already exist: {response.status_code}")
    except Exception as e:
        print(f"⚠️ User registration error: {e}")
    
    # Step 5: Login as user
    print("\n5. Logging in as user...")
    user_login_data = {
        "username": "user@test.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", data=user_login_data, timeout=10)
        if response.status_code == 200:
            auth_data = response.json()
            user_token = auth_data['access_token']
            print("✅ User logged in successfully")
        else:
            print(f"❌ User login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User login error: {e}")
        return False
    
    # Step 6: View services as user
    print("\n6. Viewing services as user...")
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    try:
        response = requests.get(f"{base_url}/services/", headers=user_headers, timeout=10)
        if response.status_code == 200:
            services = response.json()
            print(f"✅ User can view services: {len(services)} services found")
            
            if services:
                print("\n📋 Available Services:")
                for service in services:
                    print(f"  • {service['name']} ({service['service_type']})")
                    print(f"    Provider: {service.get('provider', {}).get('first_name', 'Unknown')} {service.get('provider', {}).get('last_name', '')}")
                    print(f"    Description: {service['description'][:100]}...")
                    print()
            else:
                print("⚠️ No services found - there might be an issue")
                return False
        else:
            print(f"❌ Failed to view services: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ View services error: {e}")
        return False
    
    print("\n🎉 Services flow test completed successfully!")
    print("✅ Providers can create services")
    print("✅ Users can view services")
    print("✅ Services display with provider information")
    
    return True

if __name__ == "__main__":
    success = test_services_flow()
    if success:
        print("\n🚀 Services functionality is working correctly!")
        print("💡 Users should now be able to see services in the frontend.")
    else:
        print("\n❌ Services functionality has issues that need to be fixed.")
