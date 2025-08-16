"""
Health Router - System Monitoring and Status
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any
import time
import psutil
import os

router = APIRouter()

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    uptime: float
    version: str
    environment: str

class SystemStatus(BaseModel):
    """System status response model."""
    status: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        uptime=time.time() - os.path.getctime(__file__),  # Simplified uptime
        version="2.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@router.get("/status", response_model=SystemStatus)
async def system_status():
    """Get detailed system status."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return SystemStatus(
            status="operational",
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            active_connections=0  # Placeholder for actual connection tracking
        )
    except Exception as e:
        return SystemStatus(
            status="error",
            cpu_usage=0.0,
            memory_usage=0.0,
            disk_usage=0.0,
            active_connections=0
        )

@router.get("/ready")
async def readiness_check(request: Request):
    """Readiness check to ensure the system is ready to serve requests."""
    try:
        # Check if RAG engine is available
        if hasattr(request.app.state, 'rag_engine'):
            return {"status": "ready", "message": "System is ready to serve requests"}
        else:
            return {"status": "not_ready", "message": "RAG engine not initialized"}
    except Exception as e:
        return {"status": "error", "message": f"Readiness check failed: {str(e)}"}

@router.get("/live")
async def liveness_check():
    """Liveness check to ensure the service is running."""
    return {"status": "alive", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

@router.get("/info")
async def system_info():
    """Get comprehensive system information."""
    try:
        return {
            "system": {
                "platform": os.name,
                "python_version": os.sys.version,
                "architecture": os.sys.platform
            },
            "environment": {
                "environment": os.getenv("ENVIRONMENT", "development"),
                "openai_api_key": "configured" if os.getenv("OPENAI_API_KEY") else "not_configured"
            },
            "process": {
                "pid": os.getpid(),
                "memory_info": psutil.Process().memory_info()._asdict() if hasattr(psutil, 'Process') else {}
            }
        }
    except Exception as e:
        return {"error": f"Failed to get system info: {str(e)}"}
