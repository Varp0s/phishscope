import asyncpg
import logging
from .config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.pool = None
        
    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                min_size=1,
                max_size=10
            )
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
            
    async def disconnect(self):
        try:
            if self.pool:
                await self.pool.close()
                logger.info("Database disconnected successfully")
        except Exception as e:
            logger.error(f"Database disconnection failed: {e}")
            raise
    
    async def execute_query(self, query: str, *args):
        try:
            async with self.pool.acquire() as conn:
                if args:
                    return await conn.execute(query, *args)
                else:
                    return await conn.execute(query)
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    async def fetch_one(self, query: str, *args):
        try:
            async with self.pool.acquire() as conn:
                if args:
                    return await conn.fetchrow(query, *args)
                else:
                    return await conn.fetchrow(query)
        except Exception as e:
            logger.error(f"Fetch one failed: {e}")
            raise
    
    async def fetch_all(self, query: str, *args):
        try:
            async with self.pool.acquire() as conn:
                if args:
                    return await conn.fetch(query, *args)
                else:
                    return await conn.fetch(query)
        except Exception as e:
            logger.error(f"Fetch all failed: {e}")
            raise

# Create database manager instance
database = DatabaseManager()

async def get_database():
    return database
