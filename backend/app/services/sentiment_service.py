"""
Sentiment analysis service using VADER and FinBERT
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Optional
import logging

from app.models.schemas import SentimentScore, SentimentLabel
from app.core.config import settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Sentiment analyzer using multiple models"""
    
    def __init__(self):
        """Initialize sentiment analyzers"""
        self.vader = None
        self.finbert_model = None
        self.finbert_tokenizer = None
        
        # Initialize VADER
        if settings.USE_VADER:
            self.vader = SentimentIntensityAnalyzer()
            logger.info("✅ VADER sentiment analyzer initialized")
        
        # Initialize FinBERT (only if enabled and has GPU)
        if settings.USE_FINBERT:
            try:
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
                import torch
                
                self.finbert_tokenizer = AutoTokenizer.from_pretrained(settings.FINBERT_MODEL)
                self.finbert_model = AutoModelForSequenceClassification.from_pretrained(settings.FINBERT_MODEL)
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self.finbert_model = self.finbert_model.cuda()
                
                logger.info("✅ FinBERT sentiment analyzer initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize FinBERT: {e}")
                self.finbert_model = None
    
    def analyze_vader(self, text: str) -> Optional[SentimentScore]:
        """
        Analyze sentiment using VADER
        
        Args:
            text: Text to analyze
            
        Returns:
            SentimentScore or None if VADER not available
        """
        if not self.vader:
            return None
        
        try:
            scores = self.vader.polarity_scores(text)
            
            # Determine label based on compound score
            compound = scores['compound']
            if compound >= 0.05:
                label = SentimentLabel.POSITIVE
            elif compound <= -0.05:
                label = SentimentLabel.NEGATIVE
            else:
                label = SentimentLabel.NEUTRAL
            
            return SentimentScore(
                compound=compound,
                positive=scores['pos'],
                negative=scores['neg'],
                neutral=scores['neu'],
                label=label
            )
        except Exception as e:
            logger.error(f"VADER analysis error: {e}")
            return None
    
    def analyze_finbert(self, text: str) -> Optional[SentimentScore]:
        """
        Analyze sentiment using FinBERT
        
        Args:
            text: Text to analyze
            
        Returns:
            SentimentScore or None if FinBERT not available
        """
        if not self.finbert_model or not self.finbert_tokenizer:
            return None
        
        try:
            import torch
            
            # Tokenize
            inputs = self.finbert_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.finbert_model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # FinBERT outputs: [negative, neutral, positive]
            scores = predictions[0].cpu().numpy()
            
            # Determine label
            label_idx = scores.argmax()
            labels_map = {0: SentimentLabel.NEGATIVE, 1: SentimentLabel.NEUTRAL, 2: SentimentLabel.POSITIVE}
            label = labels_map[label_idx]
            
            # Calculate compound score (-1 to 1)
            compound = float(scores[2] - scores[0])  # positive - negative
            
            return SentimentScore(
                compound=compound,
                positive=float(scores[2]),
                negative=float(scores[0]),
                neutral=float(scores[1]),
                label=label
            )
        except Exception as e:
            logger.error(f"FinBERT analysis error: {e}")
            return None
    
    def analyze(self, text: str, use_vader: bool = True, use_finbert: bool = False) -> dict:
        """
        Analyze text using requested models
        
        Args:
            text: Text to analyze
            use_vader: Whether to use VADER
            use_finbert: Whether to use FinBERT
            
        Returns:
            Dictionary with vader_score, finbert_score, and combined_score
        """
        results = {
            'vader_score': None,
            'finbert_score': None,
            'combined_score': None
        }
        
        # VADER analysis
        if use_vader and self.vader:
            results['vader_score'] = self.analyze_vader(text)
        
        # FinBERT analysis
        if use_finbert and self.finbert_model:
            results['finbert_score'] = self.analyze_finbert(text)
        
        # Combined score (average of available scores)
        available_scores = [s for s in [results['vader_score'], results['finbert_score']] if s]
        
        if available_scores:
            avg_compound = sum(s.compound for s in available_scores) / len(available_scores)
            avg_positive = sum(s.positive for s in available_scores) / len(available_scores)
            avg_negative = sum(s.negative for s in available_scores) / len(available_scores)
            avg_neutral = sum(s.neutral for s in available_scores) / len(available_scores)
            
            # Determine combined label
            if avg_compound >= 0.05:
                label = SentimentLabel.POSITIVE
            elif avg_compound <= -0.05:
                label = SentimentLabel.NEGATIVE
            else:
                label = SentimentLabel.NEUTRAL
            
            results['combined_score'] = SentimentScore(
                compound=avg_compound,
                positive=avg_positive,
                negative=avg_negative,
                neutral=avg_neutral,
                label=label
            )
        
        return results


# Global analyzer instance
sentiment_analyzer = SentimentAnalyzer()


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Dependency to get sentiment analyzer"""
    return sentiment_analyzer
