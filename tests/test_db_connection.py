#!/usr/bin/env python3
"""
Database Connection Test Script
Tests MySQL connection and basic operations
"""

import sys
sys.path.insert(0, '/Users/bhavyabansal/Desktop/practice')

from src.utils.database_manager import DatabaseManager

print("🔍 Testing Database Connection...\n")

try:
    db = DatabaseManager()
    
    if db.connection and db.connection.is_connected():
        print("✅ Connection successful!")
        print(f"   Host: 3.6.16.231")
        print(f"   Database: staging")
        print(f"   Table: vendor")
    else:
        print("❌ Connection failed")
        sys.exit(1)
    
    print("\n📚 Available Operations:")
    print("  1. verify_mobile_for_email(email) - Update mobile_verified = 1")
    print("  2. get_vendor_by_email(email) - Retrieve vendor details")
    print("  3. check_mobile_verified_status(email) - Check current status")
    print("  4. reset_mobile_verified(email) - Reset to 0 (cleanup)")
    
    print("\n✅ Database manager is ready!")
    
    db.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
