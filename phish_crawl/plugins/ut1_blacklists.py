import os
import gzip
import requests
from datetime import datetime
from helper.database import DatabaseManager
from helper.utils import setup_logging

class UT1BlacklistCrawler:
    def __init__(self, category):
        self.logger = setup_logging()
        self.db_manager = DatabaseManager()
        self.category = category
        self.source_name = f"UT1-Blacklists-{category}"
        self.base_url = os.getenv("UT1_CRAWL_URL")
        self.logger.info(f"UT1 {category} Blacklist Crawler initialized")

    def fetch_domains_from_file(self, filename):
        try:
            url = f"{self.base_url}/{self.category}/{filename}"
            self.logger.info(f"Fetching UT1 {self.category} from {url}")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch UT1 {self.category}: HTTP {response.status_code}")
                return None
            
            if filename.endswith('.gz'):
                content = gzip.decompress(response.content).decode('utf-8')
            else:
                content = response.text

            domains = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
            self.logger.info(f"Fetched {len(domains)} entries from UT1 {self.category} {filename}")
            return domains
            
        except Exception as e:
            self.logger.error(f"Error fetching UT1 {self.category} {filename}: {e}")
            return None

    def fetch_blocklist(self):
        domains = []
        file_types = ['domains.gz', 'domains', 'urls']
        
        for file_type in file_types:
            fetched_domains = self.fetch_domains_from_file(file_type)
            if fetched_domains:
                domains.extend(fetched_domains)
                break  # Use the first successful file type
                
        if not domains:
            self.logger.warning(f"No domains found for UT1 {self.category}")
            return None
            
        # Remove duplicates while preserving order
        unique_domains = list(dict.fromkeys(domains))
        self.logger.info(f"Total unique domains for UT1 {self.category}: {len(unique_domains)}")
        
        return unique_domains

    def process_data(self, domains):
        if not domains:
            self.logger.warning(f"No domains to process from UT1 {self.category}")
            return False
        
        try:
            if not self.db_manager.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            count = 0
            table_name = f"ut1_{self.category.replace('-', '_')}"
            
            for domain in domains:
                # Format as URL if it's just a domain
                if not domain.startswith(('http://', 'https://')):
                    url = f"http://{domain}"
                else:
                    url = domain
                
                # Insert into specific UT1 table
                success = self.db_manager.insert_ut1_data(table_name, url)
                
                if success:
                    count += 1
            
            self.logger.info(f"Successfully processed {count} out of {len(domains)} UT1 {self.category} entries")
            self.db_manager.disconnect()
            return count > 0
        
        except Exception as e:
            self.logger.error(f"Error processing UT1 {self.category} data: {e}")
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
            self.logger.error(f"UT1 {self.category} crawler execution failed: {e}")
            return False


# Specific UT1 category crawlers
class UT1AdultCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("adult")

class UT1AgressifCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("agressif")

class UT1ArjelCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("arjel")

class UT1AssociationsReligieusesCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("associations_religieuses")

class UT1AstrologyCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("astrology")

class UT1AudioVideoCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("audio-video")

class UT1BankCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("bank")

class UT1BitcoinCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("bitcoin")

class UT1BlogCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("blog")

class UT1CelebrityCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("celebrity")

class UT1ChatCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("chat")

class UT1ChildCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("child")

class UT1CleaningCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("cleaning")

class UT1CookingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("cooking")

class UT1CryptojackingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("cryptojacking")

class UT1DangerousMaterialCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("dangerous_material")

class UT1DatingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("dating")

class UT1DDoSCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("ddos")

class UT1DialerCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("dialer")

class UT1DoHCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("doh")

class UT1DownloadCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("download")

class UT1DrogueCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("drogue")

class UT1DynamicDNSCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("dynamic-dns")

class UT1EducationalGamesCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("educational_games")

class UT1ExamenPixCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("examen_pix")

class UT1FakenewsCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("fakenews")

class UT1FilehostingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("filehosting")

class UT1FinancialCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("financial")

class UT1ForumsCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("forums")

class UT1GamblingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("gambling")

class UT1GamesCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("games")

class UT1HackingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("hacking")

class UT1JobsearchCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("jobsearch")

class UT1LingerieCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("lingerie")

class UT1ListeBuCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("liste_bu")

class UT1MalwareCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("malware")

class UT1MangaCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("manga")

class UT1MarketingwareCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("marketingware")

class UT1MixedAdultCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("mixed_adult")

class UT1MobilePhoneCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("mobile-phone")

class UT1PhishingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("phishing")

class UT1PressCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("press")

class UT1PubliciteCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("publicite")

class UT1RadioCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("radio")

class UT1ReaffectedCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("reaffected")

class UT1RedirectorCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("redirector")

class UT1RemoteControlCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("remote-control")

class UT1ResidentialProxiesCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("residential_proxies")

class UT1SectCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("sect")

class UT1SexualEducationCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("sexual_education")

class UT1ShoppingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("shopping")

class UT1ShortenerCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("shortener")

class UT1SocialNetworksCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("social_networks")

class UT1SportsCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("sports")

class UT1StalkerwareCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("stalkerware")

class UT1StrictRedirectorCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("strict_redirector")

class UT1StrongRedirectorCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("strong_redirector")

class UT1TranslationCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("translation")

class UT1TricheurCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("tricheur")

class UT1TricheurPixCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("tricheur_pix")

class UT1UpdateCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("update")

class UT1VPNCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("vpn")

class UT1WarezCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("warez")

class UT1WebhostingCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("webhosting")

class UT1WebmailCrawler(UT1BlacklistCrawler):
    def __init__(self):
        super().__init__("webmail")
