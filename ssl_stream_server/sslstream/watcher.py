import aiohttp
import asyncio
import logging
import math
import requests
import sys
import os

from sslstream.certlib import parse_ctl_entry

class TransparencyWatcher(object):
    BAD_CT_SERVERS = [
        "alpha.ctlogs.org",
        "clicky.ct.letsencrypt.org",
        "ct.akamai.com",
        "ct.filippo.io/behindthesofa",
        "ct.gdca.com.cn",
        "ct.izenpe.com",
        "ct.izenpe.eus",
        "ct.sheca.com",
        "ct.startssl.com",
        "ct.wosign.com",
        "ctlog.api.venafi.com",
        "ctlog.gdca.com.cn",
        "ctlog.sheca.com",
        "ctlog.wosign.com",
        "ctlog2.wosign.com",
        "flimsy.ct.nordu.net:8080",
        "log.certly.io",
        "nessie2021.ct.digicert.com/log",
        "plausible.ct.nordu.net",
        "www.certificatetransparency.cn/ct",
    ]

    MAX_BLOCK_SIZE = 64

    def __init__(self, _loop):
        self.loop = _loop
        self.stopped = False
        self.logger = logging.getLogger('certstream.watcher')

        self.stream = asyncio.Queue(maxsize=3000)

        self.logger.info("Initializing the CTL watcher")

    def _initialize_ts_logs(self):
        try:
            self.logger.info("Retrieving certificate transparency logs list from Google...")
            response = requests.get('https://www.gstatic.com/ct/log_list/v3/all_logs_list.json', timeout=10)
            response.raise_for_status() 
            official_log_data = response.json()
            usable_logs = []
            
            for operator in official_log_data.get('operators', []):
                for log in operator.get('logs', []):
                    if 'state' in log and 'usable' in log['state']:
                        url = log['url']
                        if url.startswith('https://'):
                            url = url[8:] 
                        if url.endswith('/'):
                            url = url[:-1] 

                        usable_logs.append({
                            'description': log['description'],
                            'url': url,
                            'operator': operator['name']
                        })
            
            self.transparency_logs = {'logs': usable_logs}
            self.logger.info(f"Found {len(usable_logs)} usable logs from the official list")
            
        except Exception as e:
            self.logger.error(f"Error retrieving certificate directory: {str(e)}")
            self.logger.info("Using fallback transparency logs list...")
            self.transparency_logs = {
                "logs": [
                    {
                        "description": "Google 'Argon2025h1' log",
                        "url": "ct.googleapis.com/logs/us1/argon2025h1",
                        "operator": "Google"
                    },
                    {
                        "description": "Google 'Argon2025h2' log", 
                        "url": "ct.googleapis.com/logs/us1/argon2025h2",
                        "operator": "Google"
                    },
                    {
                        "description": "Google 'Xenon2025h1' log",
                        "url": "ct.googleapis.com/logs/eu1/xenon2025h1",
                        "operator": "Google"
                    },
                    {
                        "description": "Google 'Xenon2025h2' log",
                        "url": "ct.googleapis.com/logs/eu1/xenon2025h2", 
                        "operator": "Google"
                    },
                    {
                        "description": "Cloudflare 'Nimbus2025'",
                        "url": "ct.cloudflare.com/logs/nimbus2025",
                        "operator": "Cloudflare"
                    },
                    {
                        "description": "DigiCert Yeti2025 Log",
                        "url": "yeti2025.ct.digicert.com/log",
                        "operator": "DigiCert"
                    },
                    {
                        "description": "Let's Encrypt 'Oak2025h1'",
                        "url": "oak.ct.letsencrypt.org/2025h1",
                        "operator": "Let's Encrypt"
                    },
                    {
                        "description": "Let's Encrypt 'Oak2025h2'",
                        "url": "oak.ct.letsencrypt.org/2025h2",
                        "operator": "Let's Encrypt"
                    },
                    {
                        "description": "TrustAsia Log2025a",
                        "url": "ct2025-a.trustasia.com/log2025a",
                        "operator": "TrustAsia"
                    },
                    {
                        "description": "TrustAsia Log2025b",
                        "url": "ct2025-b.trustasia.com/log2025b",
                        "operator": "TrustAsia"
                    }
                ]
            }

        self.logger.info("Retrieved transparency log with {} entries to watch.".format(len(self.transparency_logs['logs'])))
        for entry in self.transparency_logs['logs']:
            operator_info = f" ({entry.get('operator', 'Unknown')})" if 'operator' in entry else ""
            self.logger.info("  + {}{}".format(entry['description'], operator_info))

    async def _print_memory_usage(self):
        import objgraph
        import gc

        while True:
            print("Stream backlog : {}".format(self.stream.qsize()))
            gc.collect()
            objgraph.show_growth()
            await asyncio.sleep(60)

    def get_tasks(self):
        self._initialize_ts_logs()

        coroutines = []

        if os.getenv("DEBUG_MEMORY", False):
            coroutines.append(self._print_memory_usage())

        self.logger.info(f"Setting up tasks for {len(self.transparency_logs['logs'])} certificate transparency logs")
        
        for log in self.transparency_logs['logs']:
            url = log['url']
            skip = False
            
            for bad_server in self.BAD_CT_SERVERS:
                if bad_server in url:
                    operator_info = f" ({log.get('operator', 'Unknown')})" if 'operator' in log else ""
                    self.logger.info(f"Skipping {log['description']}{operator_info} (in bad servers list)")
                    skip = True
                    break
            
            if not skip:
                operator_info = f" ({log.get('operator', 'Unknown')})" if 'operator' in log else ""
                self.logger.info(f"Adding task for {log['description']}{operator_info} ({url})")
                coroutines.append(self.watch_for_updates_task(log))
        
        self.logger.info(f"Created {len(coroutines)} CT log monitoring tasks")
        return coroutines

    def stop(self):
        self.logger.info('Got stop order, exiting...')
        self.stopped = True
        for task in asyncio.Task.all_tasks():
            task.cancel()

    async def watch_for_updates_task(self, operator_information):
        try:
            latest_size = 0
            name = operator_information['description']
            self.logger.info(f"[{name}] Starting CT log monitoring task")
            while not self.stopped:
                try:
                    url = operator_information['url']
                    if url.startswith(("http://", "https://")):
                        parsed_url = url.replace("https://", "").replace("http://", "")
                        ct_url = f"https://{parsed_url}/ct/v1/get-sth"
                    else:
                        ct_url = f"https://{url}/ct/v1/get-sth"
                    
                    self.logger.info(f"[{name}] Connecting to {ct_url}")
                    timeout = aiohttp.ClientTimeout(total=30)
                    
                    async with aiohttp.ClientSession(loop=self.loop, timeout=timeout) as session:
                        self.logger.info(f"[{name}] Session created, sending request...")
                        async with session.get(ct_url) as response:
                            self.logger.info(f"[{name}] Response received with status {response.status}")
                            if response.status == 200:
                                info = await response.json()
                                self.logger.info(f"[{name}] Successfully retrieved CT log data")
                            else:
                                error_text = await response.text()
                                self.logger.error(f"[{name}] HTTP error: {response.status}, {error_text}")
                                await asyncio.sleep(300)
                                continue
                                
                except aiohttp.ClientError as e:
                    self.logger.error(f'[{name}] Connection error -> {str(e)}')
                    await asyncio.sleep(300) 
                    continue
                except asyncio.TimeoutError:
                    self.logger.error(f'[{name}] Connection timeout')
                    await asyncio.sleep(300)
                    continue
                except Exception as e:
                    self.logger.error(f'[{name}] Unexpected error: {str(e)}')
                    await asyncio.sleep(300)
                    continue

                tree_size = info.get('tree_size')
                self.logger.info(f'[{name}] Current tree size: {tree_size}')

                if latest_size == 0:
                    self.logger.info(f'[{name}] First run, setting initial size to {tree_size}')
                    latest_size = tree_size

                if latest_size < tree_size:
                    self.logger.info(f'[{name}] [{latest_size} -> {tree_size}] New certs found, updating!')

                    try:
                        cert_count = 0
                        async for result_chunk in self.get_new_results(operator_information, latest_size, tree_size):
                            chunk_size = len(result_chunk)
                            self.logger.info(f'[{name}] Processing chunk of {chunk_size} certificates')
                            
                            successful_parses = 0
                            for entry in result_chunk:
                                try:
                                    cert_data = parse_ctl_entry(entry, operator_information)
                                    if cert_data is not None:
                                        await self.stream.put(cert_data)
                                        cert_count += 1
                                        successful_parses += 1
                                    else:
                                        self.logger.debug(f'[{name}] Skipped certificate (parsing returned None)')
                                except Exception as parse_error:
                                    self.logger.debug(f'[{name}] Error parsing certificate: {str(parse_error)}')
                            
                            if successful_parses > 0:
                                self.logger.info(f'[{name}] Successfully parsed {successful_parses}/{chunk_size} certificates in chunk')
                            
                        self.logger.info(f'[{name}] Added {cert_count} certificates to the stream')

                    except aiohttp.ClientError as e:
                        self.logger.error(f"[{name}] Network error while getting new results: {str(e)}")
                        await asyncio.sleep(60)
                        continue
                    except Exception as e:
                        self.logger.error(f"[{name}] Unexpected error while processing certificates: {str(e)}")
                        await asyncio.sleep(60)
                        continue

                    self.logger.info(f'[{name}] Update complete, new tree size: {tree_size}')
                    latest_size = tree_size
                else:
                    self.logger.info(f'[{name}] [{latest_size}|{tree_size}] No new certificates')

                self.logger.debug(f'[{name}] Sleeping for 30 seconds before next check')
                await asyncio.sleep(30)
        except Exception as e:
            print("Encountered an exception while getting new results! -> {}".format(e))
            return

    async def get_new_results(self, operator_information, latest_size, tree_size):
        total_size = tree_size - latest_size
        start = latest_size

        end = start + self.MAX_BLOCK_SIZE

        chunks = math.ceil(total_size / self.MAX_BLOCK_SIZE)

        self.logger.info("Retrieving {} certificates ({} -> {}) for {}".format(tree_size-latest_size, latest_size, tree_size, operator_information['description']))
        async with aiohttp.ClientSession(loop=self.loop) as session:
            for _ in range(chunks):
                if end >= tree_size:
                    end = tree_size - 1

                assert end >= start, "End {} is less than start {}!".format(end, start)
                assert end < tree_size, "End {} is less than tree_size {}".format(end, tree_size)

                url = "https://{}/ct/v1/get-entries?start={}&end={}".format(operator_information['url'], start, end)

                async with session.get(url) as response:
                    certificates = await response.json()
                    if 'error_message' in certificates:
                        print("error!")

                    for index, cert in zip(range(start, end+1), certificates['entries']):
                        cert['index'] = index

                    yield certificates['entries']

                start += self.MAX_BLOCK_SIZE
                end = start + self.MAX_BLOCK_SIZE + 1

class DummyTransparencyWatcher(object):
    stream = asyncio.Queue()
    def get_tasks(self):
        return []

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    watcher = TransparencyWatcher(loop)
    loop.run_until_complete(asyncio.gather(*watcher.get_tasks()))
