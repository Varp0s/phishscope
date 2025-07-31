#!/usr/bin/env python3
import uvicorn
import asyncio
import logging
from pathlib import Path
import sys

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from core.config import settings
from core.logging_config import setup_logging

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting PhishScope FastAPI Server...")
    logger.info(f"Configuration:")
    logger.info(f"   • Host: {settings.API_HOST}")
    logger.info(f"   • Port: {settings.API_PORT}")
    logger.info(f"   • Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    logger.info(f"   • Log Level: {settings.LOG_LEVEL}")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False,  
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        use_colors=True
    )

if __name__ == "__main__":
    main()
