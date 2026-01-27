"""
Sentiment analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.sentiment_analyzer import sentiment_analyzer
from app.database import get_connection  # UPDATED for pg8000
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
        else:
            logger.warning(