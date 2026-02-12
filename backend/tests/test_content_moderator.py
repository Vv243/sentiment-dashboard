import pytest
from app.services.content_moderator import content_moderator

class TestContentModerator:
    """Test suite for content moderation"""
    
    def test_safe_content_not_flagged(self):
        """Test that normal content is not flagged"""
        result = content_moderator.check_content("This is a great product!")
        assert result["is_harmful"] is False
        assert result["severity"] == "safe"
    
    def test_harmful_content_structure(self):
        """Test that check_content returns correct structure"""
        result = content_moderator.check_content("test text")
        
        assert "is_harmful" in result
        assert "reason" in result
        assert "severity" in result
        assert isinstance(result["is_harmful"], bool)
    
    def test_empty_content_handling(self):
        """Test handling of empty content"""
        result = content_moderator.check_content("")
        assert result["is_harmful"] is False
    
    def test_moderation_severity_levels(self):
        """Test that severity levels are valid"""
        result = content_moderator.check_content("normal text")
        assert result["severity"] in ["safe", "low", "medium", "high", "critical"]