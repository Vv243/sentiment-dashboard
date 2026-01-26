from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# MongoDB client - will be set when app starts
mongodb_client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo():
    """Connect to MongoDB when the application starts"""
    global mongodb_client, database
    try:
        # Get MongoDB settings from environment variables
        mongodb_url = os.getenv("MONGODB_URL")
        database_name = os.getenv("DATABASE_NAME", "sentiment_db")
        
        if not mongodb_url:
            raise ValueError("MONGODB_URL not found in environment variables")
        
        # MongoDB client with SSL/TLS settings for production
        mongodb_client = AsyncIOMotorClient(
            mongodb_url,
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        database = mongodb_client[database_name]
        
        # Test the connection
        await mongodb_client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {database_name}")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection when application shuts down"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        logger.info("Closed MongoDB connection")

def get_database():
    """Get the database instance"""
    return database