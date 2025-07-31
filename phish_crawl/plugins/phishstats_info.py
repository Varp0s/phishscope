import os
import sys
import requests
import json
import logging
from datetime import datetime
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helper.database import DatabaseManager
from helper.utils import clean_url

class PhishStatsCrawler:
    def __init__(self):
        """Initialize the PhishStats crawler"""
        self.base_url = "https://api.phishstats.info"
        self.api_endpoint = f"{self.base_url}/api/phishing"
        self.db_manager = DatabaseManager()
        self.session = requests.Session()
        
        # Configure session headers
        self.session.headers.update({
            'User-Agent': 'PhishScope-Crawler/1.0 (Security Research)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        })
        
        # Set request parameters for the latest data
        self.params = {
            '_sort': '-id',  # Sort by newest first
            # '_limit': 1000   # Limit to 1000 results per request
        }
        
        logging.info("PhishStats.info crawler initialized")

    def fetch_data(self):
        try:
            logging.info(f"Fetching data from PhishStats.info API: {self.api_endpoint}")
            
            response = self.session.get(
                self.api_endpoint,
                params=self.params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    logging.info(f"Successfully fetched {len(data)} phishing URLs from PhishStats.info")
                    return data
                else:
                    logging.error(f"Unexpected data format received from PhishStats.info: {type(data)}")
                    return None
            else:
                logging.error(f"Failed to fetch data from PhishStats.info. Status code: {response.status_code}")
                logging.error(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error while fetching PhishStats.info data: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error while parsing PhishStats.info data: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while fetching PhishStats.info data: {e}")
            return None

    def process_data(self, data_list):
        if not data_list:
            logging.warning("No data to process from PhishStats.info")
            return False

        try:
            if not self.db_manager.connect():
                logging.error("Failed to connect to database")
                return False

            processed_count = 0
            duplicate_count = 0
            error_count = 0

            for item in data_list:
                try:
                    # Validate required fields
                    if not item.get('id') or not item.get('url'):
                        logging.warning(f"Skipping invalid PhishStats entry: missing id or url")
                        error_count += 1
                        continue

                    # Clean and validate URL
                    cleaned_url = clean_url(item['url'])
                    if not cleaned_url:
                        logging.warning(f"Skipping invalid URL: {item['url']}")
                        error_count += 1
                        continue
                    
                    # Update the item with cleaned URL
                    item['url'] = cleaned_url

                    # Check for duplicates before processing
                    if self.db_manager.check_phishstats_duplicate(item['id'], cleaned_url):
                        duplicate_count += 1
                        continue

                    # Insert data into database
                    success = self.db_manager.insert_phishstats_data(item)
                    
                    if success:
                        processed_count += 1
                        if processed_count % 100 == 0:
                            logging.info(f"Processed {processed_count} PhishStats URLs...")
                    else:
                        error_count += 1

                except Exception as e:
                    logging.error(f"Error processing PhishStats item {item.get('id', 'unknown')}: {e}")
                    error_count += 1
                    continue

            self.db_manager.disconnect()
            
            logging.info(f"PhishStats.info processing completed:")
            logging.info(f"  - Processed: {processed_count}")
            logging.info(f"  - Duplicates skipped: {duplicate_count}")
            logging.info(f"  - Errors: {error_count}")
            logging.info(f"  - Total items: {len(data_list)}")
            
            return processed_count > 0

        except Exception as e:
            logging.error(f"Error processing PhishStats.info data: {e}")
            self.db_manager.disconnect()
            return False

    def run(self):
        try:
            logging.info("=== Starting PhishStats.info Crawler ===")
            start_time = datetime.now()
            
            # Fetch data from API
            data = self.fetch_data()
            if not data:
                logging.error("Failed to fetch data from PhishStats.info")
                return False
            
            # Process and store data
            success = self.process_data(data)
            end_time = datetime.now()
            duration = end_time - start_time
            
            if success:
                logging.info(f"=== PhishStats.info Crawler Completed Successfully in {duration} ===")
                return True
            else:
                logging.error(f"=== PhishStats.info Crawler Failed after {duration} ===")
                return False
                
        except Exception as e:
            logging.error(f"Unexpected error in PhishStats.info crawler: {e}")
            return False

def main():
    crawler = PhishStatsCrawler()
    success = crawler.run()
    if success:
        print("PhishStats.info crawler completed successfully!")
    else:
        print("PhishStats.info crawler failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
