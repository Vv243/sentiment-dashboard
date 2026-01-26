"""
Sentiment analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.sentiment_analyzer import sentiment_analyzer
from app.database import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Tesla stock is going to the moon! 🚀"
            }
        }


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis"""
    text: str
    sentiment: str
    emoji: str
    scores: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    saved_to_db: bool = False
    moderation: dict = Field(default_factory=dict)  # NEW: Add this line
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Tesla stock is going to the moon! 🚀",
                "sentiment": "positive",
                "emoji": "😊",
                "scores": {
                    "positive": 0.754,
                    "negative": 0.0,
                    "neutral": 0.246,
                    "compound": 0.875
                },
                "timestamp": "2026-01-24T13:20:54.123456",
                "saved_to_db": True,
                "moderation": {
                    "flagged": False,
                    "reason": None,
                    "severity": "safe"
                }
            }
        }


@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text using VADER.
    
    Returns sentiment classification and scores.
    Saves the result to MongoDB for history tracking.
    """
    logger.info(f"📥 Received sentiment analysis request")
    
    # Analyze sentiment
    result = sentiment_analyzer.analyze(request.text)
    
    # Add timestamp
    timestamp = datetime.utcnow()
    result['timestamp'] = timestamp
    
    # Save to MongoDB
    saved_to_db = False
    try:
        db = get_database()
        if db is not None:
            # Create document to save
            sentiment_record = {
                "text": request.text,
                "sentiment": result['sentiment'],
                "emoji": result['emoji'],
                "scores": result['scores'],
                "timestamp": timestamp
            }
            
            # Insert into 'sentiment_analyses' collection
            await db.sentiment_analyses.insert_one(sentiment_record)
            saved_to_db = True
            logger.info(f"💾 Saved sentiment analysis to MongoDB")
        else:
            logger.warning("⚠️ Database not available, skipping save")
    except Exception as e:
        logger.error(f"❌ Error saving to database: {e}")
        # Don't fail the request if database save fails
    
    result['saved_to_db'] = saved_to_db
    
    logger.info(f"📤 Returning result: {result['sentiment']}")
    
    return result

@router.get("/history")
async def get_sentiment_history(limit: int = 10):
    """Get recent sentiment analysis history."""
    logger.info(f"📊 Fetching sentiment history (limit: {limit})")
    
    # Validate limit
    if limit < 1:
        limit = 10
    elif limit > 100:
        limit = 100
    
    db = get_database()
    
    # If database unavailable, return empty gracefully
    if db is None:
        logger.warning("⚠️ Database not available")
        return {
            "count": 0,
            "limit": limit,
            "analyses": []
        }
    
    try:
        # Get recent analyses
        cursor = db.sentiment_analyses.find().sort("timestamp", -1).limit(limit)
        analyses = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            analyses.append(doc)
        
        logger.info(f"📤 Returning {len(analyses)} analyses")
        return {
            "count": len(analyses),
            "limit": limit,
            "analyses": analyses
        }
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return {
            "count": 0,
            "limit": limit,
            "analyses": []
        }