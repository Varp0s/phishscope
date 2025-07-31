import requests
import gzip
import json
import logging
import os
from datetime import datetime
from helper.database import DatabaseManager
from helper.utils import clean_url

class PhishTankCrawler:
    def __init__(self):
        self.api_url = os.getenv('PHISHTANK_API_URL')
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"PhishTank API URL: {self.api_url}")
        if not self.api_url:
            self.logger.error("PHISHTANK_API_URL environment variable is not set!")
    
    def fetch_data(self):
        try:
            if not self.api_url:
                self.logger.error("PhishTank API URL is not configured")
                return None
                
            self.logger.info("Starting PhishTank data fetch...")
            self.logger.info(f"Fetching from URL: {self.api_url}")
            headers = {
                'User-Agent': 'PhishingCrawler/1.0 (Educational Purpose)'
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=30, allow_redirects=True)
            if response.status_code == 403:
                self.logger.error("PhishTank API returned 403 Forbidden. You may need an API key.")
                return None
            elif response.status_code == 404:
                self.logger.error("PhishTank API returned 404 Not Found. The endpoint may have changed.")
                return None
            elif response.status_code == 429:
                self.logger.error("PhishTank API returned 429 Too Many Requests. Rate limit exceeded.")
                return None
            
            response.raise_for_status()
            content_type = response.headers.get('content-type', '').lower()
            if 'json' not in content_type and 'gzip' not in content_type and 'application/octet-stream' not in content_type:
                self.logger.warning(f"Unexpected content type: {content_type}")
            decompressed_data = gzip.decompress(response.content)
            json_data = json.loads(decompressed_data.decode('utf-8'))
            self.logger.info(f"Fetched {len(json_data)} records from PhishTank")
            return json_data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching PhishTank data: {e}")
            return None
        except gzip.BadGzipFile as e:
            self.logger.error(f"Error decompressing PhishTank data: {e}")
            self.logger.error("Response may not be gzipped or may be corrupted")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing PhishTank JSON: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching PhishTank data: {e}")
            return None
    
    def process_data(self, data):
        if not data:
            return False
        try:
            if not self.db_manager.connect():
                return False
            
            success_count = 0
            error_count = 0
            batch_size = 100
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                batch_success = 0
                batch_errors = 0
                
                try:
                    for record in batch:
                        try:
                            if record.get('url'):
                                record['url'] = clean_url(record['url'])
                            phish_id = record.get('phish_id')
                            url = record.get('url')
                            
                            if not phish_id or not url:
                                batch_errors += 1
                                continue
                            if self.db_manager.check_phishtank_duplicate(phish_id, url):
                                print(f"Duplicate found for url {url}, skipping...")
                                continue
                            
                            if self.db_manager.insert_phishtank_data(record):
                                batch_success += 1
                            else:
                                batch_errors += 1
                                self.db_manager.rollback()
                                
                        except Exception as e:
                            self.logger.error(f"Error processing record {record.get('phish_id', 'unknown')}: {e}")
                            batch_errors += 1
                            self.db_manager.rollback()
                    
                    if batch_success > 0:
                        self.db_manager.commit()
                    success_count += batch_success
                    error_count += batch_errors
                    
                    if (i // batch_size + 1) % 10 == 0:
                        self.logger.info(f"Processed {i + len(batch)}/{len(data)} records. Success: {success_count}, Errors: {error_count}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
                    self.db_manager.rollback()
                    error_count += len(batch)
            self.logger.info(f"PhishTank processing complete: {success_count} successful, {error_count} errors")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error processing PhishTank data: {e}")
            self.db_manager.rollback()
            return False
        finally:
            self.db_manager.disconnect()
    
    def run(self):
        try:
            self.logger.info("=== Starting PhishTank Crawler ===")
            start_time = datetime.now()
            data = self.fetch_data()
            if data is None:
                self.logger.error("Failed to fetch PhishTank data")
                return False
            if not self.process_data(data):
                self.logger.error("Failed to process PhishTank data")
                return False
            end_time = datetime.now()
            duration = end_time - start_time
            self.logger.info(f"=== PhishTank Crawler completed in {duration.total_seconds():.2f} seconds ===")
            return True
        except Exception as e:
            self.logger.error(f"PhishTank crawler failed: {e}")
            return False
