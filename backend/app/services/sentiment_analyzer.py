"""
Sentiment analysis service using VADER.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Sentiment analyzer using VADER.
    
    VADER (Valence Aware Dictionary and sEntiment Reasoner) is specifically
    attuned to sentiments expressed in social media.
    """
    def __init__(self):
        """Initialize the VADER sentiment analyzer"""
        logger.info("🧠 Initializing VADER sentiment analyzer...")
        self.analyzer = SentimentIntensityAnalyzer()
        logger.info("✅ VADER initialized successfully")

    def analyze(self, text:str) -> dict:
        """
        Analyze sentiment of text.
        
        Args:
            text: The text to analyze
            
        Returns:
            dict with sentiment scores and classification
        """
        logger.info(f"📊 Analyzing text: {text[:50]}...")

        # Get VADER Scores
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
            'text' : text,
            'sentiment' : sentiment,
            'emoji': emoji,
            'scores': {
                'positive': round(scores['pos'], 3),
                'negative': round(scores['neg'], 3),
                'neutral': round(scores['neu'], 3),
                'compound': round(scores['compound'], 3)
            }
        }

        logger.info(f"✅ Sentiment: {sentiment} {emoji} (compound: {compound:.3f})")
        
        return result

# Create global instances
sentiment_analyzer = SentimentAnalyzer()