from fastapi import APIRouter, Depends
import logging
from core.database import get_database

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def health_check(db=Depends(get_database)):
    try:
        # Test database connection
        result = await db.fetch_one("SELECT 1 as health_check, NOW() as timestamp")
        
        if result:
            return {
                "status": "healthy",
                "database": {
                    "status": "connected",
                    "timestamp": result["timestamp"]
                },
                "api": {
                    "status": "running",
                    "version": "v1"
                }
            }
        else:
            return {
                "status": "unhealthy",
                "database": {
                    "status": "disconnected"
                },
                "api": {
                    "status": "running",
                    "version": "v1"
                }
            }
            
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": {
                "status": "error",
                "error": str(e)
            },
            "api": {
                "status": "running",
                "version": "v1"
            }
        }

@router.get("/db")
async def database_health(db=Depends(get_database)):
    try:
        # Test basic connection
        basic_test = await db.fetch_one("SELECT 1 as test")
        # Test certificates table
        table_test = await db.fetch_one("SELECT COUNT(*) as count FROM certificates LIMIT 1")
        # Get current timestamp
        timestamp_result = await db.fetch_one("SELECT NOW() as timestamp")
        
        return {
            "database_connection": "ok" if basic_test else "failed",
            "certificates_table": "ok" if table_test else "failed",
            "timestamp": timestamp_result["timestamp"] if timestamp_result else None
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "database_connection": "failed",
            "error": str(e)
        }
