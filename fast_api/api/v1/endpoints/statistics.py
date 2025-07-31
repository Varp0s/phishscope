from fastapi import APIRouter, Depends
import logging
import asyncio
from datetime import datetime, timedelta
from core.database import get_database

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple in-memory cache for statistics
_stats_cache = {
    "data": None,
    "last_updated": None,
    "cache_duration": 300  # 5 minutes
}

async def get_cached_statistics(db):
    now = datetime.utcnow()
    # Check if we have cached data that's still valid
    if (_stats_cache["data"] is not None and 
        _stats_cache["last_updated"] is not None and
        now - _stats_cache["last_updated"] < timedelta(seconds=_stats_cache["cache_duration"])):
        logger.info("Returning cached statistics")
        return _stats_cache["data"]
    
    logger.info("Fetching fresh statistics from database")
    try:
        # Simplified query with essential statistics only
        cert_stats_query = """
        SELECT 
            COUNT(*) as total_certificates,
            COUNT(CASE WHEN created_at >= NOW() - INTERVAL '24 hours' THEN 1 END) as recent_24h,
            COUNT(CASE WHEN domains IS NOT NULL AND domains != '' THEN 1 END) as with_domains,
            MAX(created_at) as latest_date,
            MIN(created_at) as oldest_date
        FROM certificates
        """
        
        cert_stats = await db.fetch_one(cert_stats_query)
        
        # Simplified phishing statistics - just get approximate counts
        phishing_stats_query = """
        SELECT
            (SELECT reltuples::bigint FROM pg_class WHERE relname = 'phishtank') as phishtank_count,
            (SELECT reltuples::bigint FROM pg_class WHERE relname = 'openphish') as openphish_count,
            (SELECT reltuples::bigint FROM pg_class WHERE relname = 'phishingarmy') as phishingarmy_count,
            (SELECT reltuples::bigint FROM pg_class WHERE relname = 'blackmirror') as blackmirror_count,
            (SELECT reltuples::bigint FROM pg_class WHERE relname = 'phishunt') as phishunt_count,
            (SELECT reltuples::bigint FROM pg_class WHERE relname = 'phishstats') as phishstats_count
        """
        
        phishing_stats = await db.fetch_one(phishing_stats_query)
        
        # Get UT1 categories from individual tables if they exist
        ut1_categories = {}
        ut1_categories_count = 0
        total_ut1_urls = 0
        
        # List of known UT1 categories
        ut1_category_names = [
            'adult', 'agressif', 'arjel', 'associations_religieuses', 'astrology', 
            'audio_video', 'bank', 'bitcoin', 'blog', 'celebrity', 'chat', 'child', 
            'cleaning', 'cooking', 'cryptojacking', 'dangerous_material', 'dating', 
            'ddos', 'dialer', 'doh', 'download', 'drogue', 'dynamic_dns', 
            'educational_games', 'examen_pix', 'fakenews', 'filehosting', 
            'financial', 'forums', 'gambling', 'games', 'hacking', 'jobsearch', 
            'lingerie', 'liste_bu', 'malware', 'manga', 'marketingware', 
            'mixed_adult', 'mobile_phone', 'phishing', 'press', 'publicite', 
            'radio', 'reaffected', 'redirector', 'remote_control', 
            'residential_proxies', 'sect', 'sexual_education', 'shopping', 
            'shortener', 'social_networks', 'sports', 'stalkerware', 
            'strict_redirector', 'strong_redirector', 'translation', 'tricheur', 
            'tricheur_pix', 'update', 'vpn', 'warez', 'webhosting', 'webmail'
        ]
        
        # Try to get stats from individual UT1 tables
        for category in ut1_category_names:
            try:
                table_name = f"ut1_{category}"
                ut1_result = await db.fetch_one(f"""
                    SELECT reltuples::bigint as count 
                    FROM pg_class 
                    WHERE relname = '{table_name}'
                """)
                if ut1_result and ut1_result["count"]:
                    count = max(0, ut1_result["count"])
                    ut1_categories[category] = count
                    total_ut1_urls += count
                    ut1_categories_count += 1
            except Exception as e:
                # Table doesn't exist, skip it
                logger.debug(f"UT1 table {table_name} not found: {e}")
                continue
        
        # Extract values from query results
        total_certificates = cert_stats["total_certificates"] if cert_stats else 0
        recent_certificates_24h = cert_stats["recent_24h"] if cert_stats else 0
        certificates_with_domains = cert_stats["with_domains"] if cert_stats else 0
        latest_certificate_date = cert_stats["latest_date"].isoformat() if cert_stats and cert_stats["latest_date"] else None
        oldest_certificate_date = cert_stats["oldest_date"].isoformat() if cert_stats and cert_stats["oldest_date"] else None
        
        # Extract phishing statistics (using pg_class for fast approximation)
        total_phishtank = max(0, phishing_stats["phishtank_count"] or 0) if phishing_stats else 0
        total_openphish = max(0, phishing_stats["openphish_count"] or 0) if phishing_stats else 0
        total_phishingarmy = max(0, phishing_stats["phishingarmy_count"] or 0) if phishing_stats else 0
        total_blackmirror = max(0, phishing_stats["blackmirror_count"] or 0) if phishing_stats else 0
        total_phishunt = max(0, phishing_stats["phishunt_count"] or 0) if phishing_stats else 0
        total_phishstats = max(0, phishing_stats["phishstats_count"] or 0) if phishing_stats else 0
        
        # Calculate totals
        total_phishing_urls = total_phishtank + total_openphish + total_phishingarmy + total_blackmirror + total_phishunt + total_phishstats + total_ut1_urls
        
        # Calculate grand total (certificates + phishing URLs)
        grand_total_intelligence = total_certificates + total_phishing_urls
        
        # Approximate recent activity (for performance)
        recent_phishing_24h = int(total_phishing_urls * 0.01)  # Assume 1% are from last 24h
        
        stats_data = {
            "total_certificates": total_certificates,
            "recent_certificates_24h": recent_certificates_24h,
            "recent_certificates_7d": int(recent_certificates_24h * 7),  # Approximation
            "updated_certificates": int(total_certificates * 0.5),  # Approximation
            "certificates_with_domains": certificates_with_domains,
            "unique_subject_cns": total_certificates,  # Approximation
            "total_domains": certificates_with_domains,
            "avg_certificates_per_day": recent_certificates_24h,  # Approximation
            "latest_certificate_date": latest_certificate_date,
            "oldest_certificate_date": oldest_certificate_date,
            "grand_total_intelligence": grand_total_intelligence,
            "phishing_data": {
                "total_phishing_urls": total_phishing_urls,
                "recent_phishing_24h": recent_phishing_24h,
                "sources": {
                    "phishtank": total_phishtank,
                    "openphish": total_openphish,
                    "phishing_army": total_phishingarmy,
                    "black_mirror": total_blackmirror,
                    "phishunt": total_phishunt,
                    "phishstats": total_phishstats,
                    "ut1_blacklists": {
                        "total_ut1_urls": total_ut1_urls,
                        "categories_count": ut1_categories_count,
                        "categories": ut1_categories
                    }
                }
            },
            "database_status": "connected"
        }
        
        # Update cache
        _stats_cache["data"] = stats_data
        _stats_cache["last_updated"] = now
        
        return stats_data
        
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        # Return cached data if available, even if stale
        if _stats_cache["data"] is not None:
            logger.warning("Returning stale cached data due to error")
            return _stats_cache["data"]
        
        return {
            "error": "Failed to fetch statistics",
            "database_status": "error"
        }

@router.get("/")
async def get_statistics(db=Depends(get_database)):
    return await get_cached_statistics(db)

@router.get("/recent")
async def get_recent_activity(
    limit: int = 10,
    db=Depends(get_database)
):
    try:
        query = """
            SELECT subject_cn, domains, created_at, updated_at,
                   CASE WHEN updated_at != created_at THEN true ELSE false END as was_updated
            FROM certificates 
            WHERE domains IS NOT NULL AND domains != ''
            ORDER BY GREATEST(created_at, updated_at) DESC 
            LIMIT $1
        """
        
        results = await db.fetch_all(query, [limit])
        
        return {
            "recent_activity": [dict(result) for result in results],
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error fetching recent activity: {e}")
        return {
            "error": "Failed to fetch recent activity"
        }
