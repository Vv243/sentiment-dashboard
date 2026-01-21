"""
Sentiment analysis API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.schemas import (
    TextAnalysisRequest,
    TextAnalysisResponse,
    TickerSentimentSummary,
    HistoricalSentimentResponse,
    SentimentLabel
)
from app.services.sentiment_service import SentimentAnalyzer, get_sentiment_analyzer
from app.core.database import get_collection

router = APIRouter()


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Analyze sentiment of provided text
    
    Args:
        request: Text analysis request with text and model preferences
        
    Returns:
        Sentiment scores from requested models
    """
    try:
        results = analyzer.analyze(
            text=request.text,
            use_vader=request.use_vader,
            use_finbert=request.use_finbert
        )
        
        return TextAnalysisResponse(
            text=request.text,
            vader_score=results['vader_score'],
            finbert_score=results['finbert_score'],
            combined_score=results['combined_score']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.get("/{ticker}", response_model=TickerSentimentSummary)
async def get_ticker_sentiment(ticker: str):
    """
    Get current sentiment summary for a ticker
    
    Args:
        ticker: Stock ticker symbol (e.g., TSLA, AAPL)
        
    Returns:
        Current sentiment summary with aggregated metrics
    """
    try:
        ticker = ticker.upper()
        collection = await get_collection("sentiment_records")
        
        # Get records from last 24 hours
        time_threshold = datetime.utcnow() - timedelta(hours=24)
        
        records = await collection.find({
            "ticker": ticker,
            "timestamp": {"$gte": time_threshold}
        }).to_list(length=1000)
        
        if not records:
            raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
        
        # Calculate aggregated metrics
        total_posts = len(records)
        positive_count = sum(1 for r in records if r['sentiment']['label'] == SentimentLabel.POSITIVE)
        negative_count = sum(1 for r in records if r['sentiment']['label'] == SentimentLabel.NEGATIVE)
        neutral_count = sum(1 for r in records if r['sentiment']['label'] == SentimentLabel.NEUTRAL)
        
        compounds = [r['sentiment']['compound'] for r in records]
        avg_compound = sum(compounds) / len(compounds)
        
        # Determine current label
        if avg_compound >= 0.05:
            label = SentimentLabel.POSITIVE
        elif avg_compound <= -0.05:
            label = SentimentLabel.NEGATIVE
        else:
            label = SentimentLabel.NEUTRAL
        
        # Get latest sentiment
        latest = records[-1]['sentiment']
        
        return TickerSentimentSummary(
            ticker=ticker,
            current_sentiment={
                "compound": avg_compound,
                "positive": sum(r['sentiment']['positive'] for r in records) / total_posts,
                "negative": sum(r['sentiment']['negative'] for r in records) / total_posts,
                "neutral": sum(r['sentiment']['neutral'] for r in records) / total_posts,
                "label": label
            },
            total_posts=total_posts,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            avg_compound=avg_compound,
            last_updated=records[-1]['timestamp']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sentiment: {str(e)}")


@router.get("/{ticker}/history", response_model=HistoricalSentimentResponse)
async def get_historical_sentiment(
    ticker: str,
    days: int = Query(7, ge=1, le=30, description="Number of days of history")
):
    """
    Get historical sentiment data for a ticker
    
    Args:
        ticker: Stock ticker symbol
        days: Number of days of history to retrieve (1-30)
        
    Returns:
        Historical sentiment data with time series
    """
    try:
        ticker = ticker.upper()
        collection = await get_collection("sentiment_records")
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get records
        records = await collection.find({
            "ticker": ticker,
            "timestamp": {"$gte": start_date, "$lte": end_date}
        }).sort("timestamp", 1).to_list(length=10000)
        
        if not records:
            raise HTTPException(status_code=404, detail=f"No historical data for {ticker}")
        
        # Group by hour for aggregation
        hourly_data = {}
        for record in records:
            # Round to nearest hour
            hour_key = record['timestamp'].replace(minute=0, second=0, microsecond=0)
            
            if hour_key not in hourly_data:
                hourly_data[hour_key] = {
                    'compounds': [],
                    'post_count': 0
                }
            
            hourly_data[hour_key]['compounds'].append(record['sentiment']['compound'])
            hourly_data[hour_key]['post_count'] += 1
        
        # Create data points
        data_points = []
        for timestamp in sorted(hourly_data.keys()):
            data = hourly_data[timestamp]
            avg_sentiment = sum(data['compounds']) / len(data['compounds'])
            
            data_points.append({
                'timestamp': timestamp.isoformat(),
                'sentiment': avg_sentiment,
                'post_count': data['post_count']
            })
        
        return HistoricalSentimentResponse(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            data_points=data_points
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")
