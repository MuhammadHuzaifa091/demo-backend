#!/usr/bin/env python3
"""Reset database with proper admin role support."""

import asyncio
import os
import sqlite3
from pathlib import Path

def reset_database():
    """Reset the database and ensure admin role support."""
    print("🔄 Resetting database with admin role support...")
    
    # Database file path
    db_path = Path("database.db")
    
    # Remove existing database
    if db_path.exists():
        os.remove(db_path)
        print("✅ Removed existing database")
    
    # Connect to create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create users table with proper role support
        cursor.execute("""
            CREATE TABLE users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                is_superuser BOOLEAN DEFAULT FALSE,
                is_verified BOOLEAN DEFAULT FALSE,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'user' CHECK (role IN ('user', 'provider_individual', 'provider_organization', 'admin')),
                service_type TEXT,
                experience TEXT,
                contact_info TEXT,
                company_name TEXT,
                team_size INTEGER
            )
        """)
        print("✅ Created users table with admin role support")
        
        # Create repair_requests table
        cursor.execute("""
            CREATE TABLE repair_requests (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                voice_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ Created repair_requests table")
        
        # Create service_providers table
        cursor.execute("""
            CREATE TABLE service_providers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                service_type TEXT NOT NULL,
                description TEXT NOT NULL,
                contact_info TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ Created service_providers table")
        
        # Create services table
        cursor.execute("""
            CREATE TABLE services (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                service_type TEXT NOT NULL,
                description TEXT NOT NULL,
                contact_info TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                provider_id TEXT NOT NULL,
                FOREIGN KEY (provider_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ Created services table")
        
        conn.commit()
        print("🎉 Database reset completed successfully!")
        print("📋 Supported roles: user, provider_individual, provider_organization, admin")
        
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = reset_database()
    if success:
        print("\n🚀 Database is ready!")
        print("💡 Now restart your FastAPI server:")
        print("   uvicorn app.main:app --reload")
        print("\n🎯 You can now register admin users!")
    else:
        print("\n❌ Database reset failed!")
