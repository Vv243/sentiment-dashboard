"""
Fallback Data Collector - Automatically uses synthetic data when APIs fail

This service attempts to use real APIs first, then falls back to synthetic data
"""

import logging
from typing import List, Optional

from app.models.schemas import SocialMediaPost
from app.services.reddit_collector import RedditCollector
from app.services.twitter_collector import TwitterCollector
from app.services.synthetic_data import SyntheticDataGenerator

logger = logging.getLogger(__name__)


class FallbackCollector:
    """
    Collector that tries real APIs first, falls back to synthetic data
    """
    
    def __init__(
        self,
        reddit_collector: RedditCollector,
        twitter_collector: TwitterCollector,
        synthetic_generator: SyntheticDataGenerator
    ):
        self.reddit = reddit_collector
        self.twitter = twitter_collector
        self.synthetic = synthetic_generator
    
    def collect_posts(
        self,
        ticker: str,
        source: str = "reddit",
        limit: int = 100,
        use_synthetic_fallback: bool = True
    ) -> tuple[List[SocialMediaPost], str]:
        """
        Collect posts with automatic fallback
        
        Args:
            ticker: Stock ticker symbol
            source: 'reddit' or 'twitter'
            limit: Number of posts to collect
            use_synthetic_fallback: Whether to use synthetic data if APIs fail
            
        Returns:
            Tuple of (posts_list, data_source)
            data_source will be 'reddit', 'twitter', or 'synthetic'
        """
        posts = []
        
        # Try real API first
        try:
            if source == "reddit":
                logger.info(f"Attempting to collect from Reddit for {ticker}...")
                posts = self.reddit.collect_posts(ticker=ticker, limit=limit)
                
                if posts:
                    logger.info(f"✅ Successfully collected {len(posts)} posts from Reddit")
                    return posts, "reddit"
                else:
                    logger.warning(f"⚠️ Reddit returned no posts for {ticker}")
            
            elif source == "twitter":
                logger.info(f"Attempting to collect from Twitter for {ticker}...")
                posts = self.twitter.collect_posts(ticker=ticker, limit=limit)
                
                if posts:
                    logger.info(f"✅ Successfully collected {len(posts)} posts from Twitter")
                    return posts, "twitter"
                else:
                    logger.warning(f"⚠️ Twitter returned no posts for {ticker}")
        
        except Exception as e:
            logger.error(f"❌ {source.capitalize()} API error: {e}")
        
        # Fallback to synthetic data
        if use_synthetic_fallback:
            logger.info(f"📊 Using synthetic data for {ticker} (API unavailable or no results)")
            
            # Generate realistic distribution based on ticker popularity
            posts = self.synthetic.generate_posts_for_ticker(
                ticker=ticker,
                count=limit,
                days_back=7
            )
            
            logger.info(f"✅ Generated {len(posts)} synthetic posts for {ticker}")
            return posts, "synthetic"
        
        return [], "none"
    
    def collect_with_smart_fallback(
        self,
        ticker: str,
        preferred_source: str = "reddit",
        limit: int = 100
    ) -> tuple[List[SocialMediaPost], str]:
        """
        Try multiple sources intelligently
        
        Order: preferred_source → other_source → synthetic
        
        Returns:
            Tuple of (posts_list, actual_source_used)
        """
        # Try preferred source
        posts, source = self.collect_posts(
            ticker=ticker,
            source=preferred_source,
            limit=limit,
            use_synthetic_fallback=False
        )
        
        if posts:
            return posts, source
        
        # Try alternative source
        alternative = "twitter" if preferred_source == "reddit" else "reddit"
        logger.info(f"Trying alternative source: {alternative}")
        
        posts, source = self.collect_posts(
            ticker=ticker,
            source=alternative,
            limit=limit,
            use_synthetic_fallback=False
        )
        
        if posts:
            return posts, source
        
        # Fall back to synthetic
        logger.info("All real sources failed, using synthetic data")
        posts = self.synthetic.generate_posts_for_ticker(
            ticker=ticker,
            count=limit,
            days_back=7
        )
        
        return posts, "synthetic"


def get_fallback_collector(
    reddit_collector: RedditCollector,
    twitter_collector: TwitterCollector,
    synthetic_generator: SyntheticDataGenerator
) -> FallbackCollector:
    """Create fallback collector instance"""
    return FallbackCollector(reddit_collector, twitter_collector, synthetic_generator)
