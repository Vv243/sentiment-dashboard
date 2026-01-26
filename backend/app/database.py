from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# MongoDB client - will be set when app starts
mongodb_client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo():
    """Connect to MongoDB when the application starts - NON-BLOCKING"""
    global mongodb_client, database
    try:
        # Get MongoDB settings from environment variables
        mongodb_url = os.getenv("MONGODB_URL")
        database_name = os.getenv("DATABASE_NAME", "sentiment_db")
        
        if not mongodb_url:
            logger.warning("⚠️ MONGODB_URL not found - running without database")
            return
        
        # Try to connect with timeout
        logger.info("📦 Attempting MongoDB connection...")
        mongodb_client = AsyncIOMotorClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000
        )
        
        # Test the connection with timeout
        await mongodb_client.admin.command('ping')
        database = mongodb_client[database_name]
        logger.info(f"✅ Connected to MongoDB: {database_name}")
        
    except Exception as e:
        logger.warning(f"⚠️ MongoDB connection failed: {e}")
        logger.warning("⚠️ API will run WITHOUT database persistence")
        # Don't raise - let the API start anyway
        mongodb_client = None
        database = None

async def close_mongo_connection():
    """Close MongoDB connection when application shuts down"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        logger.info("Closed MongoDB connection")

def get_database():
    """Get the database instance - may return None"""
    return database