from fastapi import FastAPI, Depends, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv
from pathlib import Path


env_file_path = Path('./env/.env')
load_dotenv()

from core.config import settings
from core.database import database, get_database
from api.v1.router import api_router
from core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
try:
    from plugins.vt_scanner import (
        url_search,
        hash_search,
        vt_report
    )
    VT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"VirusTotal scanner not available: {e}")
    VT_AVAILABLE = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting PhishScope API...")
    try:
        await database.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    
    yield

    logger.info("Shutting down PhishScope API...")
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Database disconnection failed: {e}")
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=f"/{settings.API_VERSION}/swagger",
    redoc_url=f"/{settings.API_VERSION}/redoc",
    openapi_url=f"/{settings.API_VERSION}/openapi.json",
    
    
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] 
)

app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")

@app.get("/")
async def root():
    return {
        "message": "PhishScope API",
        "version": settings.API_VERSION,
        "docs": f"/{settings.API_VERSION}/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check(db=Depends(get_database)):
    try:
        result = await db.fetch_one("SELECT 1 as health_check")
        db_status = "connected" if result else "disconnected"
    except Exception as e:
        logger.error(f"Health check database error: {e}")
        db_status = "error"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.API_VERSION
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
