#!/usr/bin/env python3
"""
Development startup script for JiaWeiTong Home Service Connect.
This script will set up the database and start the development server.
"""

import subprocess
import sys
from pathlib import Path

def run_migration():
    """Run the database migration."""
    print("🔧 Running database migration...")
    try:
        subprocess.run([sys.executable, "create_migration.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Migration failed!")
        return False
    return True

def start_server():
    """Start the FastAPI development server."""
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.run([
            "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")

def main():
    """Main startup function."""
    print("🏠 JiaWeiTong Home Service Connect - Development Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the project root directory!")
        sys.exit(1)
    
    # Run migration
    if not run_migration():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
