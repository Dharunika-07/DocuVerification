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

# Get MongoDB URI
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

print("\n🔌 Attempting connection...")

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
    print(f"  Server Version: {info.get('version')}")

    db = client.get_database()
    print(f"\n💾 Database Name: {db.name}")
    print(f"📂 Collections: {db.list_collection_names()}")

except Exception as e:
    print("\n❌ CONNECTION FAILED!")
    print("Error:", str(e))

print("\n" + "=" * 60)