"""
PostgreSQL database connection using psycopg2 (synchronous).
"""
import psycopg2
from psycopg2.pool import SimpleConnectionPool
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# PostgreSQL connection pool
pool: SimpleConnectionPool = None

def connect_to_postgres():
    """Connect to PostgreSQL when the application starts"""
    global pool
    try:
        # Get PostgreSQL URL from environment
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            logger.warning("⚠️ DATABASE_URL not found - running without database")
            return
        
        # Create connection pool (synchronous)
        logger.info("📦 Attempting PostgreSQL connection...")
        pool = SimpleConnectionPool(
            1,  # min connections
            10,  # max connections
            database_url
        )
        
        # Test the connection
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT version()')
            version = cursor.fetchone()[0]
            logger.info(f"✅ Connected to PostgreSQL")
            logger.info(f"📊 Database version: {version[:50]}...")
            
            # Create tables
            create_tables(conn)
            conn.commit()
        finally:
            pool.putconn(conn)
        
    except Exception as e:
        logger.warning(f"⚠️ PostgreSQL connection failed: {e}")
        logger.warning("⚠️ API will run WITHOUT database persistence")
        pool = None

def create_tables(conn):
    """Create sentiment_analyses table if it doesn't exist"""
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
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
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON sentiment_analyses(timestamp DESC)
        ''')
        
        logger.info("✅ Database tables ready")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")

def close_postgres_connection():
    """Close PostgreSQL connection when application shuts down"""
    global pool
    if pool:
        pool.closeall()
        logger.info("Closed PostgreSQL connection")

def get_pool():
    """Get the connection pool - may return None"""
    return pool