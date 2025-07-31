import os
import requests
from datetime import datetime
from helper.database import DatabaseManager
from helper.utils import setup_logging

class BlackMirrorBlocklistCrawler:
    def __init__(self):
        self.logger = setup_logging()
        self.db_manager = DatabaseManager()
        self.blocklist_url = os.getenv('BLACKMIRROR_API_URL')
        self.source_name = "Black Mirror Blocklist"
        self.logger.info("Black Mirror Blocklist Crawler initialized")

    def fetch_blocklist(self):
        try:
            self.logger.info(f"Fetching Black Mirror blocklist from {self.blocklist_url}")
            response = requests.get(self.blocklist_url, timeout=30)
            
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch Black Mirror blocklist: HTTP {response.status_code}")
                return None
            
            # Parse the text file - one domain per line
            domains = [line.strip() for line in response.text.splitlines() if line.strip()]
            self.logger.info(f"Fetched {len(domains)} domains from Black Mirror blocklist")
            return domains
        except Exception as e:
            self.logger.error(f"Error fetching Black Mirror blocklist: {e}")
            return None

    def process_data(self, domains):
        if not domains:
            self.logger.warning("No domains to process from Black Mirror blocklist")
            return False
        
        try:
            if not self.db_manager.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            count = 0
            
            for domain in domains:
                # Format as URL if it's just a domain
                if not domain.startswith(('http://', 'https://')):
                    url = f"http://{domain}"
                else:
                    url = domain
                
                # Insert into blackmirror table
                success = self.db_manager.insert_blackmirror_data(url)
                if success:
                    count += 1
            
            self.logger.info(f"Successfully processed {count} out of {len(domains)} Black Mirror blocklist entries")
            self.db_manager.disconnect()
            return count > 0
        
        except Exception as e:
            self.logger.error(f"Error processing Black Mirror blocklist data: {e}")
            if self.db_manager.is_connected():
                self.db_manager.disconnect()
            return False

    def run(self):
        try:
            domains = self.fetch_blocklist()
            if domains:
                return self.process_data(domains)
            return False
        except Exception as e:
            self.logger.error(f"Black Mirror blocklist crawler execution failed: {e}")
            return False