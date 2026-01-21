"""
Health check and monitoring endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "sentiment-analysis-api",
        "version": "1.0.0"
    }


@router.get("/metrics")
async def get_metrics():
    """
    Get API metrics (placeholder for future implementation)
    
    Returns:
        Basic metrics
    """
    return {
        "uptime": "placeholder",
        "requests_total": 0,
        "requests_per_minute": 0,
        "active_collections": 0,
        "timestamp": datetime.utcnow().isoformat()
    }
