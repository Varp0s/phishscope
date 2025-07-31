import os
import sys
import schedule
import time
import threading
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from helper.utils import setup_logging
from helper.database import DatabaseManager
from plugins.phishtank import PhishTankCrawler
from plugins.openphish import OpenPhishCrawler
from plugins.phishing_army_blocklist import PhishingArmyBlocklistCrawler
from plugins.black_mirror_blocklist import BlackMirrorBlocklistCrawler
from plugins.phishunt_io import PhishuntCrawler
from plugins.phishstats_info import PhishStatsCrawler
from plugins.ut1_blacklists import (
    UT1AdultCrawler, UT1AgressifCrawler, UT1ArjelCrawler, 
    UT1AssociationsReligieusesCrawler, UT1AstrologyCrawler, UT1AudioVideoCrawler,
    UT1BankCrawler, UT1BitcoinCrawler, UT1BlogCrawler, UT1CelebrityCrawler,
    UT1ChatCrawler, UT1ChildCrawler, UT1CleaningCrawler, UT1CookingCrawler,
    UT1CryptojackingCrawler, UT1DangerousMaterialCrawler, UT1DatingCrawler,
    UT1DDoSCrawler, UT1DialerCrawler, UT1DoHCrawler, UT1DownloadCrawler,
    UT1DrogueCrawler, UT1DynamicDNSCrawler, UT1EducationalGamesCrawler,
    UT1ExamenPixCrawler, UT1FakenewsCrawler, UT1FilehostingCrawler,
    UT1FinancialCrawler, UT1ForumsCrawler, UT1GamblingCrawler, UT1GamesCrawler,
    UT1HackingCrawler, UT1JobsearchCrawler, UT1LingerieCrawler, UT1ListeBuCrawler,
    UT1MalwareCrawler, UT1MangaCrawler, UT1MarketingwareCrawler, UT1MixedAdultCrawler,
    UT1MobilePhoneCrawler, UT1PhishingCrawler, UT1PressCrawler, UT1PubliciteCrawler,
    UT1RadioCrawler, UT1ReaffectedCrawler, UT1RedirectorCrawler, UT1RemoteControlCrawler,
    UT1ResidentialProxiesCrawler, UT1SectCrawler, UT1SexualEducationCrawler,
    UT1ShoppingCrawler, UT1ShortenerCrawler, UT1SocialNetworksCrawler, UT1SportsCrawler,
    UT1StalkerwareCrawler, UT1StrictRedirectorCrawler, UT1StrongRedirectorCrawler,
    UT1TranslationCrawler, UT1TricheurCrawler, UT1TricheurPixCrawler, UT1UpdateCrawler,
    UT1VPNCrawler, UT1WarezCrawler, UT1WebhostingCrawler, UT1WebmailCrawler
)

