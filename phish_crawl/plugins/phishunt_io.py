import requests
import logging
import os
from datetime import datetime
from helper.database import DatabaseManager
from helper.utils import clean_url

class PhishuntCrawler:
    def __init__(self):
        self.api_url = os.getenv('PHISHUNT_API_URL', 'https://phishunt.io/feed.txt')
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
    
    def fetch_data(self):
        try:
            self.logger.info("Starting Phishunt.io data fetch...")
            headers = {
                'User-Agent': 'PhishingCrawler/1.0 (Educational Purpose)'
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            urls = response.text.strip().split('\n')
            urls = [url.strip() for url in urls if url.strip() and url.strip().startswith(('http://', 'https://'))]
            
            self.logger.info(f"Fetched {len(urls)} URLs from Phishunt.io")
            return urls
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching Phishunt.io data: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching Phishunt.io data: {e}")
            return None
    
    def process_data(self, urls):
        if not urls:
            return False
        
        try:
            if not self.db_manager.connect():
                return False
            
            success_count = 0
            error_count = 0
            batch_size = 50
            
            for i in range(0, len(urls), batch_size):
                batch = urls[i:i + batch_size]
                batch_success = 0
                batch_errors = 0
                
                for url in batch:
                    try:
                        cleaned_url = clean_url(url)
                        if not cleaned_url:
                            batch_errors += 1
                            continue
                        
                        # Check if URL already exists
                        if self.db_manager.check_phishunt_duplicate(cleaned_url):
                            continue
                        
                        # Insert new URL
                        if self.db_manager.insert_phishunt_url(cleaned_url):
                            batch_success += 1
                        else:
                            batch_errors += 1
                            
                    except Exception as e:
                        self.logger.error(f"Error processing URL {url}: {e}")
                        batch_errors += 1
                
                success_count += batch_success
                error_count += batch_errors
                
                self.logger.info(f"Processed batch {i//batch_size + 1}: {batch_success} success, {batch_errors} errors")
            
            self.db_manager.disconnect()
            self.logger.info(f"Phishunt.io processing completed: {success_count} successful insertions, {error_count} errors")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error processing Phishunt.io data: {e}")
            if self.db_manager.is_connected():
                self.db_manager.disconnect()
            return False
    
    def run(self):
        try:
            self.logger.info("Starting Phishunt.io crawler...")
            
            # Fetch data
            urls = self.fetch_data()
            if not urls:
                self.logger.warning("No data fetched from Phishunt.io")
                return False
            
            # Process data
            result = self.process_data(urls)
            
            if result:
                self.logger.info("Phishunt.io crawler completed successfully")
            else:
                self.logger.warning("Phishunt.io crawler completed with issues")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Critical error in Phishunt.io crawler: {e}")
            return False

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('../logs/crawler.log'),
            logging.StreamHandler()
        ]
    )
    
    crawler = PhishuntCrawler()
    return crawler.run()

if __name__ == "__main__":
    main()
