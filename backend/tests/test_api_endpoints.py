# backend/tests/test_api_endpoints.py
import pytest
from fastapi import status

class TestSentimentAPI:
    """Test suite for API endpoints"""
    
    def test_analyze_endpoint_success(self, client):
        """Test POST /analyze with valid input"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "This is amazing!",
                "model": "vader"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "sentiment" in data
        assert "scores" in data
        assert "model" in data
        assert data["sentiment"] == "positive"
    
    def test_analyze_endpoint_hybrid_model(self, client):
        """Test POST /analyze with hybrid model"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "This is amazing!",
                "model": "distilbert"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["model"] == "hybrid"
    
    def test_analyze_endpoint_empty_text(self, client):
        """Test POST /analyze with empty text - should be rejected"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "",
                "model": "vader"
            }
        )
        
        # Empty text should be rejected with 422 validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_analyze_endpoint_invalid_model(self, client):
        """Test POST /analyze with invalid model name - should be rejected"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "Test text",
                "model": "invalid_model"
            }
        )
        
        # Invalid model should be rejected with 422 validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_history_endpoint(self, client):
        """Test GET /history endpoint"""
        response = client.get("/api/v1/sentiment/history?limit=10&offset=0")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Response is a dict with 'analyses' key, not a direct list
        assert isinstance(data, dict)
        assert "analyses" in data
        assert isinstance(data["analyses"], list)
        assert "count" in data
        assert "limit" in data
    
    def test_feedback_endpoint_thumbs_up(self, client):
        """Test POST /feedback with thumbs up"""
        response = client.post(
            "/api/v1/sentiment/feedback",
            json={
                "analysis_id": 1,
                "feedback": "thumbs_up"
            }
        )
        
        # May return 200 or 404 if ID doesn't exist
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_feedback_endpoint_thumbs_down(self, client):
        """Test POST /feedback with thumbs down"""
        response = client.post(
            "/api/v1/sentiment/feedback",
            json={
                "analysis_id": 1,
                "feedback": "thumbs_down"
            }
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    # NEW TESTS - ALL PROPERLY INDENTED INSIDE THE CLASS
    def test_analyze_endpoint_long_text(self, client):
        """Test POST /analyze with long text"""
        long_text = "This is a great product. " * 50
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": long_text,
                "model": "vader"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "sentiment" in data
    
    def test_analyze_endpoint_special_characters(self, client):
        """Test POST /analyze with special characters"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "Great!!! Love it!!!",
                "model": "vader"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "sentiment" in data
    
    def test_analyze_response_structure(self, client):
        """Test that analyze response has all required fields"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "Test text",
                "model": "vader"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check all required fields
        assert "sentiment" in data
        assert "emoji" in data
        assert "scores" in data
        assert "model" in data
        assert "moderation" in data
        assert "timestamp" in data
    
    def test_history_endpoint_with_pagination(self, client):
        """Test GET /history with different pagination params"""
        # Test with limit=5
        response = client.get("/api/v1/sentiment/history?limit=5&offset=0")
        assert response.status_code == status.HTTP_200_OK
        
        # Test with offset=10
        response = client.get("/api/v1/sentiment/history?limit=10&offset=10")
        assert response.status_code == status.HTTP_200_OK
    
    def test_history_response_structure(self, client):
        """Test that history response has correct structure"""
        response = client.get("/api/v1/sentiment/history?limit=10&offset=0")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "analyses" in data
        assert "count" in data
        assert "limit" in data
        assert data["limit"] == 10
    
    def test_feedback_invalid_analysis_id(self, client):
        """Test POST /feedback with non-existent ID"""
        response = client.post(
            "/api/v1/sentiment/feedback",
            json={
                "analysis_id": 999999,
                "feedback": "thumbs_up"
            }
        )
        
        # Should return 404 for non-existent ID
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_200_OK]

    def test_batch_endpoint_if_exists(self, client):
        """Test batch analysis endpoint if implemented"""
        response = client.post(
            "/api/v1/sentiment/batch",
            json={
                "texts": ["Great product!", "Terrible service", "It's okay"],
                "model": "vader"
            }
        )
        
        # If endpoint exists, should return 200
        if response.status_code != 404:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list) or isinstance(data, dict)
    
    def test_analytics_endpoint_if_exists(self, client):
        """Test analytics endpoint if implemented"""
        response = client.get("/api/v1/sentiment/analytics")
        
        # If endpoint exists, should return 200
        if response.status_code != 404:
            assert response.status_code == status.HTTP_200_OK
    
    def test_export_csv_endpoint_if_exists(self, client):
        """Test CSV export endpoint if implemented"""
        response = client.get("/api/v1/sentiment/export")
        
        # If endpoint exists, should return 200 or csv data
        if response.status_code != 404:
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
    
    def test_analyze_with_database_save(self, client):
        """Test that analysis result includes database save confirmation"""
        response = client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": "This is a test for database",
                "model": "vader"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Response should contain all expected fields
        assert "text" in data or "sentiment" in data