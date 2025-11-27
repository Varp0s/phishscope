import asyncio
import aiohttp
from asyncio import Queue
import logging

logger = logging.getLogger(__name__)

# Configuration
MAX_BLOCK_SIZE = 512
CONCURRENT_REQUESTS = 50
CONNECTION_TIMEOUT = 30
READ_TIMEOUT = 60

# Comprehensive CT Log Sources - All major operators included
CT_LOG_SOURCES = [
    # Google Argon Logs (2021-2025)
    "https://ct.googleapis.com/logs/argon2021",
    "https://ct.googleapis.com/logs/argon2022",
    "https://ct.googleapis.com/logs/argon2023",
    "https://ct.googleapis.com/logs/argon2024",
    "https://ct.googleapis.com/logs/argon2025",
    
    # Google Xenon Logs (2021-2025)
    "https://ct.googleapis.com/logs/xenon2021",
    "https://ct.googleapis.com/logs/xenon2022",
    "https://ct.googleapis.com/logs/xenon2023",
    "https://ct.googleapis.com/logs/xenon2024",
    "https://ct.googleapis.com/logs/xenon2025",
    
    # Google Icarus/Pilot/Rocketeer/Skydiver/Submariner
    "https://ct.googleapis.com/icarus",
    "https://ct.googleapis.com/pilot",
    "https://ct.googleapis.com/rocketeer",
    "https://ct.googleapis.com/skydiver",
    "https://ct.googleapis.com/submariner",
    
    # Google US Regional (us1)
    "https://us1.ct.googleapis.com/logs/us1/argon2024",
    "https://us1.ct.googleapis.com/logs/us1/argon2025",
    "https://us1.ct.googleapis.com/logs/us1/xenon2024",
    "https://us1.ct.googleapis.com/logs/us1/xenon2025",
    
    # Google EU Regional (eu1)
    "https://eu1.ct.googleapis.com/logs/eu1/argon2024",
    "https://eu1.ct.googleapis.com/logs/eu1/argon2025",
    "https://eu1.ct.googleapis.com/logs/eu1/xenon2024",
    "https://eu1.ct.googleapis.com/logs/eu1/xenon2025",
    
    # Google APAC Regional (asia1)
    "https://asia1.ct.googleapis.com/logs/asia1/argon2024",
    "https://asia1.ct.googleapis.com/logs/asia1/argon2025",
    "https://asia1.ct.googleapis.com/logs/asia1/xenon2024",
    "https://asia1.ct.googleapis.com/logs/asia1/xenon2025",
    
    # Cloudflare Nimbus Logs (2021-2025)
    "https://ct.cloudflare.com/logs/nimbus2021",
    "https://ct.cloudflare.com/logs/nimbus2022",
    "https://ct.cloudflare.com/logs/nimbus2023",
    "https://ct.cloudflare.com/logs/nimbus2024",
    "https://ct.cloudflare.com/logs/nimbus2025",
    
    # DigiCert Logs
    "https://ct1.digicert-ct.com/log",
    "https://ct2.digicert-ct.com/log",
    "https://yeti2024.ct.digicert.com/log",
    "https://yeti2025.ct.digicert.com/log",
    "https://nessie2024.ct.digicert.com/log",
    "https://nessie2025.ct.digicert.com/log",
    "https://wyvern.ct.digicert.com/2024",
    "https://wyvern.ct.digicert.com/2025",
    "https://sphinx.ct.digicert.com/2024",
    "https://sphinx.ct.digicert.com/2025",
    
    # Let's Encrypt Oak Logs (2021-2025)
    "https://oak.ct.letsencrypt.org/2021",
    "https://oak.ct.letsencrypt.org/2022",
    "https://oak.ct.letsencrypt.org/2023",
    "https://oak.ct.letsencrypt.org/2024",
    "https://oak.ct.letsencrypt.org/2025",
    
    # Sectigo Logs (Mammoth & Sabre)
    "https://mammoth.ct.comodo.com",
    "https://sabre.ct.comodo.com",
    "https://sabre2024h1.ct.sectigo.com",
    "https://sabre2024h2.ct.sectigo.com",
    "https://sabre2025h1.ct.sectigo.com",
    "https://sabre2025h2.ct.sectigo.com",
    "https://mammoth2024h1.ct.sectigo.com",
    "https://mammoth2024h2.ct.sectigo.com",
    "https://mammoth2025h1.ct.sectigo.com",
    "https://mammoth2025h2.ct.sectigo.com",
    
    # TrustAsia Logs
    "https://ct.trustasia.com/log2021",
    "https://ct.trustasia.com/log2022",
    "https://ct.trustasia.com/log2023",
    "https://ct.trustasia.com/log2024",
    "https://ct.trustasia.com/log2025",
    "https://ct2021.trustasia.com/log2021",
    "https://ct2024.trustasia.com/log2024",
    "https://ct2025.trustasia.com/log2025",
    
    # Symantec/Norton Logs
    "https://ct.ws.symantec.com",
    "https://vega.ws.symantec.com",
    
    # CNNIC Logs (China)
    "https://ctserver.cnnic.cn",
    "https://ct.gdca.com.cn",
    
    # StartCom Logs
    "https://ct.startssl.com",
    
    # Venafi Logs
    "https://ctlog.api.venafi.com",
    "https://ctlog-gen2.api.venafi.com",
    
    # Certly Logs
    "https://log.certly.io",
    
    # Izenpe Logs
    "https://ct.izenpe.eus",
    
    # WoSign Logs
    "https://ct.wosign.com",
    "https://ctlog.wosign.com",
    
    # GDCA (China)
    "https://ct.gdca.com.cn",
    "https://ctlog.gdca.com.cn",
    
    # SHECA (Shanghai CA)
    "https://ct.sheca.com",
    
    # Nordu Logs (Nordic)
    "https://plausible.ct.nordu.net",
    "https://plausible.ct.nordu.net:8080",
    
    # SSLMate CertSpotter
    "https://certspotter.com",
    
    # Additional Active Logs
    "https://ct-log.gdca.com.cn",
    "https://ctserver.trustasia.com",
    "https://ct.akamai.com",
    "https://alpha.ctlogs.org",
]


