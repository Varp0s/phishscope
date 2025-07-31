import requests
import logging
import os
from helper.database import DatabaseManager
from helper.utils import clean_url

class PhishingArmyBlocklistCrawler:
    def __init__(self):
        self.api_url = os.getenv('PHISHING_ARMY_API_URL')
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)

    def fetch_blocklist(self):
        try:
            self.logger.info("Fetching blocklist from Phishing Army...")
            response = requests.get(self.api_url)
            response.raise_for_status()
            urls = response.text.strip().split('\n')
            urls = [url.strip() for url in urls if url.strip() and not url.strip().startswith('#') and not url.strip().startswith('=')]
            self.logger.info(f"Fetched {len(urls)} URLs from Phishing Army blocklist")
            return urls
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching Phishing Army data: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching Phishing Army data: {e}")
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
                            if self.db_manager.check_phishingarmy_duplicate(cleaned_url):
                                self.logger.info(f"Duplicate URL found: {cleaned_url}, skipping")
                                continue
                            if self.db_manager.insert_phishingarmy_data(cleaned_url):
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
            self.logger.info(f"Phishing Army processing complete: {success_count} successful, {error_count} errors")
            return success_count > 0
        except Exception as e:
            self.logger.error(f"Error processing Phishing Army data: {e}")
            self.db_manager.rollback()
            return False
        finally:
            self.db_manager.disconnect()

    def run(self):
        try:
            self.logger.info("Starting Phishing Army blocklist plugin...")
            urls = self.fetch_blocklist()
            if not urls:
                self.logger.warning("No URLs fetched from Phishing Army blocklist.")
                return False
            if not self.process_data(urls):
                self.logger.error("Error processing Phishing Army blocklist data.")
                return False
            self.logger.info("Phishing Army blocklist plugin completed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error in Phishing Army blocklist plugin: {e}")
            return False