#!/usr/bin/env python3
"""
Manual migration script to add role fields to users table.
Run this script to update the database with the new role-based fields.
"""

import asyncio
import sqlite3
from pathlib import Path

def create_migration():
    """Create the migration for role-based fields."""
    
    # Database file path
    db_path = Path("app.db")
    
    if not db_path.exists():
        print("Database file not found. Creating new database...")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if role column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'role' not in columns:
            print("Adding role-based columns to users table...")
            
            # Add new columns to users table
            cursor.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "user"')
            cursor.execute('ALTER TABLE users ADD COLUMN service_type TEXT')
            cursor.execute('ALTER TABLE users ADD COLUMN experience TEXT')
            cursor.execute('ALTER TABLE users ADD COLUMN contact_info TEXT')
            cursor.execute('ALTER TABLE users ADD COLUMN company_name TEXT')
            cursor.execute('ALTER TABLE users ADD COLUMN team_size INTEGER')
            
            conn.commit()
            print("✅ Successfully added role-based columns to users table!")
        else:
            print("✅ Role columns already exist in users table!")
        
        # Check and update repair_requests table
        cursor.execute("PRAGMA table_info(repair_requests)")
        repair_columns = [column[1] for column in cursor.fetchall()]
        
        if 'voice_file' not in repair_columns:
            print("Adding voice_file column to repair_requests table...")
            cursor.execute('ALTER TABLE repair_requests ADD COLUMN voice_file TEXT')
            # Make description optional
            cursor.execute('CREATE TABLE repair_requests_new AS SELECT id, title, description, created_at, user_id, voice_file FROM repair_requests')
            cursor.execute('DROP TABLE repair_requests')
            cursor.execute('ALTER TABLE repair_requests_new RENAME TO repair_requests')
            conn.commit()
            print("✅ Successfully updated repair_requests table!")
        else:
            print("✅ Voice file column already exists in repair_requests table!")
        
        # Create services table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
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
        conn.commit()
        print("✅ Services table created/verified!")
            
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_migration()
