"""
DistilBERT sentiment analyzer - more accurate than VADER.
Uses HuggingFace transformers for context-aware sentiment analysis.
"""
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class DistilBERTAnalyzer:
    """
    Sentiment analyzer using DistilBERT transformer model.
    More accurate than VADER, especially for:
    - Sarcasm detection
    - Negation handling
    - Slang and informal language
    - Context understanding
    """
    
    def __init__(self):
        """Initialize DistilBERT model (loads on first use)"""
        self._model = None
        logger.info("🤖 DistilBERT analyzer initialized (lazy loading)")
    
    def _load_model(self):
        """Lazy load the model (only when first needed)"""
        if self._model is None:
            logger.info("📦 Loading DistilBERT model...")
            self._model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU (Render doesn't have GPU)
            )
            logger.info("✅ DistilBERT model loaded successfully")
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
        
        try:
            # Load model if not already loaded
            model = self._load_model()
            
            # Get prediction
            result = model(text[:512])[0]  # DistilBERT max length: 512 tokens
            
            # Extract label and confidence
            label = result['label']  # 'POSITIVE' or 'NEGATIVE'
            confidence = result['score']  # 0.0 to 1.0
            
            # Map to our format
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
            
            # Calculate neutral (middle ground)
            # If confidence is low, it's more neutral
            neutral_score = 1 - confidence
            
            # Normalize scores to sum to 1.0
            total = positive_score + negative_score + neutral_score
            positive_score /= total
            negative_score /= total
            neutral_score /= total
            
            # Calculate compound score (-1 to 1)
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
            # Fallback to error response
            return {
                'error': str(e),
                'sentiment': 'error',
                'emoji': '⚠️'
            }

# Global instance
distilbert_analyzer = DistilBERTAnalyzer()