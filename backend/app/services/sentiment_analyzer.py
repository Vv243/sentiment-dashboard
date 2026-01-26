"""
Sentiment analysis service using VADER with content moderation.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.services.content_moderator import content_moderator
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Sentiment analyzer using VADER with content moderation.
    
    VADER (Valence Aware Dictionary and sEntiment Reasoner) is specifically
    attuned to sentiments expressed in social media.
    
    Includes content moderation to detect harmful patterns that VADER might miss.
    """
    def __init__(self):
        """Initialize the VADER sentiment analyzer"""
        logger.info("🧠 Initializing VADER sentiment analyzer...")
        self.analyzer = SentimentIntensityAnalyzer()
        logger.info("✅ VADER initialized successfully")

    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of text with content moderation.
        
        Args:
            text: The text to analyze
            
        Returns:
            dict with sentiment scores, classification, and moderation flags
        """
        logger.info(f"📊 Analyzing text: {text[:50]}...")
        
        # Step 1: Check for harmful content first
        moderation_result = content_moderator.check_content(text)
        
        # Step 2: If harmful, override sentiment analysis
        if moderation_result['is_harmful']:
            logger.warning(f"⚠️ Harmful content detected, overriding sentiment")
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
                    'reason': moderation_result['reason'],
                    'severity': moderation_result['severity']
                }
            }

        # Step 3: Run VADER analysis for safe content
        scores = self.analyzer.polarity_scores(text)

        # Determine overall sentiment based on compound score
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

        result = {
            'text': text,
            'sentiment': sentiment,
            'emoji': emoji,
            'scores': {
                'positive': round(scores['pos'], 3),
                'negative': round(scores['neg'], 3),
                'neutral': round(scores['neu'], 3),
                'compound': round(scores['compound'], 3)
            },
            'moderation': {
                'flagged': False,
                'reason': None,
                'severity': 'safe'
            }
        }

        logger.info(f"✅ Sentiment: {sentiment} {emoji} (compound: {compound:.3f})")
        
        return result

# Create global instance
sentiment_analyzer = SentimentAnalyzer()