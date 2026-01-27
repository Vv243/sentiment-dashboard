"""
Sentiment analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.sentiment_analyzer import sentiment_analyzer
from app.database import get_connection, cleanup_old_records  # ADDED cleanup_old_records
from datetime import datetime
import logging
import random  # For periodic cleanup

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
    moderation: dict = Field(default_factory=dict)
    
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
    Saves the result to PostgreSQL for history tracking.
    """
    logger.info(f"📥 Received sentiment analysis request")
    
    # Analyze sentiment
    result = sentiment_analyzer.analyze(request.text)
    
    # Add timestamp
    timestamp = datetime.utcnow()
    result['timestamp'] = timestamp
    
    # Save to PostgreSQL using pg8000
    saved_to_db = False
    try:
        conn = get_connection()
        if conn is not None:
            conn.run('''
                INSERT INTO sentiment_analyses 
                (text, sentiment, emoji, positive, negative, neutral, compound, 
                 timestamp, flagged, moderation_reason, moderation_severity)
                VALUES (:text, :sentiment, :emoji, :positive, :negative, :neutral, :compound, 
                        :timestamp, :flagged, :reason, :severity)
            ''',
                text=request.text,
                sentiment=result['sentiment'],
                emoji=result['emoji'],
                positive=result['scores']['positive'],
                negative=result['scores']['negative'],
                neutral=result['scores']['neutral'],
                compound=result['scores']['compound'],
                timestamp=timestamp,
                flagged=result['moderation']['flagged'],
                reason=result['moderation']['reason'],
                severity=result['moderation']['severity']
            )
            saved_to_db = True
            logger.info(f"💾 Saved sentiment analysis to PostgreSQL")
            
            # Periodic cleanup: 10% chance to run cleanup after each save
            # This prevents running cleanup on EVERY request (performance)
            if random.randint(1, 10) == 1:  # 10% chance
                cleanup_old_records(keep_last=10000)
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
    
    conn = get_connection()
    
    # If database unavailable, return empty gracefully
    if conn is None:
        logger.warning("⚠️ Database not available")
        return {
            "count": 0,
            "limit": limit,
            "analyses": []
        }
    
    try:
        # Get recent analyses with SQL query using pg8000
        rows = conn.run('''
            SELECT id, text, sentiment, emoji, 
                   positive, negative, neutral, compound,
                   timestamp, flagged, moderation_reason, moderation_severity
            FROM sentiment_analyses
            ORDER BY timestamp DESC
            LIMIT :limit
        ''', limit=limit)
        
        # Convert to list of dicts
        analyses = []
        for row in rows:
            analyses.append({
                "id": row[0],
                "text": row[1],
                "sentiment": row[2],
                "emoji": row[3],
                "scores": {
                    "positive": float(row[4]),
                    "negative": float(row[5]),
                    "neutral": float(row[6]),
                    "compound": float(row[7])
                },
                "timestamp": row[8].isoformat(),
                "moderation": {
                    "flagged": row[9],
                    "reason": row[10],
                    "severity": row[11]
                }
            })
        
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