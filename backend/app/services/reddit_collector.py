"""
Reddit data collection service using PRAW
"""
import praw
from typing import List, Optional
from datetime import datetime
import logging

from app.core.config import settings
from app.models.schemas import SocialMediaPost

logger = logging.getLogger(__name__)


class RedditCollector:
    """Reddit data collector"""
    
    def __init__(self):
        """Initialize Reddit API client"""
        self.reddit = None
        
        if settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET:
            try:
                self.reddit = praw.Reddit(
                    client_id=settings.REDDIT_CLIENT_ID,
                    client_secret=settings.REDDIT_CLIENT_SECRET,
                    user_agent=settings.REDDIT_USER_AGENT
                )
                logger.info("✅ Reddit API client initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Reddit client: {e}")
    
    def collect_posts(
        self,
        ticker: str,
        subreddits: List[str] = None,
        limit: int = 100
    ) -> List[SocialMediaPost]:
        """
        Collect posts mentioning ticker from Reddit
        
        Args:
            ticker: Stock ticker symbol
            subreddits: List of subreddit names (default: wallstreetbets, stocks, investing)
            limit: Maximum number of posts to collect
            
        Returns:
            List of SocialMediaPost objects
        """
        if not self.reddit:
            logger.warning("Reddit client not initialized")
            return []
        
        if not subreddits:
            subreddits = ["wallstreetbets", "stocks", "investing"]
        
        posts = []
        
        try:
            for subreddit_name in subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Search for ticker mentions
                search_query = f"{ticker} OR ${ticker}"
                
                for submission in subreddit.search(
                    search_query,
                    time_filter="day",
                    limit=limit // len(subreddits)
                ):
                    # Create post object
                    post = SocialMediaPost(
                        post_id=submission.id,
                        ticker=ticker.upper(),
                        text=f"{submission.title} {submission.selftext}".strip(),
                        source="reddit",
                        author=str(submission.author) if submission.author else "deleted",
                        created_at=datetime.fromtimestamp(submission.created_utc),
                        likes=submission.score,
                        retweets=0,  # Reddit doesn't have retweets
                        comments=submission.num_comments,
                        url=f"https://reddit.com{submission.permalink}"
                    )
                    
                    posts.append(post)
                    
                    if len(posts) >= limit:
                        break
                
                if len(posts) >= limit:
                    break
            
            logger.info(f"Collected {len(posts)} posts from Reddit for {ticker}")
            
        except Exception as e:
            logger.error(f"Error collecting Reddit posts: {e}")
        
        return posts
    
    def get_hot_posts(self, subreddit_name: str = "wallstreetbets", limit: int = 50) -> List[SocialMediaPost]:
        """
        Get hot posts from a subreddit
        
        Args:
            subreddit_name: Name of subreddit
            limit: Number of posts to fetch
            
        Returns:
            List of SocialMediaPost objects
        """
        if not self.reddit:
            return []
        
        posts = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for submission in subreddit.hot(limit=limit):
                post = SocialMediaPost(
                    post_id=submission.id,
                    ticker="UNKNOWN",  # Will be extracted later
                    text=f"{submission.title} {submission.selftext}".strip(),
                    source="reddit",
                    author=str(submission.author) if submission.author else "deleted",
                    created_at=datetime.fromtimestamp(submission.created_utc),
                    likes=submission.score,
                    retweets=0,
                    comments=submission.num_comments,
                    url=f"https://reddit.com{submission.permalink}"
                )
                
                posts.append(post)
            
            logger.info(f"Collected {len(posts)} hot posts from r/{subreddit_name}")
            
        except Exception as e:
            logger.error(f"Error getting hot posts: {e}")
        
        return posts


# Global collector instance
reddit_collector = RedditCollector()


def get_reddit_collector() -> RedditCollector:
    """Dependency to get Reddit collector"""
    return reddit_collector
