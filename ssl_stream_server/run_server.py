import asyncio
import logging
from datetime import datetime
from helper.sql_helper import db_helper, init_database, cleanup_database
from sslstream.watcher import TransparencyWatcher
from sslstream.certlib import parse_ctl_entry

logging.basicConfig(
    format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CertificateCrawler:
    """High-throughput certificate processor with batch insertion"""
    def __init__(self):
        self.processed_count = 0
        self.batch = []
        self.batch_size = 500
        self.batch_lock = asyncio.Lock()
        self.errors = 0
        
    async def process_certificate(self, cert_data: dict):
        """Process a single certificate and add to batch"""
        try:
            leaf_cert = cert_data.get('leaf_cert', {})
            subject = leaf_cert.get('subject', {})
            all_domains = leaf_cert.get('all_domains', [])
            
            cert_db_data = {
                'subject_cn': subject.get('CN'),
                'issuer_cn': None,
                'serial_number': leaf_cert.get('serial_number'),
                'fingerprint': leaf_cert.get('fingerprint'),
                'not_before': datetime.fromtimestamp(leaf_cert.get('not_before', 0)) if leaf_cert.get('not_before') else None,
                'not_after': datetime.fromtimestamp(leaf_cert.get('not_after', 0)) if leaf_cert.get('not_after') else None,
                'domains': ', '.join(all_domains) if all_domains else '',
                'raw_data': cert_data
            }
            
            async with self.batch_lock:
                self.batch.append(cert_db_data)
                if len(self.batch) >= self.batch_size:
                    await self._flush_batch()
                    
        except Exception as e:
            self.errors += 1
            if self.errors % 1000 == 0:
                logger.error(f"Certificate processing errors: {self.errors}")
    
    async def _flush_batch(self):
        if not self.batch:
            return
            
        batch_to_insert = self.batch[:]
        self.batch = []
        
        try:
            count = await db_helper.bulk_insert_certificates(batch_to_insert)
            if count:
                self.processed_count += count
                logger.info(f"📊 Inserted {count} certificates | Total: {self.processed_count}")
        except Exception as e:
            logger.error(f"Batch insert error: {e}")
    
    async def force_flush(self):
        async with self.batch_lock:
            await self._flush_batch()

class CertificateWorker:    
    def __init__(self, worker_id: int, watcher: TransparencyWatcher, crawler: CertificateCrawler):
        self.worker_id = worker_id
        self.watcher = watcher
        self.crawler = crawler
        self.running = False
        self.processed = 0
        
    async def run(self):
        """Main worker loop"""
        self.running = True
        logger.info(f"Worker {self.worker_id} started")
        
        while self.running:
            try:
                # Get entry from queue with timeout
                entry = await self.watcher.get_queue_item(timeout=2.0)
                
                if entry is None:
                    # No entry, flush batch
                    await self.crawler.force_flush()
                    continue
                
                # Parse the CT log entry
                cert_data = parse_ctl_entry(entry)
                
                if cert_data:
                    await self.crawler.process_certificate(cert_data)
                    self.processed += 1
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {self.worker_id} error: {e}")
                await asyncio.sleep(0.5)
        
        logger.info(f"Worker {self.worker_id} stopped (processed: {self.processed})")
    
    def stop(self):
        self.running = False

async def status_reporter(watcher: TransparencyWatcher, crawler: CertificateCrawler):
    """Periodically report status"""
    while True:
        try:
            await asyncio.sleep(30)
            logger.info(
                f"📈 Status | Queue: {watcher.queue_size} | "
                f"Processed: {crawler.processed_count} | "
                f"Errors: {crawler.errors}"
            )
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Status reporter error: {e}")

async def main():
    logger.info("🚀 Starting Certificate Crawler...")
    logger.info("📊 Initializing database connection...")
    
    db_success = await init_database()
    if not db_success:
        logger.error("❌ Failed to initialize database. Exiting.")
        return
    
    logger.info("✅ Database initialized successfully!")
    
    # Create components
    crawler = CertificateCrawler()
    watcher = TransparencyWatcher()
    
    # Get log sources info
    tasks_info = watcher.get_tasks()
    logger.info(f"📡 Monitoring {len(tasks_info)} CT log sources")
    
    try:
        # Create tasks
        tasks = []
        
        # Main watcher task
        watcher_task = asyncio.create_task(watcher.watch_logs(poll_interval=5))
        tasks.append(watcher_task)
        logger.info("✅ CT log watcher started")
        
        # Create worker pool
        num_workers = 15
        workers = []
        for i in range(num_workers):
            worker = CertificateWorker(i, watcher, crawler)
            worker_task = asyncio.create_task(worker.run())
            workers.append(worker)
            tasks.append(worker_task)
        logger.info(f"✅ Created {num_workers} processing workers")
        
        # Status reporter
        status_task = asyncio.create_task(status_reporter(watcher, crawler))
        tasks.append(status_task)
        
        logger.info("🔍 Certificate Crawler is now monitoring CT logs...")
        logger.info("💾 All certificate data saved to PostgreSQL")
        logger.info("🔎 Query: SELECT * FROM certificates WHERE domains ILIKE '%domain%'")
        
        # Wait for all tasks
        await asyncio.gather(*tasks)
        
    except KeyboardInterrupt:
        logger.info("🛑 Stopping Certificate Crawler...")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        await watcher.close()
        await crawler.force_flush()
        await cleanup_database()
        logger.info("👋 Certificate Crawler stopped")

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
