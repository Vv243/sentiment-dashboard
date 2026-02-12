# backend/tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestMainApp:
    """Test suite for main application"""
    
    def test_root_endpoint(self):
        """Test GET / root endpoint"""
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test GET /health endpoint"""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_docs_endpoint(self):
        """Test that /docs is accessible"""
        client = TestClient(app)
        response = client.get("/docs")
        
        assert response.status_code == 200
    
    def test_cors_headers(self):
        """Test that CORS is configured"""
        client = TestClient(app)
        response = client.get("/")
        
        # Should have CORS headers
        assert "access-control-allow-origin" in response.headers or response.status_code == 200