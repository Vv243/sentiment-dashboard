"""
PostgreSQL database connection and management.
"""
import asyncpg
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# PostgreSQL connection pool
pool: asyncpg.Pool = None

async def connect_to_postgres():
    """Connect to PostgreSQL when the application starts"""
    global pool
    try:
        # Get PostgreSQL URL from environment
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            logger.warning("⚠️ DATABASE_URL not found - running without database")
            return
        
        # Create connection pool
        logger.info("📦 Attempting PostgreSQL connection...")
        pool = await asyncpg.create_pool(
            database_url,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        
        # Test the connection and get version
        async with pool.acquire() as conn:
            version = await conn.fetchval('SELECT version()')
            logger.info(f"✅ Connected to PostgreSQL")
            logger.info(f"📊 Database version: {version[:50]}...")
            
            # Create table if it doesn't exist
            await create_tables(conn)
        
    except Exception as e:
        logger.warning(f"⚠️ PostgreSQL connection failed: {e}")
        logger.warning("⚠️ API will run WITHOUT database persistence")
        pool = None

async def create_tables(conn):
    """Create sentiment_analyses table if it doesn't exist"""
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_analyses (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                sentiment VARCHAR(50) NOT NULL,
                emoji VARCHAR(10) NOT NULL,
                positive REAL NOT NULL,
                negative REAL NOT NULL,
                neutral REAL NOT NULL,
                compound REAL NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                flagged BOOLEAN DEFAULT FALSE,
                moderation_reason TEXT,
                moderation_severity VARCHAR(20)
            )
        ''')
        
        # Create index on timestamp for faster queries
        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON sentiment_analyses(timestamp DESC)
        ''')
        
        logger.info("✅ Database tables ready")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")

async def close_postgres_connection():
    """Close PostgreSQL connection when application shuts down"""
    global pool
    if pool:
        await pool.close()
        logger.info("Closed PostgreSQL connection")

def get_pool():
    """Get the connection pool - may return None"""
    return pool