"""
Data collection API endpoints with automatic fallback to synthetic data
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from datetime import datetime

from app.models.schemas import (
    CollectionRequest,
    CollectionResponse,
    TrendingTopic,
    SentimentRecord,
    SocialMediaPost
)
from app.services.reddit_collector import RedditCollector, get_reddit_collector
from app.services.twitter_collector import TwitterCollector, get_twitter_collector
from app.services.synthetic_data import SyntheticDataGenerator, get_synthetic_generator
from app.services.fallback_collector import FallbackCollector, get_fallback_collector
from app.services.sentiment_service import SentimentAnalyzer, get_sentiment_analyzer
from app.core.database import get_collection

router = APIRouter()


# Background task for data collection
async def collect_and_analyze(
    ticker: str,
    source: str,
    reddit_collector: RedditCollector,
    twitter_collector: TwitterCollector,
    analyzer: SentimentAnalyzer
):
    """
    Background task to collect posts and analyze sentiment
    """
    try:
        # Collect posts
        posts: List[SocialMediaPost] = []
        
        if source == "reddit":
            posts = reddit_collector.collect_posts(ticker=ticker, limit=100)
        elif source == "twitter":
            posts = twitter_collector.collect_posts(ticker=ticker, limit=100)
        else:
            return
        
        if not posts:
            print(f"No posts found for {ticker} from {source}")
            return
        
        # Analyze sentiment for each post
        collection = await get_collection("sentiment_records")
        
        for post in posts:
            # Analyze sentiment
            results = analyzer.analyze(text=post.text, use_vader=True, use_finbert=False)
            
            if results['combined_score']:
                # Create sentiment record
                record = SentimentRecord(
                    ticker=ticker.upper(),
                    post=post,
                    sentiment=results['combined_score'],
                    timestamp=datetime.utcnow()
                )
                
                # Insert into database
                await collection.insert_one(record.dict(by_alias=True, exclude={'id'}))
        
        print(f"✅ Analyzed {len(posts)} posts for {ticker} from {source}")
        
    except Exception as e:
        print(f"❌ Error in background collection: {e}")


@router.post("/start", response_model=CollectionResponse)
async def start_collection(
    request: CollectionRequest,
    background_tasks: BackgroundTasks,
    reddit_collector: RedditCollector = Depends(get_reddit_collector),
    twitter_collector: TwitterCollector = Depends(get_twitter_collector),
    analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Start data collection for a ticker
    
    Args:
        request: Collection request with ticker and source
        background_tasks: FastAPI background tasks
        
    Returns:
        Collection response with status
    """
    try:
        ticker = request.ticker.upper()
        source = request.source.lower()
        
        if source not in ["reddit", "twitter"]:
            raise HTTPException(status_code=400, detail="Source must be 'reddit' or 'twitter'")
        
        # Add background task
        background_tasks.add_task(
            collect_and_analyze,
            ticker=ticker,
            source=source,
            reddit_collector=reddit_collector,
            twitter_collector=twitter_collector,
            analyzer=analyzer
        )
        
        return CollectionResponse(
            ticker=ticker,
            status="started",
            message=f"Data collection started for {ticker} from {source}",
            started_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting collection: {str(e)}")


@router.post("/collect-now/{ticker}")
async def collect_now(
    ticker: str,
    source: str = "reddit",
    use_synthetic_fallback: bool = True,
    reddit_collector: RedditCollector = Depends(get_reddit_collector),
    twitter_collector: TwitterCollector = Depends(get_twitter_collector),
    synthetic_generator: SyntheticDataGenerator = Depends(get_synthetic_generator),
    analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Immediately collect and analyze data for a ticker (synchronous)
    
    Uses real API first, falls back to synthetic data if API fails or returns no results
    
    Args:
        ticker: Stock ticker symbol
        source: Data source preference (reddit or twitter)
        use_synthetic_fallback: Use synthetic data if real APIs fail (default: True)
        
    Returns:
        Collection summary with actual data source used
    """
    try:
        ticker = ticker.upper()
        
        # Create fallback collector
        fallback = FallbackCollector(reddit_collector, twitter_collector, synthetic_generator)
        
        # Collect posts with automatic fallback
        posts, actual_source = fallback.collect_with_smart_fallback(
            ticker=ticker,
            preferred_source=source,
            limit=50
        )
        
        if not posts:
            return {
                "ticker": ticker,
                "posts_collected": 0,
                "posts_analyzed": 0,
                "source": "none",
                "message": f"No data available for {ticker} (all sources failed)",
                "timestamp": datetime.utcnow()
            }
        
        # Analyze and save
        collection = await get_collection("sentiment_records")
        analyzed_count = 0
        
        for post in posts:
            results = analyzer.analyze(text=post.text, use_vader=True)
            
            if results['combined_score']:
                record = SentimentRecord(
                    ticker=ticker,
                    post=post,
                    sentiment=results['combined_score'],
                    timestamp=datetime.utcnow()
                )
                
                await collection.insert_one(record.dict(by_alias=True, exclude={'id'}))
                analyzed_count += 1
        
        # Include message if using synthetic data
        message = f"Successfully collected from {actual_source}"
        if actual_source == "synthetic":
            message += " (real APIs unavailable - using demo data for testing)"
        
        return {
            "ticker": ticker,
            "posts_collected": len(posts),
            "posts_analyzed": analyzed_count,
            "source": actual_source,
            "message": message,
            "timestamp": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Collection error: {str(e)}")


@router.get("/trending", response_model=List[TrendingTopic])
async def get_trending():
    """
    Get trending tickers based on mention count
    
    Returns:
        List of trending topics with sentiment
    """
    try:
        collection = await get_collection("sentiment_records")
        
        # Get records from last 24 hours
        from datetime import timedelta
        time_threshold = datetime.utcnow() - timedelta(hours=24)
        
        # Aggregate by ticker
        pipeline = [
            {"$match": {"timestamp": {"$gte": time_threshold}}},
            {
                "$group": {
                    "_id": "$ticker",
                    "count": {"$sum": 1},
                    "avg_sentiment": {"$avg": "$sentiment.compound"},
                    "first_seen": {"$min": "$timestamp"}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        results = await collection.aggregate(pipeline).to_list(length=10)
        
        trending = [
            TrendingTopic(
                ticker=r['_id'],
                mention_count=r['count'],
                sentiment_score=r['avg_sentiment'],
                trending_since=r['first_seen']
            )
            for r in results
        ]
        
        return trending
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting trending: {str(e)}")


@router.post("/generate-demo-data/{ticker}")
async def generate_demo_data(
    ticker: str,
    count: int = 100,
    scenario: str = "balanced",
    synthetic_generator: SyntheticDataGenerator = Depends(get_synthetic_generator),
    analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Generate synthetic demo data for testing and demonstrations
    
    Useful for:
    - Testing without API credentials
    - Consistent demo data for presentations
    - Simulating different market scenarios
    
    Args:
        ticker: Stock ticker symbol
        count: Number of posts to generate (10-500)
        scenario: Market scenario - 'balanced', 'bullish', 'bearish', 'volatile', 'stable'
        
    Returns:
        Generation summary
    """
    try:
        ticker = ticker.upper()
        count = max(10, min(count, 500))  # Limit between 10-500
        
        # Generate posts based on scenario
        if scenario in ['bullish', 'bearish', 'volatile', 'stable']:
            posts = synthetic_generator.generate_market_scenario(ticker, scenario)
        else:
            posts = synthetic_generator.generate_posts_for_ticker(ticker, count)
        
        # Analyze and save
        collection = await get_collection("sentiment_records")
        analyzed_count = 0
        
        for post in posts:
            results = analyzer.analyze(text=post.text, use_vader=True)
            
            if results['combined_score']:
                record = SentimentRecord(
                    ticker=ticker,
                    post=post,
                    sentiment=results['combined_score'],
                    timestamp=datetime.utcnow()
                )
                
                await collection.insert_one(record.dict(by_alias=True, exclude={'id'}))
                analyzed_count += 1
        
        return {
            "ticker": ticker,
            "posts_generated": len(posts),
            "posts_analyzed": analyzed_count,
            "scenario": scenario,
            "source": "synthetic",
            "message": f"Generated {len(posts)} synthetic posts for {ticker} ({scenario} scenario)",
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")
