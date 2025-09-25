#!/usr/bin/env python3
"""Test admin role validation."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_admin_role():
    """Test if admin role is properly defined."""
    try:
        from app.models.user_roles import UserRole
        from app.schemas.user import RoleBasedRegistration, UserCreate
        
        print("🔍 Testing UserRole enum...")
        print(f"Available roles: {[role.value for role in UserRole]}")
        print(f"Admin role exists: {'admin' in [role.value for role in UserRole]}")
        
        # Test creating a RoleBasedRegistration with admin role
        print("\n🔍 Testing RoleBasedRegistration schema...")
        try:
            test_data = {
                "email": "admin@test.com",
                "password": "testpass123",
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin"
            }
            
            registration = RoleBasedRegistration(**test_data)
            print(f"✅ RoleBasedRegistration created successfully with role: {registration.role}")
            print(f"Role type: {type(registration.role)}")
            
        except Exception as e:
            print(f"❌ RoleBasedRegistration failed: {str(e)}")
            return False
        
        # Test creating UserCreate with admin role
        print("\n🔍 Testing UserCreate schema...")
        try:
            user_create = UserCreate(
                email="admin@test.com",
                password="testpass123",
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN
            )
            print(f"✅ UserCreate created successfully with role: {user_create.role}")
            
        except Exception as e:
            print(f"❌ UserCreate failed: {str(e)}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_admin_role()
    if success:
        print("\n🎉 Admin role validation passed!")
        print("💡 The issue might be with the database or server cache.")
        print("🔄 Try restarting the FastAPI server.")
    else:
        print("\n❌ Admin role validation failed!")
        print("🔧 Schema or enum definition needs to be fixed.")
