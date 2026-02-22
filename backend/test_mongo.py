"""
MongoDB Connection Test Script
Run this to diagnose connection issues
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

print("=" * 60)
print("🔍 MongoDB Connection Diagnostic Tool")
print("=" * 60)

# Load environment variables
load_dotenv()

# Try to get MongoDB URI from different variable names
mongodb_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")

print("\n📋 Environment Check:")
print(f"  MONGODB_URI set: {os.getenv('MONGODB_URI') is not None}")
print(f"  MONGO_URI set: {os.getenv('MONGO_URI') is not None}")

if not mongodb_uri:
    print("\n❌ ERROR: No MongoDB connection string found!")
    print("\nPlease set MONGODB_URI in your .env file:")
    print("MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority")
    exit(1)

print(f"\n🔗 Connection String:")
print(f"  Protocol: {mongodb_uri.split('://')[0]}")
print(f"  First 30 chars: {mongodb_uri[:30]}...")
print(f"  Last 20 chars: ...{mongodb_uri[-20:]}")

# Check for common issues
print("\n🔍 Checking for common issues...")

issues = []

if mongodb_uri.startswith("mongodb://") and "mongodb.net" in mongodb_uri:
    issues.append("❌ Using 'mongodb://' instead of 'mongodb+srv://' for Atlas")
    issues.append("   Fix: Change 'mongodb://' to 'mongodb+srv://'")

if ":27017" in mongodb_uri and "mongodb+srv" in mongodb_uri:
    issues.append("❌ Port number in SRV connection string")
    issues.append("   Fix: Remove ':27017' when using mongodb+srv://")

if "@" not in mongodb_uri:
    issues.append("❌ No credentials found in connection string")
    issues.append("   Fix: Include username and password")

if "<password>" in mongodb_uri or "<username>" in mongodb_uri:
    issues.append("❌ Placeholder not replaced in connection string")
    issues.append("   Fix: Replace <username> and <password> with actual values")

if issues:
    print("\n⚠️  ISSUES FOUND:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("  ✅ No obvious issues detected")

# Attempt connection
print("\n🔌 Attempting connection...")
print("  Timeout: 30 seconds")

try:
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )
    
    # Force connection
    info = client.server_info()
    
    print("\n✅ SUCCESS! MongoDB connection works!")
    print(f"\n📊 Server Info:")
    print(f"  Version: {info.get('version')}")
    print(f"  Git Version: {info.get('gitVersion', 'N/A')}")
    
    # Get database
    db = client.get_database()
    print(f"\n💾 Database Info:")
    print(f"  Name: {db.name}")
    print(f"  Collections: {db.list_collection_names()}")
    
    print("\n✅ Your MongoDB connection is working correctly!")
    print("You can now run your Flask app.")
    
except Exception as e:
    print(f"\n❌ CONNECTION FAILED!")
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    
    print("\n🔧 Troubleshooting Steps:")
    print("  1. Check your connection string format")
    print("  2. Verify username and password are correct")
    print("  3. Ensure your IP is whitelisted in MongoDB Atlas")
    print("     - Go to Network Access")
    print("     - Add IP Address: 0.0.0.0/0")
    print("  4. Check if the database user exists")
    print("     - Go to Database Access")
    print("     - Verify user is listed with correct permissions")
    print("  5. If password has special characters, URL-encode them")
    print("     - @ becomes %40")
    print("     - # becomes %23")
    print("     - $ becomes %24")
    
    print("\n📖 Get correct connection string:")
    print("  1. Go to https://cloud.mongodb.com")
    print("  2. Click Database → Connect → Drivers")
    print("  3. Copy the connection string")
    print("  4. Replace <password> with your actual password")
    print("  5. Add database name: /verifychain before the ?")
    
print("\n" + "=" * 60)