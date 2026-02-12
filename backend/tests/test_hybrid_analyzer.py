# backend/tests/test_hybrid_analyzer.py
import pytest
from app.services.distilbert_analyzer import hybrid_analyzer

class TestHybridAnalyzer:
    """Test suite for hybrid analyzer (VADER + TextBlob + Patterns)"""
    
    def test_analyze_positive_text(self):
        """Test hybrid analysis on clearly positive text"""
        result = hybrid_analyzer.analyze("This is absolutely amazing and wonderful!")
        
        assert result["sentiment"] == "positive"
        assert result["model"] == "hybrid"
        assert result["emoji"] == "😊"
        assert "scores" in result
        assert result["scores"]["compound"] > 0
    
    def test_analyze_negative_text(self):
        """Test hybrid analysis on clearly negative text"""
        result = hybrid_analyzer.analyze("This is terrible, awful, and horrible")
        
        assert result["sentiment"] == "negative"
        assert result["model"] == "hybrid"
        assert result["emoji"] == "😞"
        assert result["scores"]["compound"] < 0
    
    def test_analyze_neutral_text(self):
        """Test hybrid analysis on neutral text"""
        result = hybrid_analyzer.analyze("The package arrived on schedule")
        
        assert result["model"] == "hybrid"
        assert result["emoji"] in ["😐", "😊", "😞"]
        assert "scores" in result
    
    def test_negation_handling(self):
        """Test that hybrid handles negations correctly"""
        result = hybrid_analyzer.analyze("not bad at all")
        
        # Should not be classified as negative
        assert result["sentiment"] != "negative"
        assert result["model"] == "hybrid"
    
    def test_sarcasm_detection(self):
        """Test hybrid on sarcastic text"""
        result = hybrid_analyzer.analyze("Oh great, another delay")
        
        assert result["model"] == "hybrid"
        assert "scores" in result
    
    def test_slang_handling(self):
        """Test hybrid on modern slang"""
        result = hybrid_analyzer.analyze("This movie absolutely slaps")
        
        assert result["model"] == "hybrid"
        assert result["sentiment"] in ["positive", "neutral"]
    
    def test_mixed_sentiment(self):
        """Test hybrid on mixed sentiment text"""
        result = hybrid_analyzer.analyze("The product is good but the service is bad")
        
        assert result["model"] == "hybrid"
        assert "scores" in result
        assert "positive" in result["scores"]
        assert "negative" in result["scores"]
    
    def test_empty_text(self):
        """Test hybrid analyzer with empty text"""
        result = hybrid_analyzer.analyze("")
        
        assert result["model"] == "hybrid"
        assert "scores" in result
    
    def test_very_long_text(self):
        """Test hybrid analyzer with very long text"""
        long_text = "This is great! " * 100
        result = hybrid_analyzer.analyze(long_text)
        
        assert result["model"] == "hybrid"
        assert result["sentiment"] == "positive"
    
    def test_special_characters(self):
        """Test hybrid analyzer with special characters"""
        result = hybrid_analyzer.analyze("Amazing!!! 😊😊😊 Love it!!!")
        
        assert result["model"] == "hybrid"
        assert "scores" in result