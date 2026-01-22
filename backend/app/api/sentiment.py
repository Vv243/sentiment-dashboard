"""
Sentiment analysis API endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.sentiment_analyzer import sentiment_analyzer
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
                }
            }
        }


@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text using VADER.
    
    Returns sentiment classification and scores.
    """
    logger.info(f"📥 Received sentiment analysis request")
    
    result = sentiment_analyzer.analyze(request.text)
    
    logger.info(f"📤 Returning result: {result['sentiment']}")
    
    return result
