#!/usr/bin/env python3
"""Debug the role validation issue."""

# Test the UserRole enum directly
print("Testing UserRole enum...")

try:
    from app.models.user_roles import UserRole
    print(f"✅ UserRole imported successfully")
    print(f"Available roles: {[role.value for role in UserRole]}")
    print(f"Admin role: {UserRole.ADMIN}")
    print(f"Admin value: {UserRole.ADMIN.value}")
except Exception as e:
    print(f"❌ Error importing UserRole: {e}")
    exit(1)

# Test Pydantic validation
print("\nTesting Pydantic validation...")

try:
    from pydantic import BaseModel
    from typing import Optional
    
    class TestRegistration(BaseModel):
        email: str
        password: str
        first_name: str
        last_name: str
        role: UserRole
        service_type: Optional[str] = None
    
    # Test with admin role
    test_data = {
        "email": "admin@test.com",
        "password": "testpass123",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin"
    }
    
    registration = TestRegistration(**test_data)
    print(f"✅ Pydantic validation passed!")
    print(f"Role: {registration.role}")
    print(f"Role type: {type(registration.role)}")
    
except Exception as e:
    print(f"❌ Pydantic validation failed: {e}")
    
    # Try with enum directly
    try:
        test_data["role"] = UserRole.ADMIN
        registration = TestRegistration(**test_data)
        print(f"✅ Pydantic validation with enum passed!")
        print(f"Role: {registration.role}")
    except Exception as e2:
        print(f"❌ Even enum validation failed: {e2}")

print("\nDone!")
