"""
PostgreSQL database connection using pg8000 (pure Python).
"""
import pg8000.native
import logging
import os
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv()

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
        
         # DEBUG: Print database URL details
        print("\n" + "="*60)
        print("🔍 DATABASE.PY DEBUG")
        print("="*60)
        print(f"DATABASE_URL from os.getenv: {database_url}")
        print("="*60 + "\n")
        
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
                moderation_severity VARCHAR(20),
                user_feedback VARCHAR(10)
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

def cleanup_old_records(keep_last=10000):
    """
    Keep only the most recent N records.
    Automatically removes older records AND harmful content to prevent database from filling up.
    
    Args:
        keep_last: Number of most recent records to keep (default: 10000)
    """
    global connection
    
    if connection is None:
        return
    
    try:
        # STEP 1: Delete ALL harmful content first (regardless of age)
        harmful_count = connection.run('SELECT COUNT(*) FROM sentiment_analyses WHERE flagged = TRUE')[0][0]
        if harmful_count > 0:
            connection.run('DELETE FROM sentiment_analyses WHERE flagged = TRUE')
            logger.info(f"🧹 Automatically deleted {harmful_count} harmful records")
        
        # STEP 2: Count total safe records
        count_result = connection.run('SELECT COUNT(*) FROM sentiment_analyses')
        total_records = count_result[0][0]
        
        # STEP 3: Only cleanup old safe records if we exceed the limit
        if total_records > keep_last:
            # Delete all but the last N safe records
            connection.run('''
                DELETE FROM sentiment_analyses
                WHERE id NOT IN (
                    SELECT id FROM sentiment_analyses
                    ORDER BY timestamp DESC
                    LIMIT :keep_last
                )
            ''', keep_last=keep_last)
            
            deleted = total_records - keep_last
            logger.info(f"🧹 Cleaned up {deleted} old safe records, keeping last {keep_last}")
    except Exception as e:
        logger.error(f"❌ Error cleaning up records: {e}")