class PhishingCrawler:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), 'env', '.env'))
        self.logger = setup_logging()
        self.phishtank_crawler = PhishTankCrawler()
        self.openphish_crawler = OpenPhishCrawler()
        self.phishtank_interval = int(os.getenv('PHISHTANK_FETCH_INTERVAL', 2))
        self.openphish_interval = int(os.getenv('OPENPHISH_FETCH_INTERVAL', 12))
        self.phishing_army_interval = int(os.getenv('PHISHING_ARMY_FETCH_INTERVAL', 24))
        self.black_mirror_interval = int(os.getenv('BLACKMIRROR_FETCH_INTERVAL', 24))
        self.phishunt_interval = int(os.getenv('PHISHUNT_FETCH_INTERVAL', 24))
        self.phishstats_interval = int(os.getenv('PHISHSTATS_FETCH_INTERVAL', 24))
        self.ut1_interval = int(os.getenv('UT1_FETCH_INTERVAL', 24))
        
        # UT1 crawler configuration
        self.ut1_crawlers = {}
        if os.getenv('UT1_ADULT_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['adult'] = UT1AdultCrawler()
        if os.getenv('UT1_AGRESSIF_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['agressif'] = UT1AgressifCrawler()
        if os.getenv('UT1_ARJEL_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['arjel'] = UT1ArjelCrawler()
        if os.getenv('UT1_ASSOCIATIONS_RELIGIEUSES_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['associations_religieuses'] = UT1AssociationsReligieusesCrawler()
        if os.getenv('UT1_ASTROLOGY_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['astrology'] = UT1AstrologyCrawler()
        if os.getenv('UT1_AUDIO_VIDEO_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['audio_video'] = UT1AudioVideoCrawler()
        if os.getenv('UT1_BANK_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['bank'] = UT1BankCrawler()
        if os.getenv('UT1_BITCOIN_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['bitcoin'] = UT1BitcoinCrawler()
        if os.getenv('UT1_BLOG_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['blog'] = UT1BlogCrawler()
        if os.getenv('UT1_CELEBRITY_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['celebrity'] = UT1CelebrityCrawler()
        if os.getenv('UT1_CHAT_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['chat'] = UT1ChatCrawler()
        if os.getenv('UT1_CHILD_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['child'] = UT1ChildCrawler()
        if os.getenv('UT1_CLEANING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['cleaning'] = UT1CleaningCrawler()
        if os.getenv('UT1_COOKING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['cooking'] = UT1CookingCrawler()
        if os.getenv('UT1_CRYPTOJACKING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['cryptojacking'] = UT1CryptojackingCrawler()
        if os.getenv('UT1_DANGEROUS_MATERIAL_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['dangerous_material'] = UT1DangerousMaterialCrawler()
        if os.getenv('UT1_DATING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['dating'] = UT1DatingCrawler()
        if os.getenv('UT1_DDOS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['ddos'] = UT1DDoSCrawler()
        if os.getenv('UT1_DIALER_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['dialer'] = UT1DialerCrawler()
        if os.getenv('UT1_DOH_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['doh'] = UT1DoHCrawler()
        if os.getenv('UT1_DOWNLOAD_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['download'] = UT1DownloadCrawler()
        if os.getenv('UT1_DROGUE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['drogue'] = UT1DrogueCrawler()
        if os.getenv('UT1_DYNAMIC_DNS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['dynamic_dns'] = UT1DynamicDNSCrawler()
        if os.getenv('UT1_EDUCATIONAL_GAMES_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['educational_games'] = UT1EducationalGamesCrawler()
        if os.getenv('UT1_EXAMEN_PIX_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['examen_pix'] = UT1ExamenPixCrawler()
        if os.getenv('UT1_FAKENEWS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['fakenews'] = UT1FakenewsCrawler()
        if os.getenv('UT1_FILEHOSTING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['filehosting'] = UT1FilehostingCrawler()
        if os.getenv('UT1_FINANCIAL_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['financial'] = UT1FinancialCrawler()
        if os.getenv('UT1_FORUMS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['forums'] = UT1ForumsCrawler()
        if os.getenv('UT1_GAMBLING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['gambling'] = UT1GamblingCrawler()
        if os.getenv('UT1_GAMES_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['games'] = UT1GamesCrawler()
        if os.getenv('UT1_HACKING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['hacking'] = UT1HackingCrawler()
        if os.getenv('UT1_JOBSEARCH_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['jobsearch'] = UT1JobsearchCrawler()
        if os.getenv('UT1_LINGERIE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['lingerie'] = UT1LingerieCrawler()
        if os.getenv('UT1_LISTE_BU_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['liste_bu'] = UT1ListeBuCrawler()
        if os.getenv('UT1_MALWARE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['malware'] = UT1MalwareCrawler()
        if os.getenv('UT1_MANGA_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['manga'] = UT1MangaCrawler()
        if os.getenv('UT1_MARKETINGWARE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['marketingware'] = UT1MarketingwareCrawler()
        if os.getenv('UT1_MIXED_ADULT_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['mixed_adult'] = UT1MixedAdultCrawler()
        if os.getenv('UT1_MOBILE_PHONE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['mobile_phone'] = UT1MobilePhoneCrawler()
        if os.getenv('UT1_PHISHING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['phishing'] = UT1PhishingCrawler()
        if os.getenv('UT1_PRESS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['press'] = UT1PressCrawler()
        if os.getenv('UT1_PUBLICITE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['publicite'] = UT1PubliciteCrawler()
        if os.getenv('UT1_RADIO_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['radio'] = UT1RadioCrawler()
        if os.getenv('UT1_REAFFECTED_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['reaffected'] = UT1ReaffectedCrawler()
        if os.getenv('UT1_REDIRECTOR_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['redirector'] = UT1RedirectorCrawler()
        if os.getenv('UT1_REMOTE_CONTROL_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['remote_control'] = UT1RemoteControlCrawler()
        if os.getenv('UT1_RESIDENTIAL_PROXIES_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['residential_proxies'] = UT1ResidentialProxiesCrawler()
        if os.getenv('UT1_SECT_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['sect'] = UT1SectCrawler()
        if os.getenv('UT1_SEXUAL_EDUCATION_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['sexual_education'] = UT1SexualEducationCrawler()
        if os.getenv('UT1_SHOPPING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['shopping'] = UT1ShoppingCrawler()
        if os.getenv('UT1_SHORTENER_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['shortener'] = UT1ShortenerCrawler()
        if os.getenv('UT1_SOCIAL_NETWORKS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['social_networks'] = UT1SocialNetworksCrawler()
        if os.getenv('UT1_SPORTS_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['sports'] = UT1SportsCrawler()
        if os.getenv('UT1_STALKERWARE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['stalkerware'] = UT1StalkerwareCrawler()
        if os.getenv('UT1_STRICT_REDIRECTOR_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['strict_redirector'] = UT1StrictRedirectorCrawler()
        if os.getenv('UT1_STRONG_REDIRECTOR_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['strong_redirector'] = UT1StrongRedirectorCrawler()
        if os.getenv('UT1_TRANSLATION_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['translation'] = UT1TranslationCrawler()
        if os.getenv('UT1_TRICHEUR_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['tricheur'] = UT1TricheurCrawler()
        if os.getenv('UT1_TRICHEUR_PIX_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['tricheur_pix'] = UT1TricheurPixCrawler()
        if os.getenv('UT1_UPDATE_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['update'] = UT1UpdateCrawler()
        if os.getenv('UT1_VPN_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['vpn'] = UT1VPNCrawler()
        if os.getenv('UT1_WAREZ_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['warez'] = UT1WarezCrawler()
        if os.getenv('UT1_WEBHOSTING_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['webhosting'] = UT1WebhostingCrawler()
        if os.getenv('UT1_WEBMAIL_ENABLED', 'false').lower() == 'true':
            self.ut1_crawlers['webmail'] = UT1WebmailCrawler()
        self.logger.info("PhishScope initialized")
        self.logger.info(f"PhishTank interval: {self.phishtank_interval} hours")
        self.logger.info(f"OpenPhish interval: {self.openphish_interval} hours")
        self.logger.info(f"Phishing Army Blocklist interval: {self.phishing_army_interval} hours")
        self.logger.info(f"Black Mirror Blocklist interval: {self.black_mirror_interval} hours")
        self.logger.info(f"Phishunt.io interval: {self.phishunt_interval} hours")
        self.logger.info(f"PhishStats.info interval: {self.phishstats_interval} hours")
        self.logger.info(f"UT1 Blacklists interval: {self.ut1_interval} hours")
        self.logger.info(f"UT1 Enabled crawlers: {list(self.ut1_crawlers.keys())}")

    def setup_database(self):
        try:
            self.logger.info("Setting up database...")
            db_manager = DatabaseManager()
            if not db_manager.connect():
                self.logger.error("Failed to connect to database")
                return False
            if not db_manager.create_tables():
                self.logger.error("Failed to create database tables")
                return False
            db_manager.disconnect()
            self.logger.info("Database setup completed")
            return True
        except Exception as e:
            self.logger.error(f"Database setup failed: {e}")
            return False
    
    def run_phishtank_crawler(self):
        try:
            self.logger.info("Scheduled PhishTank crawler execution")
            start_time = time.time()
            success = self.phishtank_crawler.run()
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                self.logger.info(f"PhishTank crawler completed successfully in {duration:.2f}s")
            else:
                self.logger.error(f"PhishTank crawler failed after {duration:.2f}s")
        except Exception as e:
            self.logger.error(f"PhishTank crawler execution error: {e}")
    
    def run_openphish_crawler(self):
        try:
            self.logger.info("Scheduled OpenPhish crawler execution")
            start_time = time.time()
            success = self.openphish_crawler.run()
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                self.logger.info(f"OpenPhish crawler completed successfully in {duration:.2f}s")
            else:
                self.logger.error(f"OpenPhish crawler failed after {duration:.2f}s")
        except Exception as e:
            self.logger.error(f"OpenPhish crawler execution error: {e}")
            
    def run_phishing_army_blocklist_crawler(self):
        try:
            self.logger.info("Scheduled Phishing Army Blocklist crawler execution")
            start_time = time.time()
            
            army_crawler = PhishingArmyBlocklistCrawler()
            urls = army_crawler.fetch_blocklist()
            
            if urls:
                success = army_crawler.process_data(urls)
                end_time = time.time()
                duration = end_time - start_time
                
                if success:
                    self.logger.info(f"Phishing Army Blocklist crawler completed successfully in {duration:.2f}s")
                else:
                    self.logger.error(f"Phishing Army Blocklist crawler failed to process data after {duration:.2f}s")
            else:
                self.logger.error("No URLs fetched from Phishing Army Blocklist")
        except Exception as e:
            self.logger.error(f"Phishing Army Blocklist crawler execution error: {e}")
    
    def run_black_mirror_blocklist_crawler(self):
        try:
            self.logger.info("Scheduled Black Mirror Blocklist crawler execution")
            black_mirror_crawler = BlackMirrorBlocklistCrawler()
            domains = black_mirror_crawler.fetch_blocklist()
            if domains:
                success = black_mirror_crawler.process_data(domains)
                if success:
                    self.logger.info("Black Mirror Blocklist crawler completed successfully")
                else:
                    self.logger.error("Black Mirror Blocklist crawler failed to process data")
            else:
                self.logger.error("No domains fetched from Black Mirror Blocklist")
        except Exception as e:
            self.logger.error(f"Black Mirror Blocklist crawler execution error: {e}")
    
    def run_phishunt_crawler(self):
        try:
            self.logger.info("Scheduled Phishunt.io crawler execution")
            start_time = time.time()
            
            phishunt_crawler = PhishuntCrawler()
            success = phishunt_crawler.run()
            
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                self.logger.info(f"Phishunt.io crawler completed successfully in {duration:.2f}s")
            else:
                self.logger.error(f"Phishunt.io crawler failed after {duration:.2f}s")
        except Exception as e:
            self.logger.error(f"Phishunt.io crawler execution error: {e}")
    
    def run_phishstats_crawler(self):
        try:
            self.logger.info("Scheduled PhishStats.info crawler execution")
            start_time = time.time()
            
            phishstats_crawler = PhishStatsCrawler()
            success = phishstats_crawler.run()
            
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                self.logger.info(f"PhishStats.info crawler completed successfully in {duration:.2f}s")
            else:
                self.logger.error(f"PhishStats.info crawler failed after {duration:.2f}s")
        except Exception as e:
            self.logger.error(f"PhishStats.info crawler execution error: {e}")
    
    def run_ut1_crawlers(self):
        try:
            self.logger.info("Scheduled UT1 Blacklists crawler execution")
            
            if not self.ut1_crawlers:
                self.logger.warning("No UT1 crawlers enabled")
                return
            
            success_count = 0
            total_crawlers = len(self.ut1_crawlers)
            max_workers = min(10, total_crawlers)
            self.logger.info(f"Running {total_crawlers} UT1 crawlers with {max_workers} threads")
            
            def run_single_ut1_crawler(category_crawler_pair):
                category, crawler = category_crawler_pair
                try:
                    self.logger.info(f"Starting UT1 {category} crawler in thread")
                    start_time = time.time()
                    success = crawler.run()
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    if success:
                        self.logger.info(f"UT1 {category} crawler completed successfully in {duration:.2f}s")
                        return True, category, duration
                    else:
                        self.logger.error(f"UT1 {category} crawler failed after {duration:.2f}s")
                        return False, category, duration
                        
                except Exception as e:
                    self.logger.error(f"UT1 {category} crawler execution error: {e}")
                    return False, category, 0
            
            start_time = time.time()
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_category = {
                    executor.submit(run_single_ut1_crawler, (category, crawler)): category
                    for category, crawler in self.ut1_crawlers.items()
                }
                
                for future in as_completed(future_to_category):
                    category = future_to_category[future]
                    try:
                        success, crawler_category, duration = future.result()
                        if success:
                            success_count += 1
                    except Exception as e:
                        self.logger.error(f"UT1 {category} crawler thread exception: {e}")
            
            end_time = time.time()
            total_duration = end_time - start_time
            
            self.logger.info(f"UT1 Blacklists execution completed in {total_duration:.2f}s:")
            self.logger.info(f"  - Successful: {success_count}/{total_crawlers}")
            self.logger.info(f"  - Failed: {total_crawlers - success_count}/{total_crawlers}")
            self.logger.info(f"  - Average time per crawler: {total_duration/max_workers:.2f}s")
            
        except Exception as e:
            self.logger.error(f"UT1 Blacklists crawler execution error: {e}")
    
    def run_all_crawlers(self):
        self.logger.info("Running all crawlers manually with multi-threading...")
        start_time = time.time()
        
        # Define crawler tasks
        crawler_tasks = [
            ("PhishTank", self.run_phishtank_crawler),
            ("OpenPhish", self.run_openphish_crawler),
            ("Phishing Army", self.run_phishing_army_blocklist_crawler),
            ("Black Mirror", self.run_black_mirror_blocklist_crawler),
            ("Phishunt.io", self.run_phishunt_crawler),
            ("PhishStats.info", self.run_phishstats_crawler)
        ]
        
        def run_crawler_task(task_info):
            name, crawler_func = task_info
            try:
                self.logger.info(f"Starting {name} crawler in thread")
                task_start = time.time()
                crawler_func()
                task_end = time.time()
                duration = task_end - task_start
                self.logger.info(f"{name} crawler completed in {duration:.2f}s")
                return True, name, duration
            except Exception as e:
                self.logger.error(f"{name} crawler failed: {e}")
                return False, name, 0
        success_count = 0
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_to_crawler = {
                executor.submit(run_crawler_task, task): task[0]
                for task in crawler_tasks
            }
            
            for future in as_completed(future_to_crawler):
                crawler_name = future_to_crawler[future]
                try:
                    success, name, duration = future.result()
                    if success:
                        success_count += 1
                except Exception as e:
                    self.logger.error(f"{crawler_name} thread exception: {e}")
        if self.ut1_crawlers:
            self.run_ut1_crawlers()
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        self.logger.info(f"Manual crawler execution completed in {total_duration:.2f}s")
        self.logger.info(f"Main crawlers successful: {success_count}/{len(crawler_tasks)}")
    
    def setup_scheduler(self):
        try:
            schedule.every(self.phishtank_interval).hours.do(self.run_phishtank_crawler)
            schedule.every(self.openphish_interval).hours.do(self.run_openphish_crawler)
            schedule.every(self.phishing_army_interval).hours.do(self.run_phishing_army_blocklist_crawler)
            schedule.every(self.black_mirror_interval).hours.do(self.run_black_mirror_blocklist_crawler)
            schedule.every(self.phishunt_interval).hours.do(self.run_phishunt_crawler)
            schedule.every(self.phishstats_interval).hours.do(self.run_phishstats_crawler)
            
            if self.ut1_crawlers:
                schedule.every(self.ut1_interval).hours.do(self.run_ut1_crawlers)
            
            self.logger.info("Scheduler setup completed")
            self.logger.info(f"PhishTank will run every {self.phishtank_interval} hours")
            self.logger.info(f"OpenPhish will run every {self.openphish_interval} hours")
            self.logger.info(f"Phishing Army Blocklist will run every {self.phishing_army_interval} hours")
            self.logger.info(f"Black Mirror Blocklist will run every {self.black_mirror_interval} hours")
            self.logger.info(f"Phishunt.io will run every {self.phishunt_interval} hours")
            self.logger.info(f"PhishStats.info will run every {self.phishstats_interval} hours")
            
            if self.ut1_crawlers:
                self.logger.info(f"UT1 Blacklists will run every {self.ut1_interval} hours")
                self.logger.info(f"UT1 Enabled categories: {list(self.ut1_crawlers.keys())}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Scheduler setup failed: {e}")
            return False
    
    def run_scheduler(self):
        def scheduler_worker():
            while True:
                schedule.run_pending()
                time.sleep(60) 
        
        scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
        scheduler_thread.start()
        self.logger.info("Scheduler started in background thread")
    
    def start(self):
        try:
            self.logger.info("=== PhishScope Starting ===")
            if not self.setup_database():
                return False
            if not self.setup_scheduler():
                return False
            self.logger.info("Running initial data collection...")
            self.run_all_crawlers()
            self.run_scheduler()
            self.logger.info("=== PhishScope Started Successfully ===")
            self.logger.info("Press Ctrl+C to stop the crawler")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Received shutdown signal")
                return True
            
        except Exception as e:
            self.logger.error(f"Crawler startup failed: {e}")
            return False

def main():
    crawler = PhishingCrawler()
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'setup':
            crawler.setup_database()
        elif command == 'phishtank':
            crawler.setup_database()
            crawler.run_phishtank_crawler()
        elif command == 'openphish':
            crawler.setup_database()
            crawler.run_openphish_crawler()
        elif command == 'phishing_army':
            crawler.setup_database()
            crawler.run_phishing_army_blocklist_crawler()
        elif command == 'black_mirror':
            crawler.setup_database()
            crawler.run_black_mirror_blocklist_crawler()
        elif command == 'phishunt':
            crawler.setup_database()
            crawler.run_phishunt_crawler()
        elif command == 'phishstats':
            crawler.setup_database()
            crawler.run_phishstats_crawler()
        elif command == 'ut1':
            crawler.setup_database()
            if crawler.ut1_crawlers:
                crawler.run_ut1_crawlers()
            else:
                print("No UT1 crawlers enabled. Check your .env configuration.")
        elif command == 'ut1_adult':
            crawler.setup_database()
            if 'adult' in crawler.ut1_crawlers:
                crawler.ut1_crawlers['adult'].run()
            else:
                print("UT1 Adult crawler not enabled. Set UT1_ADULT_ENABLED=true in .env")
        elif command == 'ut1_phishing':
            crawler.setup_database()
            if 'phishing' in crawler.ut1_crawlers:
                crawler.ut1_crawlers['phishing'].run()
            else:
                print("UT1 PhishScope not enabled. Set UT1_PHISHING_ENABLED=true in .env")
        elif command == 'ut1_malware':
            crawler.setup_database()
            if 'malware' in crawler.ut1_crawlers:
                crawler.ut1_crawlers['malware'].run()
            else:
                print("UT1 Malware crawler not enabled. Set UT1_MALWARE_ENABLED=true in .env")
        elif command == 'ut1_ddos':
            crawler.setup_database()
            if 'ddos' in crawler.ut1_crawlers:
                success = crawler.ut1_crawlers['ddos'].run()
                print(f"UT1 DDoS crawler completed with result: {success}")
            else:
                print("UT1 DDoS crawler not enabled. Set UT1_DDOS_ENABLED=true in .env")
        elif command == 'once':
            crawler.setup_database()
            crawler.run_all_crawlers()
        else:
            print("Usage: python main.py [setup|phishtank|openphish|phishing_army|black_mirror|phishunt|phishstats|ut1|ut1_adult|ut1_phishing|ut1_malware|ut1_ddos|once]")
            print("  setup         - Setup database tables only")
            print("  phishtank     - Run PhishTank crawler once")
            print("  openphish     - Run OpenPhish crawler once")
            print("  phishing_army - Run Phishing Army Blocklist crawler once")
            print("  black_mirror  - Run Black Mirror Blocklist crawler once")
            print("  phishunt      - Run Phishunt.io crawler once")
            print("  phishstats    - Run PhishStats.info crawler once")
            print("  ut1           - Run all enabled UT1 blacklist crawlers once")
            print("  ut1_adult     - Run UT1 Adult category crawler once")
            print("  ut1_phishing  - Run UT1 Phishing category crawler once")
            print("  ut1_malware   - Run UT1 Malware category crawler once")
            print("  ut1_ddos      - Run UT1 DDoS category crawler once") 
            print("  once          - Run all crawlers once")
            print("  (no args)     - Start scheduled crawler service")
    else:
        crawler.start()

if __name__ == "__main__":
    main()
