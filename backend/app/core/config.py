"""
Configuration settings for the Sentiment Analysis API.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sentiment Analysis Dashboard"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "sentiment_db"
    
    # Reddit API Credentials
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: str = "sentiment_analyzer_v1.0"
    
    # Twitter API Credentials (Optional)
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    # Sentiment Analysis Configuration
    USE_VADER: bool = True
    USE_FINBERT: bool = False
    
    # Backup System Configuration
    USE_SYNTHETIC_FALLBACK: bool = True
    MIN_REAL_POSTS_THRESHOLD: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings object
settings = Settings()


# Helper functions
def is_reddit_configured() -> bool:
    """Check if Reddit API credentials are set"""
    return bool(settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET)


def is_twitter_configured() -> bool:
    """Check if Twitter API credentials are set"""
    return bool(settings.TWITTER_BEARER_TOKEN)
