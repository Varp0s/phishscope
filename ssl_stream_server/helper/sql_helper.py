import asyncio
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
from dotenv import load_dotenv
import psycopg
from psycopg_pool import AsyncConnectionPool

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
            conninfo = f"host={self.host} port={self.port} dbname={self.database} user={self.user} password={self.password}"
            self.pool = AsyncConnectionPool(
                conninfo=conninfo,
                min_size=10,
                max_size=50,
                timeout=60,
                open=True
            )
            await self.pool.wait()
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
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(create_certificates_table)
                    
                    for index_sql in create_indexes:
                        await cur.execute(index_sql)
                    
                    await conn.commit()
                    self.logger.info("Database tables initialized successfully with subject_cn as unique")
                    return True
        except Exception as e:
            self.logger.error(f"Failed to initialize tables: {e}")
            return False
    
    async def bulk_insert_certificates(self, cert_data_list: List[Dict[str, Any]]) -> int:
        if not cert_data_list:
            return 0
            
        insert_query = """
        INSERT INTO certificates (
            subject_cn, issuer_cn, serial_number, fingerprint, 
            not_before, not_after, domains, raw_data
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (subject_cn) DO UPDATE SET
            serial_number = EXCLUDED.serial_number,
            fingerprint = EXCLUDED.fingerprint,
            not_before = EXCLUDED.not_before,
            not_after = EXCLUDED.not_after,
            domains = EXCLUDED.domains,
            raw_data = EXCLUDED.raw_data,
            updated_at = CURRENT_TIMESTAMP;
        """
        
        try:
            async with self.pool.connection() as conn:
                async with conn.transaction():
                    async with conn.cursor() as cur:
                        inserted = 0
                        for cert_data in cert_data_list:
                            subject_cn = cert_data.get('subject_cn')
                            if not subject_cn:
                                continue
                                
                            await cur.execute(
                                insert_query,
                                (
                                    subject_cn,
                                    cert_data.get('issuer_cn'),
                                    cert_data.get('serial_number'),
                                    cert_data.get('fingerprint'),
                                    cert_data.get('not_before'),
                                    cert_data.get('not_after'),
                                    cert_data.get('domains'), 
                                    json.dumps(cert_data.get('raw_data', {}))
                                )
                            )
                            inserted += 1
                        return inserted
        except Exception as e:
            self.logger.error(f"Failed to bulk insert certificates: {e}")
            return 0
    
    async def insert_certificate(self, cert_data: Dict[str, Any]) -> Optional[int]:
        subject_cn = cert_data.get('subject_cn')
        if not subject_cn:
            self.logger.warning("Skipping certificate without subject_cn")
            return None
            
        insert_query = """
        INSERT INTO certificates (
            subject_cn, issuer_cn, serial_number, fingerprint, 
            not_before, not_after, domains, raw_data
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (subject_cn) DO UPDATE SET
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
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        insert_query,
                        (
                            subject_cn,
                            cert_data.get('issuer_cn'),
                            cert_data.get('serial_number'),
                            cert_data.get('fingerprint'),
                            cert_data.get('not_before'),
                            cert_data.get('not_after'),
                            cert_data.get('domains'), 
                            json.dumps(cert_data.get('raw_data', {}))
                        )
                    )
                    result = await cur.fetchone()
                    return result[0] if result else None
        except Exception as e:
            self.logger.error(f"Failed to insert certificate: {e}")
            return None
    
    async def search_domains(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
        SELECT id, subject_cn, domains, created_at, fingerprint, updated_at
        FROM certificates
        WHERE domains ILIKE %s
        ORDER BY updated_at DESC, created_at DESC
        LIMIT %s;
        """
        
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (f"%{search_term}%", limit))
                    rows = await cur.fetchall()
                    if not rows:
                        return []
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to search domains: {e}")
            return []
            
    async def search_domains_fulltext(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
        SELECT id, subject_cn, domains, created_at, fingerprint, updated_at,
               ts_rank(to_tsvector('english', domains), plainto_tsquery('english', %s)) as rank
        FROM certificates
        WHERE to_tsvector('english', domains) @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC, updated_at DESC, created_at DESC
        LIMIT %s;
        """
        
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (search_term, search_term, limit))
                    rows = await cur.fetchall()
                    if not rows:
                        return []
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to full-text search domains: {e}")
            return []
    
    async def search_by_subject_cn(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
        SELECT id, subject_cn, domains, created_at, fingerprint, updated_at
        FROM certificates
        WHERE subject_cn ILIKE %s
        ORDER BY updated_at DESC, created_at DESC
        LIMIT %s;
        """
        
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (f"%{search_term}%", limit))
                    rows = await cur.fetchall()
                    if not rows:
                        return []
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to search by subject_cn: {e}")
            return []
    
    async def get_certificate_by_subject_cn(self, subject_cn: str) -> Optional[Dict[str, Any]]:
        query = """
        SELECT * FROM certificates
        WHERE subject_cn = %s;
        """
        
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (subject_cn,))
                    row = await cur.fetchone()
                    if not row:
                        return None
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, row))
        except Exception as e:
            self.logger.error(f"Failed to get certificate by subject_cn: {e}")
            return None
    
    async def export_all_certificates(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit:
            query = """
            SELECT * FROM certificates
            ORDER BY updated_at DESC, created_at DESC
            LIMIT %s;
            """
            params = (limit,)
        else:
            query = """
            SELECT * FROM certificates
            ORDER BY updated_at DESC, created_at DESC;
            """
            params = ()
        
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()
                    if not rows:
                        return []
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to export certificates: {e}")
            return []
    
    async def get_stats(self) -> Dict[str, Any]:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT COUNT(*) FROM certificates")
                    total_certs = (await cur.fetchone())[0]
                    
                    await cur.execute("SELECT COUNT(*) FROM certificates WHERE created_at >= NOW() - INTERVAL '24 hours'")
                    recent_certs = (await cur.fetchone())[0]
                    
                    await cur.execute("SELECT COUNT(*) FROM certificates WHERE updated_at > created_at")
                    updated_certs = (await cur.fetchone())[0]
                    
                    await cur.execute("SELECT COUNT(DISTINCT subject_cn) FROM certificates")
                    unique_subjects = (await cur.fetchone())[0]
                    
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
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("DROP TABLE IF EXISTS certificates CASCADE")
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