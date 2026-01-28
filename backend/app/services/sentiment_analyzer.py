"""
Sentiment analysis service with multiple models.
Supports VADER (fast) and DistilBERT (accurate).
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.services.content_moderator import content_moderator
from app.services.distilbert_analyzer import distilbert_analyzer
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Multi-model sentiment analyzer.
    - VADER: Fast, rule-based (good for simple text)
    - DistilBERT: Accurate, ML-based (better for complex text)
    """
    
    def __init__(self):
        """Initialize both VADER and DistilBERT"""
        logger.info("🧠 Initializing sentiment analyzers...")
        self.vader = SentimentIntensityAnalyzer()
        # DistilBERT loads lazily (only when needed)
        logger.info("✅ Sentiment analyzers ready")
    
    def analyze(self, text: str, model: str = "vader") -> dict:
        """
        Analyze sentiment with specified model.
        
        Args:
            text: Text to analyze
            model: "vader" (fast) or "distilbert" (accurate)
            
        Returns:
            dict with sentiment, scores, and moderation
        """
        logger.info(f"📊 Analyzing with {model}: {text[:50]}...")
        
        # Step 1: Check for harmful content first
        moderation = content_moderator.check_content(text)
        
        if moderation['is_harmful']:
            logger.warning("⚠️ Harmful content detected, overriding sentiment")
            return {
                'text': text,
                'sentiment': 'harmful',
                'emoji': '⚠️',
                'scores': {
                    'positive': 0.0,
                    'negative': 1.0,
                    'neutral': 0.0,
                    'compound': -0.99
                },
                'moderation': {
                    'flagged': True,
                    'reason': moderation['reason'],
                    'severity': moderation['severity']
                },
                'model': model
            }
        
        # Step 2: Choose model for sentiment analysis
        if model == "distilbert":
            result = self._analyze_with_distilbert(text)
        else:
            result = self._analyze_with_vader(text)
        
        # Add moderation info
        result['moderation'] = {
            'flagged': False,
            'reason': None,
            'severity': 'safe'
        }
        
        return result
    
    def _analyze_with_vader(self, text: str) -> dict:
        """Analyze with VADER (fast, rule-based)"""
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = 'positive'
            emoji = '😊'
        elif compound <= -0.05:
            sentiment = 'negative'
            emoji = '😞'
        else:
            sentiment = 'neutral'
            emoji = '😐'
        
        return {
            'text': text,
            'sentiment': sentiment,
            'emoji': emoji,
            'scores': {
                'positive': round(scores['pos'], 3),
                'negative': round(scores['neg'], 3),
                'neutral': round(scores['neu'], 3),
                'compound': round(scores['compound'], 3)
            },
            'model': 'vader'
        }
    
    def _analyze_with_distilbert(self, text: str) -> dict:
        """Analyze with DistilBERT (accurate, ML-based)"""
        return distilbert_analyzer.analyze(text)

# Global instance
sentiment_analyzer = SentimentAnalyzer()