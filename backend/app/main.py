"""
Main FastAPI application file.
"""

"""
Main FastAPI application file.
"""

# LOAD ENVIRONMENT VARIABLES FIRST - BEFORE ANY OTHER IMPORTS
from dotenv import load_dotenv
import os

# Load .env.local ONLY - with override to force it
load_dotenv('.env.local', override=True)

# DEBUG: Print which database we're using
db_url = os.getenv('DATABASE_URL', 'NOT SET')
print("\n" + "="*60)
print("🔍 DATABASE CONNECTION DEBUG")
print("="*60)
print(f"DATABASE_URL: {db_url}")
if 'localhost' in db_url:
    print("✅ Using LOCAL database (sentiment_test)")
elif 'render' in db_url or 'railway' in db_url or 'supabase' in db_url:
    print("❌ WARNING: Using PRODUCTION database!")
else:
    print("⚠️ Unknown database location")
print("="*60 + "\n")

from app.api import sentiment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import logging

# Import database functions - UPDATED FOR POSTGRESQL
from app.database import connect_to_postgres, close_postgres_connection


# Set up logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Real-time sentiment analysis for stocks and cryptocurrencies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    sentiment.router,
    prefix=f"{settings.API_V1_STR}/sentiment",
    tags = ["sentiment"]
)    


@app.get("/")
async def root():
    """Welcome endpoint"""
    logger.info("📍 Root endpoint accessed")
    return {
        "message": "Welcome to Sentiment Analysis API! 🚀",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "api": settings.API_V1_STR,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("🏥 Health check performed")
    return {
        "status": "healthy",
        "service": "Sentiment Analysis API",
        "version": "1.0.0",
    }


@app.on_event("startup")
async def startup_event():
    """Runs when the application starts"""
    logger.info("🚀 Starting Sentiment Analysis API...")
    logger.info(f"📝 Documentation available at: /docs")
    logger.info(f"🏥 Health check available at: /health")
    
    # Initialize content moderator
    from app.services.content_moderator import content_moderator
    logger.info(f"🛡️ Content moderator ready: {len(content_moderator.harmful_patterns)} patterns")
    
    # Connect to PostgreSQL (SYNCHRONOUS - no await)
    logger.info("📦 Connecting to PostgreSQL...")
    connect_to_postgres()  # NO await - this is synchronous!
    
    logger.info("✅ Startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """Runs when the application shuts down"""
    logger.info("👋 Shutting down Sentiment Analysis API...")
    
    # Close PostgreSQL connection (SYNCHRONOUS - no await)
    logger.info("📦 Closing PostgreSQL connection...")
    close_postgres_connection()  # NO await - this is synchronous!
    
    logger.info("✅ Shutdown complete!")