"""
Sentiment analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import SentimentRequest, SentimentResponse  # Import from schemas
from app.services.sentiment_analyzer import sentiment_analyzer
from app.database import get_connection, cleanup_old_records
from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text using VADER or DistilBERT.
    
    Models:
    - vader: Fast, rule-based (50ms)
    - distilbert: Accurate, ML-based (200ms)
    """
    logger.info(f"📥 Received request (model: {request.model})")
    
    # Analyze with specified model
    result = sentiment_analyzer.analyze(request.text, model=request.model)
    
    # Add timestamp
    timestamp = datetime.utcnow()
    result['timestamp'] = timestamp
    
    # Save to PostgreSQL using pg8000 (skip if harmful)
    saved_to_db = False
    try:
        conn = get_connection()
        # Don't save harmful content to database
        if conn is not None and not result['moderation']['flagged']:
            conn.run('''
                INSERT INTO sentiment_analyses 
                (text, sentiment, emoji, positive, negative, neutral, compound, 
                 timestamp, flagged, moderation_reason, moderation_severity, model)
                VALUES (:text, :sentiment, :emoji, :positive, :negative, :neutral, :compound, 
                        :timestamp, :flagged, :reason, :severity, :model)
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
                severity=result['moderation']['severity'],
                model=request.model
            )
            saved_to_db = True
            logger.info(f"💾 Saved sentiment analysis to PostgreSQL")
            
            # Periodic cleanup: 10% chance to run cleanup after each save
            if random.randint(1, 10) == 1:
                cleanup_old_records(keep_last=10000)
        elif result['moderation']['flagged']:
            logger.warning("⚠️ Harmful content not saved to database")
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
                   timestamp, flagged, moderation_reason, moderation_severity,
                   user_feedback, model
            FROM sentiment_analyses
            ORDER BY timestamp DESC
            LIMIT :limit
        ''', limit=limit)
        
        # Convert to list of dicts
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
                },
                "user_feedback": row[12],
                "model": row[13]  # NEW: Return which model was used
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
    
@router.post("/feedback/{analysis_id}")
async def submit_feedback(analysis_id: int, feedback: str = "positive"):
    """
    Submit user feedback (thumbs up/down) for an analysis.
    
    Args:
        analysis_id: ID of the sentiment analysis
        feedback: "positive" or "negative"
    """
    from app.database import get_connection
    
    connection = get_connection()
    if connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    # Validate feedback
    if feedback not in ["positive", "negative"]:
        raise HTTPException(status_code=400, detail="Feedback must be 'positive' or 'negative'")
    
    try:
        # Update the analysis with feedback
        connection.run(
            "UPDATE sentiment_analyses SET user_feedback = :feedback WHERE id = :id",
            feedback=feedback,
            id=analysis_id
        )
        
        logger.info(f"✅ Feedback recorded: {feedback} for analysis {analysis_id}")
        
        return {
            "success": True,
            "analysis_id": analysis_id,
            "feedback": feedback,
            "message": "Feedback recorded successfully"
        }
        
    except Exception as e:
        logger.error(f"❌ Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to record feedback")