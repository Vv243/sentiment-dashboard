"""
Main FastAPI application file.
"""

from app.api import sentiment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import logging

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
    logger.info("📍 Root endpoint accessed")  # ← Keep this one!
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
    logger.info("✅ Startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """Runs when the application shuts down"""
    logger.info("👋 Shutting down Sentiment Analysis API...")