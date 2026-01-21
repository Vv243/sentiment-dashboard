"""
Twitter data collection service using Tweepy
"""
import tweepy
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.core.config import settings
from app.models.schemas import SocialMediaPost

logger = logging.getLogger(__name__)


class TwitterCollector:
    """Twitter data collector"""
    
    def __init__(self):
        """Initialize Twitter API client"""
        self.client = None
        
        # Try to initialize with API credentials
        if settings.TWITTER_BEARER_TOKEN:
            try:
                self.client = tweepy.Client(
                    bearer_token=settings.TWITTER_BEARER_TOKEN,
                    wait_on_rate_limit=True
                )
                logger.info("✅ Twitter API client initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Twitter client: {e}")
    
    def collect_posts(
        self,
        ticker: str,
        limit: int = 100
    ) -> List[SocialMediaPost]:
        """
        Collect tweets mentioning ticker
        
        Args:
            ticker: Stock ticker symbol (e.g., TSLA, AAPL)
            limit: Maximum number of tweets to collect
            
        Returns:
            List of SocialMediaPost objects
        """
        if not self.client:
            logger.warning("Twitter client not initialized")
            return []
        
        posts = []
        
        try:
            # Search query
            query = f"${ticker} OR #{ticker} -is:retweet lang:en"
            
            # Get tweets from last 7 days (Twitter API limitation for free tier)
            start_time = datetime.utcnow() - timedelta(days=7)
            
            # Search recent tweets
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(limit, 100),  # API limit
                start_time=start_time,
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username']
            )
            
            if not response.data:
                logger.info(f"No tweets found for {ticker}")
                return []
            
            # Create user lookup
            users = {user.id: user.username for user in response.includes.get('users', [])}
            
            # Process tweets
            for tweet in response.data:
                metrics = tweet.public_metrics
                
                post = SocialMediaPost(
                    post_id=tweet.id,
                    ticker=ticker.upper(),
                    text=tweet.text,
                    source="twitter",
                    author=users.get(tweet.author_id, "unknown"),
                    created_at=tweet.created_at,
                    likes=metrics.get('like_count', 0),
                    retweets=metrics.get('retweet_count', 0),
                    comments=metrics.get('reply_count', 0),
                    url=f"https://twitter.com/user/status/{tweet.id}"
                )
                
                posts.append(post)
            
            logger.info(f"Collected {len(posts)} tweets for {ticker}")
            
        except tweepy.TweepyException as e:
            logger.error(f"Twitter API error: {e}")
        except Exception as e:
            logger.error(f"Error collecting tweets: {e}")
        
        return posts
    
    def collect_trending(self, location_id: int = 1) -> List[str]:
        """
        Get trending topics (Note: Requires elevated access)
        
        Args:
            location_id: WOEID location (1 = worldwide)
            
        Returns:
            List of trending topics
        """
        # This requires elevated API access
        # For now, return empty list
        logger.warning("Trending topics require elevated Twitter API access")
        return []


# Global collector instance
twitter_collector = TwitterCollector()


def get_twitter_collector() -> TwitterCollector:
    """Dependency to get Twitter collector"""
    return twitter_collector
