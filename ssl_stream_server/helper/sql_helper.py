import asyncio
import asyncpg
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLHelper:
    def __init__(self, 
                 host: str = None,
                 port: int = None,
                 database: str = None,
                 user: str = None,                 password: str = None):
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', '5432'))
        self.database = database or os.getenv('DB_NAME', 'phishing_crawler')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', 'postgres')
        self.pool = None
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Database config: {self.user}@{self.host}:{self.port}/{self.database}")
        
    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                min_size=1,
                max_size=10
            )
            self.logger.info(f"Connected to PostgreSQL database: {self.database}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            return False
    
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.logger.info("Database connection pool closed")
    
    async def init_tables(self):
        create_certificates_table = """
        CREATE TABLE IF NOT EXISTS certificates (
            id SERIAL PRIMARY KEY,
            subject_cn TEXT UNIQUE NOT NULL,  -- Make subject_cn unique and not null
            issuer_cn TEXT,
            serial_number TEXT,
            fingerprint TEXT,
            not_before TIMESTAMP,
            not_after TIMESTAMP,
            domains TEXT, -- All domains as comma-separated string for fast search
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        create_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_certificates_fingerprint ON certificates(fingerprint);",
            "CREATE INDEX IF NOT EXISTS idx_certificates_domains_gin ON certificates USING gin(to_tsvector('english', domains));",
            "CREATE INDEX IF NOT EXISTS idx_certificates_domains_text ON certificates(domains);",
            "CREATE INDEX IF NOT EXISTS idx_certificates_created_at ON certificates(created_at);",
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_certificates_subject_cn_unique ON certificates(subject_cn);"
        ]
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(create_certificates_table)
                
                for index_sql in create_indexes:
                    await conn.execute(index_sql)
                
                self.logger.info("Database tables initialized successfully with subject_cn as unique")
                return True
        except Exception as e:
            self.logger.error(f"Failed to initialize tables: {e}")
            return False
    
    async def insert_certificate(self, cert_data: Dict[str, Any]) -> Optional[int]:
        subject_cn = cert_data.get('subject_cn')
        if not subject_cn:
            self.logger.warning("Skipping certificate without subject_cn")
            return None
            
        insert_query = """
        INSERT INTO certificates (
            subject_cn, issuer_cn, serial_number, fingerprint, 
            not_before, not_after, domains, raw_data
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (subject_cn) DO UPDATE SET
            issuer_cn = EXCLUDED.issuer_cn,
            serial_number = EXCLUDED.serial_number,
            fingerprint = EXCLUDED.fingerprint,
            not_before = EXCLUDED.not_before,
            not_after = EXCLUDED.not_after,
            domains = EXCLUDED.domains,
            raw_data = EXCLUDED.raw_data,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id;
        """
        
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow(
                    insert_query,
                    subject_cn,
                    cert_data.get('issuer_cn'),
                    cert_data.get('serial_number'),
                    cert_data.get('fingerprint'),
                    cert_data.get('not_before'),
                    cert_data.get('not_after'),
                    cert_data.get('domains'), 
                    json.dumps(cert_data.get('raw_data', {}))
                )
                return result['id'] if result else None
        except Exception as e:
            self.logger.error(f"Failed to insert certificate: {e}")
            return None
    
    async def search_domains(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
        SELECT id, subject_cn, domains, created_at, fingerprint, updated_at
        FROM certificates
        WHERE domains ILIKE $1
        ORDER BY updated_at DESC, created_at DESC
        LIMIT $2;
        """
        
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, f"%{search_term}%", limit)
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to search domains: {e}")
            return []
            
    async def search_domains_fulltext(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
        SELECT id, subject_cn, domains, created_at, fingerprint, updated_at,
               ts_rank(to_tsvector('english', domains), plainto_tsquery('english', $1)) as rank
        FROM certificates
        WHERE to_tsvector('english', domains) @@ plainto_tsquery('english', $1)
        ORDER BY rank DESC, updated_at DESC, created_at DESC
        LIMIT $2;
        """
        
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, search_term, limit)
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to full-text search domains: {e}")
            return []
    
    async def search_by_subject_cn(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
        SELECT id, subject_cn, domains, created_at, fingerprint, updated_at
        FROM certificates
        WHERE subject_cn ILIKE $1
        ORDER BY updated_at DESC, created_at DESC
        LIMIT $2;
        """
        
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, f"%{search_term}%", limit)
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to search by subject_cn: {e}")
            return []
    
    async def get_certificate_by_subject_cn(self, subject_cn: str) -> Optional[Dict[str, Any]]:
        query = """
        SELECT * FROM certificates
        WHERE subject_cn = $1;
        """
        
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, subject_cn)
                return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Failed to get certificate by subject_cn: {e}")
            return None
    
    async def export_all_certificates(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit:
            query = """
            SELECT * FROM certificates
            ORDER BY updated_at DESC, created_at DESC
            LIMIT $1;
            """
            params = [limit]
        else:
            query = """
            SELECT * FROM certificates
            ORDER BY updated_at DESC, created_at DESC;
            """
            params = []
        
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, *params)
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to export certificates: {e}")
            return []
    
    async def get_stats(self) -> Dict[str, Any]:
        try:
            async with self.pool.acquire() as conn:
                total_certs = await conn.fetchval("SELECT COUNT(*) FROM certificates")
                recent_certs = await conn.fetchval(
                    "SELECT COUNT(*) FROM certificates WHERE created_at >= NOW() - INTERVAL '24 hours'"
                )
                updated_certs = await conn.fetchval(
                    "SELECT COUNT(*) FROM certificates WHERE updated_at > created_at"
                )
                unique_subjects = await conn.fetchval("SELECT COUNT(DISTINCT subject_cn) FROM certificates")
                
                return {
                    'total_certificates': total_certs,
                    'recent_certificates_24h': recent_certs,
                    'updated_certificates': updated_certs,
                    'unique_subject_cns': unique_subjects
                }
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {}
    
    async def reset_database(self) -> bool:
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("DROP TABLE IF EXISTS certificates CASCADE")
                self.logger.info("Dropped certificates table")
                return await self.init_tables()
        except Exception as e:
            self.logger.error(f"Failed to reset database: {e}")
            return False

# Global instance
db_helper = PostgreSQLHelper()

async def init_database():
    success = await db_helper.connect()
    if success:
        await db_helper.init_tables()
    return success

async def cleanup_database():
    await db_helper.disconnect()