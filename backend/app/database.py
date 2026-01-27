"""
PostgreSQL database connection using pg8000 (pure Python).
"""
import pg8000.native
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database connection
connection = None

def connect_to_postgres():
    """Connect to PostgreSQL when the application starts"""
    global connection
    try:
        # Get PostgreSQL URL from environment
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            logger.warning("⚠️ DATABASE_URL not found - running without database")
            return
        
        # Parse the connection URL
        # Format: postgresql://user:password@host:port/database
        logger.info("📦 Attempting PostgreSQL connection...")
        
        # pg8000 uses individual parameters, parse the URL
        import urllib.parse
        result = urllib.parse.urlparse(database_url)
        
        connection = pg8000.native.Connection(
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port or 5432,
            database=result.path[1:]  # Remove leading /
        )
        
        # Test the connection
        version = connection.run("SELECT version()")[0][0]
        logger.info(f"✅ Connected to PostgreSQL")
        logger.info(f"📊 Database version: {version[:50]}...")
        
        # Create tables
        create_tables()
        
    except Exception as e:
        logger.warning(f"⚠️ PostgreSQL connection failed: {e}")
        logger.warning("⚠️ API will run WITHOUT database persistence")
        connection = None

def create_tables():
    """Create sentiment_analyses table if it doesn't exist"""
    try:
        connection.run('''
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
        connection.run('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON sentiment_analyses(timestamp DESC)
        ''')
        
        logger.info("✅ Database tables ready")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")

def close_postgres_connection():
    """Close PostgreSQL connection when application shuts down"""
    global connection
    if connection:
        connection.close()
        logger.info("Closed PostgreSQL connection")

def get_connection():
    """Get the database connection - may return None"""
    return connection