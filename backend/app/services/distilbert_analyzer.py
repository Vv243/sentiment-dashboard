"""
DistilBERT sentiment analyzer - more accurate than VADER.
Uses HuggingFace transformers for context-aware sentiment analysis.
"""
import logging
import os

logger = logging.getLogger(__name__)

class DistilBERTAnalyzer:
    """
    Sentiment analyzer using DistilBERT transformer model.
    
    NOTE: Requires ~512MB RAM. May not work on free hosting tiers.
    Falls back to error message if model cannot be loaded.
    """
    
    def __init__(self):
        """Initialize DistilBERT model (loads on first use)"""
        self._model = None
        self._failed = False
        logger.info("🤖 DistilBERT analyzer initialized (lazy loading)")
    
    def _load_model(self):
        """Lazy load the model (only when first needed)"""
        if self._model is None and not self._failed:
            try:
                logger.info("📦 Loading DistilBERT model...")
                from transformers import pipeline
                
                self._model = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1  # Use CPU
                )
                logger.info("✅ DistilBERT model loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load DistilBERT: {e}")
                logger.error("⚠️ This usually means insufficient memory (need ~512MB)")
                self._failed = True
                
        return self._model
    
    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment using DistilBERT.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with sentiment, emoji, scores, confidence
        """
        logger.info(f"🤖 Analyzing with DistilBERT: {text[:50]}...")
        
        # Try to load model
        model = self._load_model()
        
        # If model failed to load, return fallback VADER-style response
        if model is None:
            logger.warning("⚠️ DistilBERT unavailable, using fallback")
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            vader = SentimentIntensityAnalyzer()
            scores = vader.polarity_scores(text)
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
                'confidence': None,
                'model': 'vader-fallback',  # Indicate fallback
                'note': 'DistilBERT unavailable (insufficient memory)'
            }
        
        try:
            # Get prediction from DistilBERT
            result = model(text[:512])[0]
            
            label = result['label']
            confidence = result['score']
            
            if label == 'POSITIVE':
                sentiment = 'positive'
                emoji = '😊'
                positive_score = confidence
                negative_score = 1 - confidence
            else:
                sentiment = 'negative'
                emoji = '😞'
                positive_score = 1 - confidence
                negative_score = confidence
            
            neutral_score = 1 - confidence
            
            total = positive_score + negative_score + neutral_score
            positive_score /= total
            negative_score /= total
            neutral_score /= total
            
            compound = (positive_score - negative_score)
            
            response = {
                'text': text,
                'sentiment': sentiment,
                'emoji': emoji,
                'scores': {
                    'positive': round(positive_score, 3),
                    'negative': round(negative_score, 3),
                    'neutral': round(neutral_score, 3),
                    'compound': round(compound, 3)
                },
                'confidence': round(confidence, 3),
                'model': 'distilbert'
            }
            
            logger.info(f"✅ DistilBERT: {sentiment} {emoji} (confidence: {confidence:.3f})")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ DistilBERT error: {e}")
            return {
                'error': str(e),
                'sentiment': 'error',
                'emoji': '⚠️',
                'model': 'error'
            }

# Global instance
distilbert_analyzer = DistilBERTAnalyzer()