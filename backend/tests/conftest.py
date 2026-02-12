# backend/tests/conftest.py
import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

# Set test environment
os.environ["TESTING"] = "true"

@pytest.fixture
def client():
    """Create a test client for API testing"""
    return TestClient(app)

@pytest.fixture
def sample_texts():
    """Provide sample texts for testing"""
    return {
        "positive": "This product is amazing! I love it so much!",
        "negative": "This is terrible. Worst purchase ever.",
        "neutral": "The item arrived on time.",
        "negation": "not bad at all",
        "sarcasm": "Oh great, another delay. Just perfect.",
        "slang": "This movie absolutely slaps!",
        "harmful": "I want to hurt someone",
        "empty": "",
        "very_long": "word " * 1000  # 1000 words
    }

@pytest.fixture
def db_connection():
    """Get the database connection (may be None if DB not available)"""
    from app.database import get_connection
    return get_connection()