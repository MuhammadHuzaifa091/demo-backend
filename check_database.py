#!/usr/bin/env python3
"""Check database contents and provide cleanup options."""

import sqlite3
from pathlib import Path

def check_database():
    """Check what's in the database."""
    db_path = Path("database.db")

    if not db_path.exists():
        print("❌ Database file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check users table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"👥 Total users in database: {user_count}")

        if user_count > 0:
            cursor.execute("SELECT id, email, role, first_name, last_name FROM users")
            users = cursor.fetchall()
            print("\n📋 Existing users:")
            for user in users:
                print(f"  - ID: {user[0]}, Email: {user[1]}, Role: {user[2]}, Name: {user[3]} {user[4]}")

        # Check repair requests
        cursor.execute("SELECT COUNT(*) FROM repair_requests")
        request_count = cursor.fetchone()[0]
        print(f"\n🔧 Total repair requests: {request_count}")

        if request_count > 0:
            cursor.execute("SELECT id, title, user_id FROM repair_requests LIMIT 5")
            requests = cursor.fetchall()
            print("📝 Recent repair requests:")
            for req in requests:
                print(f"  - ID: {req[0]}, Title: {req[1]}, User: {req[2]}")

        # Check service providers
        cursor.execute("SELECT COUNT(*) FROM service_providers")
        provider_count = cursor.fetchone()[0]
        print(f"\n🏢 Total service providers: {provider_count}")

        # Check services
        cursor.execute("SELECT COUNT(*) FROM services")
        service_count = cursor.fetchone()[0]
        print(f"🔨 Total services: {service_count}")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def clear_database():
    """Clear all data from database but keep structure."""
    db_path = Path("database.db")

    if not db_path.exists():
        print("❌ Database file not found!")
        return

    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Are you sure you want to clear the database? (type 'yes' to confirm): ")

    if confirm.lower() != 'yes':
        print("❌ Operation cancelled")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Clear all tables
        tables = ['users', 'repair_requests', 'service_providers', 'services']
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"✅ Cleared {table} table")

        conn.commit()
        print("🎉 Database cleared successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error clearing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clear_database()
    else:
        print("🔍 Checking database contents...")
        check_database()
        print("\n💡 To clear the database, run: python check_database.py clear")
