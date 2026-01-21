"""
Database connection management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.core.config import settings


class Database:
    """Database connection manager"""
    client: Optional[AsyncIOMotorClient] = None
    

db = Database()


async def get_database():
    """Get database instance"""
    return db.client[settings.DATABASE_NAME]


async def connect_to_mongo():
    """Connect to MongoDB"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    # Test connection
    await db.client.admin.command('ping')
    print(f"Connected to MongoDB at {settings.MONGODB_URL}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("MongoDB connection closed")


async def get_collection(collection_name: str):
    """Get a collection from database"""
    database = await get_database()
    return database[collection_name]
