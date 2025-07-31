import psycopg2
import psycopg2.extras
import logging
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'env', '.env'))

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            logging.info("Database connection established")
            return True
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Database connection closed")
    
    def is_connected(self):
        return self.connection is not None and not self.connection.closed
    
    def create_ut1_tables(self):
        ut1_categories = [
            'adult', 'phishing', 'malware', 'gambling', 'cryptojacking',
            'vpn', 'warez', 'redirector', 'shortener', 'ddos',
            'agressif', 'arjel', 'associations_religieuses', 'astrology', 'audio_video', 'bank',
            'bitcoin', 'blog', 'celebrity', 'chat', 'child', 'cleaning',
            'cooking', 'dangerous_material', 'dating', 'dialer',
            'doh', 'download', 'drogue', 'dynamic_dns', 'educational_games',
            'examen_pix', 'fakenews', 'filehosting', 'financial', 'forums', 'games', 'hacking',
            'jobsearch', 'lingerie', 'liste_bu', 'manga', 'marketingware',
            'mixed_adult', 'mobile_phone', 'press', 'publicite',
            'radio', 'reaffected', 'remote_control', 'residential_proxies', 'sect', 'sexual_education',
            'shopping', 'social_networks', 'sports', 'stalkerware',
            'strict_redirector', 'strong_redirector', 'translation',
            'tricheur', 'tricheur_pix', 'update', 'webhosting', 'webmail'
        ]
        
        for category in ut1_categories:
            table_name = f"ut1_{category}"
            table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            index_sql = f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_url ON {table_name}(url);
            CREATE INDEX IF NOT EXISTS idx_{table_name}_created_at ON {table_name}(created_at);
            """
            self.cursor.execute(table_sql)
            self.cursor.execute(index_sql)
    
    def create_tables(self):
        try:
            phishtank_table = """
            CREATE TABLE IF NOT EXISTS phishtank (
                id SERIAL PRIMARY KEY,
                phish_id BIGINT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                phish_detail_url TEXT,
                submission_time TIMESTAMP WITH TIME ZONE,
                verified VARCHAR(10),
                verification_time TIMESTAMP WITH TIME ZONE,
                online VARCHAR(10),
                target VARCHAR(100),
                ip_address INET,
                cidr_block VARCHAR(50),
                announcing_network VARCHAR(20),
                rir VARCHAR(20),
                country VARCHAR(10),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(phish_id),
                UNIQUE(url)
            );
            """
            
            openphish_table = """
            CREATE TABLE IF NOT EXISTS openphish (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """

            phishingarmy_table = """
            CREATE TABLE IF NOT EXISTS phishingarmy (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """

            blackmirror_table = """
            CREATE TABLE IF NOT EXISTS blackmirror (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """

            phishunt_table = """
            CREATE TABLE IF NOT EXISTS phishunt (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """

            phishstats_table = """
            CREATE TABLE IF NOT EXISTS phishstats (
                id SERIAL PRIMARY KEY,
                phishstats_id BIGINT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                ip_address INET,
                country_code VARCHAR(10),
                country_name VARCHAR(100),
                region_code VARCHAR(10),
                region_name VARCHAR(100),
                city VARCHAR(100),
                zipcode VARCHAR(20),
                latitude DECIMAL(10,8),
                longitude DECIMAL(11,8),
                asn VARCHAR(20),
                bgp VARCHAR(50),
                isp VARCHAR(200),
                title TEXT,
                date_detected TIMESTAMP WITH TIME ZONE,
                date_updated TIMESTAMP WITH TIME ZONE,
                hash_value VARCHAR(100),
                score DECIMAL(3,1),
                host VARCHAR(255),
                domain VARCHAR(255),
                tld VARCHAR(10),
                domain_registered_days_ago INTEGER,
                abuse_contact TEXT,
                ssl_issuer TEXT,
                ssl_subject TEXT,
                rank_host INTEGER,
                rank_domain INTEGER,
                times_seen_ip INTEGER,
                times_seen_host INTEGER,
                times_seen_domain INTEGER,
                http_code INTEGER,
                http_server VARCHAR(100),
                google_safebrowsing VARCHAR(10),
                virus_total VARCHAR(10),
                abuse_ch_malware VARCHAR(10),
                vulnerabilities TEXT,
                ports TEXT,
                os VARCHAR(100),
                tags TEXT,
                technology TEXT,
                page_text TEXT,
                ssl_fingerprint TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(phishstats_id),
                UNIQUE(url)
            );
            """
            
            phishtank_indexes = """
            CREATE INDEX IF NOT EXISTS idx_phishtank_phish_id ON phishtank(phish_id);
            CREATE INDEX IF NOT EXISTS idx_phishtank_url ON phishtank(url);
            CREATE INDEX IF NOT EXISTS idx_phishtank_created_at ON phishtank(created_at);
            """
            
            openphish_indexes = """
            CREATE INDEX IF NOT EXISTS idx_openphish_url ON openphish(url);
            CREATE INDEX IF NOT EXISTS idx_openphish_created_at ON openphish(created_at);
            """

            phishingarmy_indexes = """
            CREATE INDEX IF NOT EXISTS idx_phishingarmy_url ON phishingarmy(url);
            CREATE INDEX IF NOT EXISTS idx_phishingarmy_created_at ON phishingarmy(created_at);
            """

            blackmirror_indexes = """
            CREATE INDEX IF NOT EXISTS idx_blackmirror_url ON blackmirror(url);
            CREATE INDEX IF NOT EXISTS idx_blackmirror_created_at ON blackmirror(created_at);
            """

            phishunt_indexes = """
            CREATE INDEX IF NOT EXISTS idx_phishunt_url ON phishunt(url);
            CREATE INDEX IF NOT EXISTS idx_phishunt_created_at ON phishunt(created_at);
            """

            phishstats_indexes = """
            CREATE INDEX IF NOT EXISTS idx_phishstats_phishstats_id ON phishstats(phishstats_id);
            CREATE INDEX IF NOT EXISTS idx_phishstats_url ON phishstats(url);
            CREATE INDEX IF NOT EXISTS idx_phishstats_created_at ON phishstats(created_at);
            CREATE INDEX IF NOT EXISTS idx_phishstats_date_detected ON phishstats(date_detected);
            CREATE INDEX IF NOT EXISTS idx_phishstats_score ON phishstats(score);
            CREATE INDEX IF NOT EXISTS idx_phishstats_host ON phishstats(host);
            CREATE INDEX IF NOT EXISTS idx_phishstats_domain ON phishstats(domain);
            """

            self.cursor.execute(phishtank_table)
            self.cursor.execute(openphish_table)
            self.cursor.execute(phishingarmy_table)
            self.cursor.execute(blackmirror_table)
            self.cursor.execute(phishunt_table)
            self.cursor.execute(phishstats_table)
            
            # Create UT1 tables
            self.create_ut1_tables()
            
            self.cursor.execute(phishtank_indexes)
            self.cursor.execute(openphish_indexes)
            self.cursor.execute(phishingarmy_indexes)
            self.cursor.execute(blackmirror_indexes)
            self.cursor.execute(phishunt_indexes)
            self.cursor.execute(phishstats_indexes)

            self.connection.commit()
            logging.info("Database tables created successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            self.connection.rollback()
            return False
    
    def check_phishtank_duplicate(self, phish_id, url):
        try:
            check_query = """
            SELECT id FROM phishtank 
            WHERE phish_id = %s OR url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (phish_id, url))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking PhishTank duplicate: {e}")
            return False
    
    def check_openphish_duplicate(self, url):
        try:
            check_query = """
            SELECT id FROM openphish 
            WHERE url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (url,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking OpenPhish duplicate: {e}")
            return False
        
    def check_phishingarmy_duplicate(self, url):
        try:
            check_query = """
            SELECT id FROM phishingarmy 
            WHERE url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (url,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking Phishing Army duplicate: {e}")
            return False

    def check_blackmirror_duplicate(self, url):
        try:
            check_query = """
            SELECT id FROM blackmirror 
            WHERE url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (url,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking Black Mirror duplicate: {e}")
            return False

    def check_phishunt_duplicate(self, url):
        try:
            check_query = """
            SELECT id FROM phishunt 
            WHERE url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (url,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking Phishunt duplicate: {e}")
            return False

    def check_ut1_duplicate(self, table_name, url):
        try:
            check_query = f"""
            SELECT id FROM {table_name} 
            WHERE url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (url,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking UT1 {table_name} duplicate: {e}")
            return False

    def insert_phishtank_data(self, data):
        try:
            insert_query = """
            INSERT INTO phishtank (
                phish_id, url, phish_detail_url, submission_time, verified, 
                verification_time, online, target, ip_address, cidr_block, 
                announcing_network, rir, country
            ) VALUES (
                %(phish_id)s, %(url)s, %(phish_detail_url)s, %(submission_time)s, 
                %(verified)s, %(verification_time)s, %(online)s, %(target)s, 
                %(ip_address)s, %(cidr_block)s, %(announcing_network)s, %(rir)s, %(country)s
            ) ON CONFLICT (phish_id) DO UPDATE SET
                url = EXCLUDED.url,
                verified = EXCLUDED.verified,
                verification_time = EXCLUDED.verification_time,
                online = EXCLUDED.online,
                target = EXCLUDED.target,
                ip_address = EXCLUDED.ip_address,
                cidr_block = EXCLUDED.cidr_block,
                announcing_network = EXCLUDED.announcing_network,
                rir = EXCLUDED.rir,
                country = EXCLUDED.country,
                updated_at = NOW()
            """
            
            ip_address = None
            cidr_block = None
            announcing_network = None
            rir = None
            country = None
            
            if data.get('details') and len(data['details']) > 0:
                detail = data['details'][0]
                ip_address = detail.get('ip_address')
                cidr_block = detail.get('cidr_block')
                announcing_network = detail.get('announcing_network')
                rir = detail.get('rir')
                country = detail.get('country')
            
            if not data.get('phish_id') or not data.get('url'):
                logging.error(f"Missing required fields in record: {data}")
                return False
                
            url = data.get('url', '')[:2000] 
            target = data.get('target', '')[:100] if data.get('target') else None
            
            record = {
                'phish_id': data.get('phish_id'),
                'url': url,
                'phish_detail_url': data.get('phish_detail_url'),
                'submission_time': data.get('submission_time'),
                'verified': data.get('verified'),
                'verification_time': data.get('verification_time'),
                'online': data.get('online'),
                'target': target,
                'ip_address': ip_address,
                'cidr_block': cidr_block,
                'announcing_network': announcing_network,
                'rir': rir,
                'country': country
            }
            
            if self.check_phishtank_duplicate(data.get('phish_id'), url):
                logging.warning(f"Duplicate PhishTank record found, skipping insertion: {data.get('phish_id')}")
                return False
            self.cursor.execute(insert_query, record)
            return True
            
        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting PhishTank data (likely duplicate): {e}")
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting PhishTank data: {e}")
            return False
        except Exception as e:
            logging.error(f"Error inserting PhishTank data: {e}")
            return False
    
    def insert_openphish_data(self, url):
        try:
            if not url or len(url) > 2000:
                logging.warning(f"Invalid URL length or empty URL: {url}")
                return False
                
            if self.check_openphish_duplicate(url):
                logging.warning(f"Duplicate OpenPhish URL found, skipping insertion: {url}")
                return False
                
            insert_query = """
            INSERT INTO openphish (url) 
            VALUES (%s) 
            ON CONFLICT (url) DO UPDATE SET
                updated_at = NOW()
            """
            self.cursor.execute(insert_query, (url,))
            return True
            
        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting OpenPhish data (likely duplicate): {e}")
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting OpenPhish data: {e}")
            return False
        except Exception as e:
            logging.error(f"Error inserting OpenPhish data: {e}")
            return False
        
    def insert_phishingarmy_data(self, url):
        try:
            if not url or len(url) > 2000:
                logging.warning(f"Invalid URL length or empty URL: {url}")
                return False

            if self.check_phishingarmy_duplicate(url):
                logging.warning(f"Duplicate Phishing Army URL found, skipping insertion: {url}")
                return False

            insert_query = """
            INSERT INTO phishingarmy (url) 
            VALUES (%s) 
            ON CONFLICT (url) DO UPDATE SET
                updated_at = NOW()
            """
            self.cursor.execute(insert_query, (url,))
            self.commit()
            return True

        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting Phishing Army data (likely duplicate): {e}")
            self.rollback()
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting Phishing Army data: {e}")
            self.rollback()
            return False
        except Exception as e:
            logging.error(f"Error inserting Phishing Army data: {e}")
            self.rollback()
            return False
    
    def insert_blackmirror_data(self, url):
        try:
            if not url or len(url) > 2000:
                logging.warning(f"Invalid URL length or empty URL: {url}")
                return False

            if self.check_blackmirror_duplicate(url):
                logging.warning(f"Duplicate Black Mirror URL found, skipping insertion: {url}")
                return False

            insert_query = """
            INSERT INTO blackmirror (url) 
            VALUES (%s) 
            ON CONFLICT (url) DO UPDATE SET
                updated_at = NOW()
            """
            self.cursor.execute(insert_query, (url,))
            self.commit()
            return True

        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting Black Mirror data (likely duplicate): {e}")
            self.rollback()
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting Black Mirror data: {e}")
            self.rollback()
            return False
        except Exception as e:
            logging.error(f"Error inserting Black Mirror data: {e}")
            self.rollback()
            return False
    
    def insert_phishunt_url(self, url):
        try:
            if not url or len(url) > 2000:
                logging.warning(f"Invalid URL length or empty URL: {url}")
                return False

            if self.check_phishunt_duplicate(url):
                logging.warning(f"Duplicate Phishunt URL found, skipping insertion: {url}")
                return False

            insert_query = """
            INSERT INTO phishunt (url) 
            VALUES (%s) 
            ON CONFLICT (url) DO UPDATE SET
                updated_at = NOW()
            """
            self.cursor.execute(insert_query, (url,))
            self.commit()
            return True

        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting Phishunt data (likely duplicate): {e}")
            self.rollback()
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting Phishunt data: {e}")
            self.rollback()
            return False
        except Exception as e:
            logging.error(f"Error inserting Phishunt data: {e}")
            self.rollback()
            return False
    
    def insert_ut1_data(self, table_name, url):
        try:
            if not url or len(url) > 2000:
                logging.warning(f"Invalid URL length or empty URL: {url}")
                return False

            if self.check_ut1_duplicate(table_name, url):
                logging.warning(f"Duplicate UT1 {table_name} URL found, skipping insertion: {url}")
                return False

            insert_query = f"""
            INSERT INTO {table_name} (url) 
            VALUES (%s) 
            ON CONFLICT (url) DO UPDATE SET
                updated_at = NOW()
            """
            self.cursor.execute(insert_query, (url,))
            self.commit()
            return True

        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting UT1 {table_name} data (likely duplicate): {e}")
            self.rollback()
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting UT1 {table_name} data: {e}")
            self.rollback()
            return False
        except Exception as e:
            logging.error(f"Error inserting UT1 {table_name} data: {e}")
            self.rollback()
            return False
    
    def check_phishstats_duplicate(self, phishstats_id, url):
        try:
            check_query = """
            SELECT id FROM phishstats 
            WHERE phishstats_id = %s OR url = %s
            LIMIT 1
            """
            self.cursor.execute(check_query, (phishstats_id, url))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Error checking PhishStats duplicate: {e}")
            return False

    def insert_phishstats_data(self, data):
        try:
            # Data validation
            if not data.get('id') or not data.get('url'):
                logging.warning("Invalid PhishStats data: missing id or url")
                return False

            if len(data.get('url', '')) > 2000:
                logging.warning(f"URL too long: {data.get('url', '')}")
                return False

            if self.check_phishstats_duplicate(data['id'], data['url']):
                logging.warning(f"Duplicate PhishStats data found, skipping insertion: {data['url']}")
                return False

            insert_query = """
            INSERT INTO phishstats (
                phishstats_id, url, ip_address, country_code, country_name,
                region_code, region_name, city, zipcode, latitude, longitude,
                asn, bgp, isp, title, date_detected, date_updated, hash_value,
                score, host, domain, tld, domain_registered_days_ago,
                abuse_contact, ssl_issuer, ssl_subject, rank_host, rank_domain,
                times_seen_ip, times_seen_host, times_seen_domain, http_code,
                http_server, google_safebrowsing, virus_total, abuse_ch_malware,
                vulnerabilities, ports, os, tags, technology, page_text,
                ssl_fingerprint
            ) VALUES (
                %(phishstats_id)s, %(url)s, %(ip_address)s, %(country_code)s, %(country_name)s,
                %(region_code)s, %(region_name)s, %(city)s, %(zipcode)s, %(latitude)s, %(longitude)s,
                %(asn)s, %(bgp)s, %(isp)s, %(title)s, %(date_detected)s, %(date_updated)s, %(hash_value)s,
                %(score)s, %(host)s, %(domain)s, %(tld)s, %(domain_registered_days_ago)s,
                %(abuse_contact)s, %(ssl_issuer)s, %(ssl_subject)s, %(rank_host)s, %(rank_domain)s,
                %(times_seen_ip)s, %(times_seen_host)s, %(times_seen_domain)s, %(http_code)s,
                %(http_server)s, %(google_safebrowsing)s, %(virus_total)s, %(abuse_ch_malware)s,
                %(vulnerabilities)s, %(ports)s, %(os)s, %(tags)s, %(technology)s, %(page_text)s,
                %(ssl_fingerprint)s
            ) ON CONFLICT (phishstats_id) DO UPDATE SET
                url = EXCLUDED.url,
                ip_address = EXCLUDED.ip_address,
                country_code = EXCLUDED.country_code,
                country_name = EXCLUDED.country_name,
                region_code = EXCLUDED.region_code,
                region_name = EXCLUDED.region_name,
                city = EXCLUDED.city,
                zipcode = EXCLUDED.zipcode,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                asn = EXCLUDED.asn,
                bgp = EXCLUDED.bgp,
                isp = EXCLUDED.isp,
                title = EXCLUDED.title,
                date_detected = EXCLUDED.date_detected,
                date_updated = EXCLUDED.date_updated,
                hash_value = EXCLUDED.hash_value,
                score = EXCLUDED.score,
                host = EXCLUDED.host,
                domain = EXCLUDED.domain,
                tld = EXCLUDED.tld,
                domain_registered_days_ago = EXCLUDED.domain_registered_days_ago,
                abuse_contact = EXCLUDED.abuse_contact,
                ssl_issuer = EXCLUDED.ssl_issuer,
                ssl_subject = EXCLUDED.ssl_subject,
                rank_host = EXCLUDED.rank_host,
                rank_domain = EXCLUDED.rank_domain,
                times_seen_ip = EXCLUDED.times_seen_ip,
                times_seen_host = EXCLUDED.times_seen_host,
                times_seen_domain = EXCLUDED.times_seen_domain,
                http_code = EXCLUDED.http_code,
                http_server = EXCLUDED.http_server,
                google_safebrowsing = EXCLUDED.google_safebrowsing,
                virus_total = EXCLUDED.virus_total,
                abuse_ch_malware = EXCLUDED.abuse_ch_malware,
                vulnerabilities = EXCLUDED.vulnerabilities,
                ports = EXCLUDED.ports,
                os = EXCLUDED.os,
                tags = EXCLUDED.tags,
                technology = EXCLUDED.technology,
                page_text = EXCLUDED.page_text,
                ssl_fingerprint = EXCLUDED.ssl_fingerprint,
                updated_at = NOW()
            """

            # Process the data to handle None values and conversions
            processed_data = {
                'phishstats_id': data['id'],
                'url': data['url'],
                'ip_address': data.get('ip'),
                'country_code': data.get('countrycode'),
                'country_name': data.get('countryname'),
                'region_code': data.get('regioncode'),
                'region_name': data.get('regionname'),
                'city': data.get('city'),
                'zipcode': data.get('zipcode'),
                'latitude': float(data['latitude']) if data.get('latitude') and data['latitude'] != '0.0000' else None,
                'longitude': float(data['longitude']) if data.get('longitude') and data['longitude'] != '0.0000' else None,
                'asn': data.get('asn'),
                'bgp': data.get('bgp'),
                'isp': data.get('isp'),
                'title': data.get('title'),
                'date_detected': data.get('date'),
                'date_updated': data.get('date_update'),
                'hash_value': data.get('hash'),
                'score': float(data['score']) if data.get('score') else None,
                'host': data.get('host'),
                'domain': data.get('domain'),
                'tld': data.get('tld'),
                'domain_registered_days_ago': data.get('domain_registered_n_days_ago'),
                'abuse_contact': data.get('abuse_contact'),
                'ssl_issuer': data.get('ssl_issuer'),
                'ssl_subject': data.get('ssl_subject'),
                'rank_host': data.get('rank_host'),
                'rank_domain': data.get('rank_domain'),
                'times_seen_ip': data.get('n_times_seen_ip'),
                'times_seen_host': data.get('n_times_seen_host'),
                'times_seen_domain': data.get('n_times_seen_domain'),
                'http_code': data.get('http_code'),
                'http_server': data.get('http_server'),
                'google_safebrowsing': data.get('google_safebrowsing'),
                'virus_total': data.get('virus_total'),
                'abuse_ch_malware': data.get('abuse_ch_malware'),
                'vulnerabilities': data.get('vulns'),
                'ports': data.get('ports'),
                'os': data.get('os'),
                'tags': data.get('tags'),
                'technology': data.get('technology'),
                'page_text': data.get('page_text'),
                'ssl_fingerprint': data.get('ssl_fingerprint')
            }

            self.cursor.execute(insert_query, processed_data)
            self.commit()
            return True

        except psycopg2.IntegrityError as e:
            logging.warning(f"Integrity error inserting PhishStats data (likely duplicate): {e}")
            self.rollback()
            return False
        except psycopg2.DataError as e:
            logging.error(f"Data error inserting PhishStats data: {e}")
            self.rollback()
            return False
        except Exception as e:
            logging.error(f"Error inserting PhishStats data: {e}")
            self.rollback()
            return False

    def commit(self):
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        if self.connection:
            self.connection.rollback()
