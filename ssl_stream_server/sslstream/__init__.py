import logging

import asyncio

# uvloop doesn't support Windows, so we'll use the default event loop policy
# try:
#     import uvloop
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#     logging.info("Using uvloop for better performance")
# except ImportError:
#     logging.info("uvloop not available, using default event loop policy")

from sslstream.certlib import MerkleTreeHeader
from sslstream.watcher import TransparencyWatcher

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

def run():
    logging.info("Starting CertStream...")

    # Create new event loop to avoid any potential issues
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    watcher = TransparencyWatcher(loop)

    # Initialize watcher manually to avoid the duplicate method issue
    watcher._initialize_ts_logs()
    
    # Manually create tasks for watching CT logs
    for log in watcher.transparency_logs['logs']:
        task = loop.create_task(watcher.watch_for_updates_task(log))
        logging.info(f"Created task for {log['description']}")

    # Run the webserver (this will also run the event loop)

if __name__ == "__main__":
    run()