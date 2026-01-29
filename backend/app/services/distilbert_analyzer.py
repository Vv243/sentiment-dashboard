"""
DistilBERT sentiment analyzer - more accurate than VADER.
Uses HuggingFace transformers for context-aware sentiment analysis.

NOTE: Disabled on servers with <1GB RAM to prevent timeouts.
"""
import logging
import psutil
import os

logger = logging.getLogger(__name__)

class DistilBERTAnalyzer:
    """
    Sentiment analyzer using DistilBERT transformer model.
    
    Automatically disabled on low-memory servers (< 1GB RAM).
    """
    
    def __init__(self):
        """Initialize DistilBERT analyzer"""
        self._model = None
        self._enabled = self._check_if_enabled()
        
        if self._enabled:
            logger.info("🤖 DistilBERT analyzer initialized (lazy loading)")
        else:
            logger.warning("⚠️ DistilBERT disabled (insufficient memory - need 1GB+)")
    
    def _check_if_enabled(self):
        """Check if we have enough memory to run DistilBERT"""
        try:
            import psutil
            total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)
            
            # Need at least 1GB to safely run DistilBERT
            if total_memory_gb < 1.0:
                logger.warning(f"⚠️ Only {total_memory_gb:.2f}GB RAM available, DistilBERT needs 1GB+")
                return False
            
            logger.info(f"✅ {total_memory_gb:.2f}GB RAM available, DistilBERT enabled")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Could not check memory: {e}, disabling DistilBERT")
            return False
    
    def _load_model(self):
        """Lazy load the model (only when first needed)"""
        if not self._enabled:
            return None
            
        if self._model is None:
            try:
                logger.info("📦 Loading DistilBERT model...")
                from transformers import pipeline
                
                self._model = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1
                )
                logger.info("✅ DistilBERT model loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load DistilBERT: {e}")
                self._enabled = False
                
        return self._model
    
    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment using DistilBERT or fallback to VADER.
        """
        logger.info(f"🤖 DistilBERT request: {text[:50]}...")
        
        # If DistilBERT is disabled, use VADER fallback immediately
        if not self._enabled:
            logger.info("⚠️ Using VADER fallback (DistilBERT unavailable)")
            return self._vader_fallback(text)
        
        # Try to load and use DistilBERT
        model = self._load_model()
        
        if model is None:
            logger.warning("⚠️ DistilBERT failed to load, using VADER fallback")
            return self._vader_fallback(text)
        
        try:
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
            
            logger.info(f"✅ DistilBERT: {sentiment} {emoji}")
            return response
            
        except Exception as e:
            logger.error(f"❌ DistilBERT error: {e}")
            return self._vader_fallback(text)
    
    def _vader_fallback(self, text: str) -> dict:
        """Fallback to VADER when DistilBERT unavailable"""
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
            'model': 'vader-fallback'
        }

# Global instance
distilbert_analyzer = DistilBERTAnalyzer()