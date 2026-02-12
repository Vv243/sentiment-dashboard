# backend/tests/test_sentiment_analyzer.py
import pytest
from app.services.sentiment_analyzer import SentimentAnalyzer

class TestSentimentAnalyzer:
    """Test suite for sentiment analysis functionality"""
    
    def test_positive_sentiment_vader(self, sample_texts):
        """Test that clearly positive text is classified correctly (VADER)"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["positive"], model="vader")
        
        assert result is not None
        assert result["sentiment"] == "positive"
        assert result["emoji"] == "😊"
        assert result["scores"]["compound"] > 0.05
        assert result["model"] == "vader"
        assert result["moderation"]["flagged"] is False
    
    def test_negative_sentiment_vader(self, sample_texts):
        """Test that clearly negative text is classified correctly (VADER)"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["negative"], model="vader")
        
        assert result is not None
        assert result["sentiment"] == "negative"
        assert result["emoji"] == "😞"
        assert result["scores"]["compound"] < -0.05
        assert result["model"] == "vader"
    
    def test_neutral_sentiment_vader(self, sample_texts):
        """Test that neutral text is classified correctly (VADER)"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["neutral"], model="vader")
        
        assert result is not None
        assert result["sentiment"] == "neutral"
        assert result["emoji"] == "😐"
        assert -0.05 <= result["scores"]["compound"] <= 0.05
    
    def test_negation_handling_hybrid(self, sample_texts):
        """Test that 'not bad' is correctly interpreted with Hybrid model"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["negation"], model="distilbert")
        
        # "not bad" should NOT be classified as negative
        assert result["sentiment"] != "negative"
        assert result["model"] == "hybrid"
    
    def test_harmful_content_detection(self, sample_texts):
        """Test that content moderation system exists and has proper structure"""
        analyzer = SentimentAnalyzer()
    
        # Test that normal negative text is NOT flagged as harmful
        result = analyzer.analyze(sample_texts["negative"], model="vader")
    
        # Verify moderation structure exists
        assert "moderation" in result
        assert "flagged" in result["moderation"]
        assert "severity" in result["moderation"]
        assert "reason" in result["moderation"]
    
        # Normal negative text should not be flagged
        assert result["moderation"]["flagged"] is False
        assert result["moderation"]["severity"] == "safe"
        assert result["moderation"]["reason"] is None
    
        # Sentiment should be negative, NOT harmful
        assert result["sentiment"] == "negative"
        
    def test_model_selection_vader(self, sample_texts):
        """Test that VADER model is used when specified"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["positive"], model="vader")
        
        assert result["model"] == "vader"
    
    def test_model_selection_hybrid(self, sample_texts):
        """Test that Hybrid model is used when distilbert is specified"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["positive"], model="distilbert")
        
        assert result["model"] == "hybrid"
    
    def test_scores_structure(self, sample_texts):
        """Test that scores have correct structure"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["positive"], model="vader")
        
        assert "scores" in result
        assert "positive" in result["scores"]
        assert "negative" in result["scores"]
        assert "neutral" in result["scores"]
        assert "compound" in result["scores"]
        
        # Check that scores are floats
        assert isinstance(result["scores"]["positive"], float)
        assert isinstance(result["scores"]["compound"], float)
    
    def test_moderation_structure(self, sample_texts):
        """Test that moderation info has correct structure"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(sample_texts["positive"], model="vader")
        
        assert "moderation" in result
        assert "flagged" in result["moderation"]
        assert "reason" in result["moderation"]
        assert "severity" in result["moderation"]
    
    def test_empty_text_handling(self, sample_texts):
        """Test handling of empty text"""
        analyzer = SentimentAnalyzer()
        # Empty text should still return a result (VADER handles it)
        result = analyzer.analyze(sample_texts["empty"], model="vader")
        
        assert result is not None
        assert "sentiment" in result