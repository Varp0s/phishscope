import requests
import logging
import os
from datetime import datetime
from helper.database import DatabaseManager
from helper.utils import clean_url

class OpenPhishCrawler:   
    def __init__(self):
        self.api_url = os.getenv('OPENPHISH_API_URL')
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
    
    def fetch_data(self):
        try:
            self.logger.info("Starting OpenPhish data fetch...")
            headers = {
                'User-Agent': 'PhishingCrawler/1.0 (Educational Purpose)'
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=30)
            response.raise_for_status()
            urls = response.text.strip().split('\n')
            urls = [url.strip() for url in urls if url.strip()]
            self.logger.info(f"Fetched {len(urls)} URLs from OpenPhish")
            return urls
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching OpenPhish data: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching OpenPhish data: {e}")
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
                
                try:
                    for url in batch:
                        try:
                            cleaned_url = clean_url(url)
                            if not cleaned_url:
                                continue
                            if self.db_manager.check_openphish_duplicate(cleaned_url):
                                continue
                            
                            if self.db_manager.insert_openphish_data(cleaned_url):
                                batch_success += 1
                            else:
                                batch_errors += 1
                                self.db_manager.rollback()
                                
                        except Exception as e:
                            self.logger.error(f"Error processing URL {url}: {e}")
                            batch_errors += 1
                            self.db_manager.rollback()
                    if batch_success > 0:
                        self.db_manager.commit()
                    
                    success_count += batch_success
                    error_count += batch_errors
                    
                    if (i // batch_size + 1) % 10 == 0:
                        self.logger.info(f"Processed {i + len(batch)}/{len(urls)} URLs. Success: {success_count}, Errors: {error_count}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
                    self.db_manager.rollback()
                    error_count += len(batch)
            
            self.logger.info(f"OpenPhish processing complete: {success_count} successful, {error_count} errors")
            
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error processing OpenPhish data: {e}")
            self.db_manager.rollback()
            return False
        finally:
            self.db_manager.disconnect()
    
    def run(self):
        try:
            self.logger.info("=== Starting OpenPhish Crawler ===")
            start_time = datetime.now()
            urls = self.fetch_data()
            if urls is None:
                self.logger.error("Failed to fetch OpenPhish data")
                return False
            if not self.process_data(urls):
                self.logger.error("Failed to process OpenPhish data")
                return False
            
            end_time = datetime.now()
            duration = end_time - start_time
            self.logger.info(f"=== OpenPhish Crawler completed in {duration.total_seconds():.2f} seconds ===")
            return True
            
        except Exception as e:
            self.logger.error(f"OpenPhish crawler failed: {e}")
            return False
