"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


# ============================================
# SENTIMENT ANALYSIS MODELS (NEW)
# ============================================

class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    text: str = Field(..., min_length=1, max_length=5000)
    model: str = Field(default="vader", pattern="^(vader|hybrid|gpt-4o-mini)$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I love this product!",
                "model": "vader"
            }
        }


class ModerationInfo(BaseModel):
    """Content moderation information"""
    flagged: bool
    reason: Optional[str] = None
    severity: str


class SentimentScores(BaseModel):
    """Sentiment scores"""
    positive: float
    negative: float
    neutral: float
    compound: float


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis"""
    text: str
    sentiment: str
    emoji: str
    scores: SentimentScores
    moderation: ModerationInfo
    timestamp: datetime
    saved_to_db: bool
    model: str
    confidence: Optional[float] = None


# ============================================
# STOCK SENTIMENT MODELS (EXISTING)
# ============================================

class SentimentLabel(str, Enum):
    """Sentiment labels"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class SentimentScore(BaseModel):
    """Sentiment score model"""
    compound: float = Field(..., ge=-1.0, le=1.0, description="Compound sentiment score")
    positive: float = Field(..., ge=0.0, le=1.0)
    negative: float = Field(..., ge=0.0, le=1.0)
    neutral: float = Field(..., ge=0.0, le=1.0)
    label: SentimentLabel


class TextAnalysisRequest(BaseModel):
    """Request model for analyzing text"""
    text: str = Field(..., min_length=1, max_length=5000)
    use_vader: bool = True
    use_finbert: bool = False


class TextAnalysisResponse(BaseModel):
    """Response model for text analysis"""
    text: str
    vader_score: Optional[SentimentScore] = None
    finbert_score: Optional[SentimentScore] = None
    combined_score: Optional[SentimentScore] = None
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


class SocialMediaPost(BaseModel):
    """Social media post model"""
    post_id: str
    ticker: str
    text: str
    source: str = Field(..., description="twitter or reddit")
    author: str
    created_at: datetime
    likes: int = 0
    retweets: int = 0
    comments: int = 0
    url: Optional[str] = None


class SentimentRecord(BaseModel):
    """Database model for sentiment records"""
    id: Optional[str] = Field(None, alias="_id")
    ticker: str
    post: SocialMediaPost
    sentiment: SentimentScore
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


class TickerSentimentSummary(BaseModel):
    """Summary of sentiment for a ticker"""
    ticker: str
    current_sentiment: SentimentScore
    total_posts: int
    positive_count: int
    negative_count: int
    neutral_count: int
    avg_compound: float
    last_updated: datetime


class HistoricalSentimentResponse(BaseModel):
    """Historical sentiment data"""
    ticker: str
    start_date: datetime
    end_date: datetime
    data_points: List[Dict]  # [{timestamp, sentiment, post_count}]


class CollectionRequest(BaseModel):
    """Request to start data collection"""
    ticker: str = Field(..., min_length=1, max_length=10)
    source: str = Field(..., description="twitter or reddit")
    keywords: Optional[List[str]] = None


class CollectionResponse(BaseModel):
    """Response for collection request"""
    ticker: str
    status: str
    message: str
    started_at: datetime = Field(default_factory=datetime.utcnow)


class TrendingTopic(BaseModel):
    """Trending topic/ticker"""
    ticker: str
    mention_count: int
    sentiment_score: float
    trending_since: datetime