class TransparencyWatcher:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.queue = Queue(maxsize=100000)
        self.session = None
        self.running = False
        self.log_positions = {}  # Track position in each log
        self.connector = None
        
    async def create_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(
                total=CONNECTION_TIMEOUT + READ_TIMEOUT,
                connect=CONNECTION_TIMEOUT,
                sock_read=READ_TIMEOUT
            )
            self.connector = aiohttp.TCPConnector(
                limit=CONCURRENT_REQUESTS * 2,
                limit_per_host=10,
                ttl_dns_cache=600,
                force_close=False,
                enable_cleanup_closed=True
            )
            self.session = aiohttp.ClientSession(
                connector=self.connector,
                timeout=timeout,
                headers={"User-Agent": "PhishScope-CT-Monitor/2.0"}
            )
        return self.session
    
    async def close(self):
        self.running = False
        if self.session and not self.session.closed:
            await self.session.close()
        if self.connector:
            await self.connector.close()
    
    async def get_sth(self, log_url: str) -> dict:
        try:
            session = await self.create_session()
            url = f"{log_url.rstrip('/')}/ct/v1/get-sth"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {"tree_size": data.get("tree_size", 0), "url": log_url}
        except Exception as e:
            logger.debug(f"Failed to get STH from {log_url}: {e}")
        return {"tree_size": 0, "url": log_url}
    
    async def get_entries(self, log_url: str, start: int, end: int) -> list:
        try:
            session = await self.create_session()
            url = f"{log_url.rstrip('/')}/ct/v1/get-entries"
            params = {"start": start, "end": min(end, start + MAX_BLOCK_SIZE - 1)}
            
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    entries = data.get("entries", [])
                    for i, entry in enumerate(entries):
                        entry["log_url"] = log_url
                        entry["index"] = start + i
                    return entries
        except Exception as e:
            logger.debug(f"Failed to get entries from {log_url}: {e}")
        return []
    
    async def process_log(self, log_url: str):
        try:
            # Get current tree size
            sth = await self.get_sth(log_url)
            tree_size = sth.get("tree_size", 0)
            
            if tree_size == 0:
                return
            # Get last known position
            last_pos = self.log_positions.get(log_url, max(0, tree_size - 10000))
            
            # Fetch new entries
            while last_pos < tree_size and self.running:
                end = min(last_pos + MAX_BLOCK_SIZE, tree_size)
                entries = await self.get_entries(log_url, last_pos, end)
                
                if not entries:
                    break
                
                for entry in entries:
                    if not self.queue.full():
                        await self.queue.put(entry)
                    else:
                        # Queue full, wait a bit
                        await asyncio.sleep(0.1)
                        try:
                            await asyncio.wait_for(
                                self.queue.put(entry),
                                timeout=1.0
                            )
                        except asyncio.TimeoutError:
                            pass
                
                last_pos = end
                self.log_positions[log_url] = last_pos
                
                # Small delay between batches
                await asyncio.sleep(0.05)
                
        except Exception as e:
            logger.error(f"Error processing log {log_url}: {e}")
    
    async def watch_logs(self, poll_interval: int = 5):
        self.running = True
        await self.create_session()
        logger.info(f"Starting CT log watcher with {len(CT_LOG_SOURCES)} log sources")
        
        while self.running:
            try:
                # Process all logs concurrently in batches
                batch_size = 20
                for i in range(0, len(CT_LOG_SOURCES), batch_size):
                    batch = CT_LOG_SOURCES[i:i + batch_size]
                    tasks = [self.process_log(log_url) for log_url in batch]
                    await asyncio.gather(*tasks, return_exceptions=True)
                    await asyncio.sleep(0.5)  # Small delay between batches
                
                # Wait before next poll cycle
                await asyncio.sleep(poll_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in watch loop: {e}")
                await asyncio.sleep(poll_interval)
        
        await self.close()
    
    def get_tasks(self):
        """Get list of monitoring tasks (compatible interface)"""
        return [{"url": log_url, "name": log_url.split("/")[-1]} for log_url in CT_LOG_SOURCES]
    
    async def get_queue_item(self, timeout: float = 1.0):
        """Get item from queue with timeout"""
        try:
            return await asyncio.wait_for(self.queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None
    
    @property
    def queue_size(self):
        return self.queue.qsize()
