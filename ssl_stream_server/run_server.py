import asyncio
import logging
from datetime import datetime
from helper.sql_helper import db_helper, init_database, cleanup_database
from sslstream.watcher import TransparencyWatcher

logging.basicConfig(
    format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CertificateCrawler:    
    def __init__(self):
        self.processed_count = 0
        
    async def process_certificate(self, cert_data):
        try:
            leaf_cert = cert_data.get('leaf_cert', {})
            subject = leaf_cert.get('subject', {})
            all_domains = leaf_cert.get('all_domains', [])
            domains_str = ', '.join(all_domains) if all_domains else ''
            cert_db_data = {
                'subject_cn': subject.get('CN'),
                'issuer_cn': None,  # Will extract if needed later
                'serial_number': leaf_cert.get('serial_number'),
                'fingerprint': leaf_cert.get('fingerprint'),
                'not_before': datetime.fromtimestamp(leaf_cert.get('not_before', 0)) if leaf_cert.get('not_before') else None,
                'not_after': datetime.fromtimestamp(leaf_cert.get('not_after', 0)) if leaf_cert.get('not_after') else None,
                'domains': domains_str,  # All domains as comma-separated string
                'raw_data': cert_data
            }
            cert_id = await db_helper.insert_certificate(cert_db_data)
            
            if cert_id:
                self.processed_count += 1
                
                if self.processed_count % 100 == 0:
                    logger.info(f"📊 Processed: {self.processed_count} certificates")
                    
        except Exception as e:
            logger.error(f"Error processing certificate: {e}")

class EnhancedTransparencyWatcher(TransparencyWatcher):    
    def __init__(self, loop, crawler_server):
        super().__init__(loop)
        self.crawler_server = crawler_server
        
    async def process_entry_task(self):
        logger.info("Starting certificate processing task...")
        
        while not self.stopped:
            try:
                cert_data = await asyncio.wait_for(self.stream.get(), timeout=5.0)
                await self.crawler_server.process_certificate(cert_data)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in processing task: {e}")
                await asyncio.sleep(1)

async def main():
    logger.info("🚀 Starting Certificate Crawler...")
    logger.info("📊 Initializing database connection...")
    db_success = await init_database()
    
    if not db_success:
        logger.error("❌ Failed to initialize database. Exiting.")
        return
    logger.info("✅ Database initialized successfully!")
    
    try:
        loop = asyncio.get_event_loop()
        crawler_server = CertificateCrawler()
        watcher = EnhancedTransparencyWatcher(loop, crawler_server)
        watcher._initialize_ts_logs()
        tasks = []
        for log in watcher.transparency_logs['logs']:
            task = loop.create_task(watcher.watch_for_updates_task(log))
            tasks.append(task)
            logger.info(f"📡 Created task for {log['description']}")
        process_task = loop.create_task(watcher.process_entry_task())
        tasks.append(process_task)
        
        logger.info("🔍 Certificate Crawler is now monitoring CT logs...")
        logger.info("💾 All certificate data will be saved to PostgreSQL")
        logger.info("� Use: SELECT * FROM certificates WHERE domains ILIKE '%domain%' for searching")
        await asyncio.gather(*tasks)
        
    except KeyboardInterrupt:
        logger.info("🛑 Stopping Certificate Crawler...")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        await cleanup_database()
        logger.info("👋 Certificate Crawler stopped")

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()