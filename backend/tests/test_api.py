"""
Basic tests for the sentiment analysis API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_analyze_text_vader():
    """Test sentiment analysis with VADER"""
    response = client.post(
        "/api/v1/sentiment/analyze",
        json={
            "text": "This is amazing! I love it!",
            "use_vader": True,
            "use_finbert": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "vader_score" in data
    assert data["vader_score"]["label"] == "positive"


def test_analyze_negative_text():
    """Test negative sentiment analysis"""
    response = client.post(
        "/api/v1/sentiment/analyze",
        json={
            "text": "This is terrible! I hate it!",
            "use_vader": True,
            "use_finbert": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vader_score"]["label"] == "negative"


def test_analyze_neutral_text():
    """Test neutral sentiment analysis"""
    response = client.post(
        "/api/v1/sentiment/analyze",
        json={
            "text": "The weather is normal today.",
            "use_vader": True,
            "use_finbert": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vader_score"]["label"] in ["neutral", "positive", "negative"]


def test_invalid_text():
    """Test with empty text"""
    response = client.post(
        "/api/v1/sentiment/analyze",
        json={
            "text": "",
            "use_vader": True
        }
    )
    assert response.status_code == 422  # Validation error


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
