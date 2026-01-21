"""
Synthetic Data Generator - Backup for Social Media API Issues

This module generates realistic synthetic social media posts for testing and demo purposes.
Use this when:
- Reddit/Twitter APIs are unavailable
- Rate limits are hit
- You need consistent demo data
- API credentials are not yet set up
"""

import random
from datetime import datetime, timedelta
from typing import List
import string

from app.models.schemas import SocialMediaPost


class SyntheticDataGenerator:
    """Generate synthetic social media posts for testing"""
    
    # Realistic post templates by sentiment
    POSITIVE_TEMPLATES = [
        "{ticker} is going to the moon! 🚀🚀🚀",
        "Just bought more {ticker}! This is the way! 💎🙌",
        "{ticker} earnings report was amazing! Bullish!",
        "Love the direction {ticker} is heading. Strong buy!",
        "{ticker} just announced great news! To the moon!",
        "Holding {ticker} long term. Best investment ever!",
        "{ticker} is undervalued. Get in while you can!",
        "Warren Buffett would love {ticker} at this price",
        "{ticker} fundamentals are solid. Very bullish 📈",
        "Just tripled my position in {ticker}. Let's go!",
        "{ticker} is the future! Can't wait for next quarter",
        "Best decision was buying {ticker} last month 🔥",
        "{ticker} management is killing it! Impressive!",
        "Technical analysis shows {ticker} ready to breakout 📊",
        "{ticker} products are game changers. All in! 💪"
    ]
    
    NEGATIVE_TEMPLATES = [
        "{ticker} is overvalued. Time to sell.",
        "Not feeling good about {ticker} anymore. Sold all shares.",
        "{ticker} earnings disappointed. Bearish trend ahead.",
        "Why is {ticker} dropping so much? Should I panic sell?",
        "{ticker} fundamentals are weak. Stay away!",
        "Just cut my losses on {ticker}. Terrible investment.",
        "{ticker} management has no idea what they're doing",
        "Avoid {ticker} at all costs. Red flags everywhere 🚩",
        "{ticker} is heading for a crash. Mark my words.",
        "Sold all my {ticker}. Too much risk. 📉",
        "{ticker} competition is killing them. Not good.",
        "Bad news for {ticker} holders. Get out while you can!",
        "Disappointed with {ticker} performance. Bearish.",
        "{ticker} valuations make no sense. Bubble territory.",
        "Technical indicators show {ticker} about to tank 📊"
    ]
    
    NEUTRAL_TEMPLATES = [
        "Thoughts on {ticker}? Considering buying some shares.",
        "{ticker} moved sideways today. What's everyone's take?",
        "Anyone have analysis on {ticker}? Doing research.",
        "What's the outlook for {ticker} this quarter?",
        "{ticker} volume seems normal today. Nothing special.",
        "Watching {ticker} closely. Waiting for entry point.",
        "Mixed feelings about {ticker}. Need more data.",
        "What do you all think about {ticker} valuation?",
        "{ticker} announcement was okay. Nothing groundbreaking.",
        "Holding {ticker} for now. Let's see what happens.",
        "Is anyone else tracking {ticker}? Thoughts?",
        "{ticker} seems fairly valued at current levels.",
        "Neutral on {ticker} until we see next earnings.",
        "Need more information before investing in {ticker}.",
        "{ticker} could go either way. Playing it safe."
    ]
    
    # Realistic usernames
    USERNAME_PREFIXES = [
        "Bull", "Bear", "Trader", "Investor", "Hodler", "Diamond", "Paper",
        "Retail", "Whale", "Ape", "Moon", "Rocket", "Stock", "Chart",
        "Market", "Value", "Growth", "Momentum", "Long", "Short"
    ]
    
    USERNAME_SUFFIXES = [
        "King", "Queen", "Lord", "Master", "Hunter", "Seeker", "Warrior",
        "Legend", "Pro", "Guru", "Wizard", "Ninja", "Expert", "Analyst",
        "Fanatic", "Addict", "Lover", "Hater", "Believer", "Skeptic"
    ]
    
    def __init__(self, seed: int = None):
        """Initialize generator with optional seed for reproducibility"""
        if seed:
            random.seed(seed)
    
    def _generate_username(self) -> str:
        """Generate a realistic Reddit-style username"""
        prefix = random.choice(self.USERNAME_PREFIXES)
        suffix = random.choice(self.USERNAME_SUFFIXES)
        number = random.randint(1, 9999)
        return f"{prefix}{suffix}{number}"
    
    def _generate_post_id(self) -> str:
        """Generate a unique post ID"""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=8))
    
    def generate_post(
        self,
        ticker: str,
        sentiment: str = None,
        days_ago: int = 0
    ) -> SocialMediaPost:
        """
        Generate a single synthetic post
        
        Args:
            ticker: Stock ticker symbol
            sentiment: 'positive', 'negative', or 'neutral' (random if None)
            days_ago: How many days ago the post was created (0 = today)
            
        Returns:
            SocialMediaPost object
        """
        # Choose sentiment if not specified
        if sentiment is None:
            sentiment = random.choice(['positive', 'negative', 'neutral'])
        
        # Select template based on sentiment
        if sentiment == 'positive':
            templates = self.POSITIVE_TEMPLATES
        elif sentiment == 'negative':
            templates = self.NEGATIVE_TEMPLATES
        else:
            templates = self.NEUTRAL_TEMPLATES
        
        text = random.choice(templates).format(ticker=ticker)
        
        # Generate timestamp
        created_at = datetime.utcnow() - timedelta(
            days=days_ago,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Generate engagement metrics (more for positive posts)
        base_engagement = 100 if sentiment == 'positive' else (
            30 if sentiment == 'negative' else 50
        )
        
        post = SocialMediaPost(
            post_id=self._generate_post_id(),
            ticker=ticker.upper(),
            text=text,
            source="synthetic",  # Mark as synthetic
            author=self._generate_username(),
            created_at=created_at,
            likes=random.randint(base_engagement // 2, base_engagement * 3),
            retweets=random.randint(base_engagement // 4, base_engagement),
            comments=random.randint(base_engagement // 10, base_engagement // 2),
            url=f"https://synthetic.example.com/post/{self._generate_post_id()}"
        )
        
        return post
    
    def generate_posts_for_ticker(
        self,
        ticker: str,
        count: int = 100,
        days_back: int = 7,
        sentiment_distribution: dict = None
    ) -> List[SocialMediaPost]:
        """
        Generate multiple posts for a ticker with realistic distribution
        
        Args:
            ticker: Stock ticker symbol
            count: Number of posts to generate
            days_back: Generate posts spread over this many days
            sentiment_distribution: Dict like {'positive': 0.4, 'negative': 0.3, 'neutral': 0.3}
                                   Defaults to balanced distribution
            
        Returns:
            List of SocialMediaPost objects
        """
        if sentiment_distribution is None:
            # Default balanced distribution
            sentiment_distribution = {
                'positive': 0.35,
                'negative': 0.35,
                'neutral': 0.30
            }
        
        posts = []
        
        # Calculate counts for each sentiment
        positive_count = int(count * sentiment_distribution.get('positive', 0.33))
        negative_count = int(count * sentiment_distribution.get('negative', 0.33))
        neutral_count = count - positive_count - negative_count
        
        # Generate posts
        for sentiment, sentiment_count in [
            ('positive', positive_count),
            ('negative', negative_count),
            ('neutral', neutral_count)
        ]:
            for _ in range(sentiment_count):
                days_ago = random.randint(0, days_back)
                post = self.generate_post(ticker, sentiment, days_ago)
                posts.append(post)
        
        # Shuffle to mix sentiments
        random.shuffle(posts)
        
        return posts
    
    def generate_trending_tickers(
        self,
        tickers: List[str] = None,
        count: int = 5
    ) -> List[tuple]:
        """
        Generate trending ticker data
        
        Args:
            tickers: List of ticker symbols (uses popular tickers if None)
            count: Number of trending tickers to return
            
        Returns:
            List of (ticker, post_count) tuples
        """
        if tickers is None:
            tickers = ['TSLA', 'AAPL', 'GME', 'AMC', 'NVDA', 'AMD', 
                      'MSFT', 'GOOGL', 'AMZN', 'META']
        
        # Generate realistic trending counts
        trending = []
        for ticker in random.sample(tickers, min(count, len(tickers))):
            post_count = random.randint(50, 500)
            trending.append((ticker, post_count))
        
        # Sort by post count
        trending.sort(key=lambda x: x[1], reverse=True)
        
        return trending
    
    def generate_market_scenario(
        self,
        ticker: str,
        scenario: str = "bullish"
    ) -> List[SocialMediaPost]:
        """
        Generate posts for specific market scenarios
        
        Args:
            ticker: Stock ticker symbol
            scenario: 'bullish', 'bearish', 'volatile', or 'stable'
            
        Returns:
            List of posts reflecting the scenario
        """
        scenarios = {
            'bullish': {'positive': 0.7, 'negative': 0.1, 'neutral': 0.2},
            'bearish': {'positive': 0.1, 'negative': 0.7, 'neutral': 0.2},
            'volatile': {'positive': 0.4, 'negative': 0.4, 'neutral': 0.2},
            'stable': {'positive': 0.3, 'negative': 0.3, 'neutral': 0.4}
        }
        
        distribution = scenarios.get(scenario, scenarios['stable'])
        
        return self.generate_posts_for_ticker(
            ticker=ticker,
            count=100,
            days_back=1,  # Recent activity
            sentiment_distribution=distribution
        )


# Global instance
synthetic_generator = SyntheticDataGenerator()


def get_synthetic_generator() -> SyntheticDataGenerator:
    """Dependency to get synthetic data generator"""
    return synthetic_generator
