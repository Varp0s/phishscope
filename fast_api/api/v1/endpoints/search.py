from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
import logging
from core.database import get_database

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def universal_search(
    q: str = Query(..., description="Search query - can be URL, keyword, domain, or certificate info", min_length=2),
    sources: Optional[List[str]] = Query(None, description="Filter by specific sources (phishtank, openphish, phishingarmy, blackmirror, phishunt, phishstats, ut1, certificates)"),
    limit: int = Query(100, description="Maximum number of results", ge=1, le=1000),
    offset: int = Query(0, description="Number of results to skip", ge=0),
    db=Depends(get_database)
):
    try:
        # Available sources and their table names
        available_sources = {
            'phishtank': 'phishtank',
            'openphish': 'openphish', 
            'phishingarmy': 'phishingarmy',
            'blackmirror': 'blackmirror',
            'phishunt': 'phishunt',
            'phishstats': 'phishstats',
            'certificates': 'certificates'
        }
        
        # UT1 categories
        ut1_categories = [
            'adult', 'agressif', 'arjel', 'associations_religieuses', 'astrology', 'audio_video', 
            'bank', 'bitcoin', 'blog', 'celebrity', 'chat', 'child', 'cleaning', 'cooking', 
            'cryptojacking', 'dangerous_material', 'dating', 'ddos', 'dialer', 'doh', 'download', 
            'drogue', 'dynamic_dns', 'educational_games', 'examen_pix', 'fakenews', 'filehosting', 
            'financial', 'forums', 'gambling', 'games', 'hacking', 'jobsearch', 'lingerie', 
            'liste_bu', 'malware', 'manga', 'marketingware', 'mixed_adult', 'mobile_phone', 
            'phishing', 'press', 'publicite', 'radio', 'reaffected', 'redirector', 'remote_control', 
            'residential_proxies', 'sect', 'sexual_education', 'shopping', 'shortener', 
            'social_networks', 'sports', 'stalkerware', 'strict_redirector', 'strong_redirector', 
            'translation', 'tricheur', 'tricheur_pix', 'update', 'vpn', 'warez', 'webhosting', 'webmail'
        ]
        
        # Add UT1 tables to available sources
        for category in ut1_categories:
            available_sources[f'ut1_{category}'] = f'ut1_{category}'
        
        # Filter sources if specified
        tables_to_search = available_sources
        if sources:
            # Validate sources
            invalid_sources = []
            valid_sources = {}
            
            for source in sources:
                if source == 'ut1':
                    # Include all UT1 categories
                    for category in ut1_categories:
                        valid_sources[f'ut1_{category}'] = f'ut1_{category}'
                elif source in available_sources:
                    valid_sources[source] = available_sources[source]
                else:
                    invalid_sources.append(source)
            
            if invalid_sources:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": f"Invalid sources: {invalid_sources}",
                        "available_sources": list(available_sources.keys()) + ['ut1']
                    }
                )
            
            tables_to_search = valid_sources
        
        # Prepare search patterns
        search_results = []
        search_pattern = f"%{q}%"
        
        # Clean query for domain detection
        clean_q = q.replace('http://', '').replace('https://', '').split('/')[0]
        domain_pattern = f"%{clean_q}%"
        
        for source_name, table_name in tables_to_search.items():
            try:
                # Different queries for different table structures
                if table_name == 'phishtank':
                    search_query = """
                    SELECT 
                        url, 
                        phish_id as id,
                        target,
                        verified,
                        created_at,
                        'phishtank' as source,
                        'phishing_url' as result_type
                    FROM phishtank 
                    WHERE url ILIKE $1 OR target ILIKE $2
                    ORDER BY created_at DESC 
                    LIMIT $3 OFFSET $4
                    """
                    results = await db.fetch_all(search_query, search_pattern, search_pattern, limit, offset)
                    
                elif table_name == 'phishstats':
                    search_query = """
                    SELECT 
                        url,
                        phishstats_id as id,
                        title,
                        country_name,
                        score,
                        host,
                        domain,
                        created_at,
                        'phishstats' as source,
                        'phishing_url' as result_type
                    FROM phishstats 
                    WHERE url ILIKE $1 OR title ILIKE $2 OR host ILIKE $3 OR domain ILIKE $4
                    ORDER BY created_at DESC 
                    LIMIT $5 OFFSET $6
                    """
                    results = await db.fetch_all(search_query, search_pattern, search_pattern, domain_pattern, domain_pattern, limit, offset)
                    
                elif table_name == 'certificates':
                    search_query = """
                    SELECT 
                        subject_cn as title,
                        domains,
                        id,
                        created_at,
                        updated_at,
                        'certificates' as source,
                        'ssl_certificate' as result_type
                    FROM certificates 
                    WHERE subject_cn ILIKE $1 OR domains ILIKE $2
                    ORDER BY created_at DESC 
                    LIMIT $3 OFFSET $4
                    """
                    results = await db.fetch_all(search_query, search_pattern, search_pattern, limit, offset)
                    
                elif table_name.startswith('ut1_'):
                    # UT1 tables - simple URL search
                    search_query = f"""
                    SELECT 
                        url,
                        id,
                        created_at,
                        '{source_name}' as source,
                        'blacklist_url' as result_type
                    FROM {table_name} 
                    WHERE url ILIKE $1 
                    ORDER BY created_at DESC 
                    LIMIT $2 OFFSET $3
                    """
                    results = await db.fetch_all(search_query, search_pattern, limit, offset)
                    
                else:
                    # Standard phishing tables
                    search_query = f"""
                    SELECT 
                        url,
                        id,
                        created_at,
                        '{source_name}' as source,
                        'phishing_url' as result_type
                    FROM {table_name} 
                    WHERE url ILIKE $1 
                    ORDER BY created_at DESC 
                    LIMIT $2 OFFSET $3
                    """
                    results = await db.fetch_all(search_query, search_pattern, limit, offset)
                
                # Add results to main list
                for result in results:
                    search_results.append(dict(result))
                    
            except Exception as e:
                logger.warning(f"Error searching in table {table_name}: {e}")
                continue
        
        # Sort all results by created_at descending and apply global limit
        # Handle datetime sorting with timezone issues
        def safe_sort_key(x):
            created_at = x.get('created_at')
            if created_at is None:
                return ''
            # Convert to string for safe comparison if it's a datetime
            if hasattr(created_at, 'isoformat'):
                return created_at.isoformat()
            return str(created_at)
        
        search_results.sort(key=safe_sort_key, reverse=True)
        
        # Apply global pagination
        paginated_results = search_results[offset:offset + limit]
        
        # Group results by type for better presentation
        results_by_type = {}
        for result in paginated_results:
            result_type = result.get('result_type', 'unknown')
            if result_type not in results_by_type:
                results_by_type[result_type] = []
            results_by_type[result_type].append(result)
        
        return {
            "query": q,
            "search_type": "universal_wildcard",
            "sources_searched": list(tables_to_search.keys()),
            "total_found": len(search_results),
            "returned": len(paginated_results),
            "limit": limit,
            "offset": offset,
            "results_by_type": results_by_type,
            "all_results": paginated_results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing universal search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during search")

@router.get("/sources")
async def get_available_sources():
    try:
        ut1_categories = [
            'adult', 'agressif', 'arjel', 'associations_religieuses', 'astrology', 'audio_video', 
            'bank', 'bitcoin', 'blog', 'celebrity', 'chat', 'child', 'cleaning', 'cooking', 
            'cryptojacking', 'dangerous_material', 'dating', 'ddos', 'dialer', 'doh', 'download', 
            'drogue', 'dynamic_dns', 'educational_games', 'examen_pix', 'fakenews', 'filehosting', 
            'financial', 'forums', 'gambling', 'games', 'hacking', 'jobsearch', 'lingerie', 
            'liste_bu', 'malware', 'manga', 'marketingware', 'mixed_adult', 'mobile_phone', 
            'phishing', 'press', 'publicite', 'radio', 'reaffected', 'redirector', 'remote_control', 
            'residential_proxies', 'sect', 'sexual_education', 'shopping', 'shortener', 
            'social_networks', 'sports', 'stalkerware', 'strict_redirector', 'strong_redirector', 
            'translation', 'tricheur', 'tricheur_pix', 'update', 'vpn', 'warez', 'webhosting', 'webmail'
        ]
        
        return {
            "main_sources": [
                "phishtank",
                "openphish", 
                "phishingarmy",
                "blackmirror",
                "phishunt",
                "phishstats",
                "certificates"
            ],
            "ut1_categories": ut1_categories,
            "search_capabilities": {
                "wildcard_search": "Use single endpoint /search/?q=<query>",
                "url_search": "Search for URLs: ?q=example.com or ?q=https://malicious.site",
                "keyword_search": "Search for keywords: ?q=paypal or ?q=banking",
                "certificate_search": "Search certificates: ?q=*.example.com or ?q=certificate_name",
                "domain_search": "Automatic domain detection and pattern matching"
            },
            "usage_examples": {
                "url": "/search/?q=https://suspicious-site.com",
                "domain": "/search/?q=paypal.com",
                "keyword": "/search/?q=banking&sources=phishtank,phishstats",
                "certificate": "/search/?q=*.google.com&sources=certificates",
                "all_ut1": "/search/?q=malware&sources=ut1",
                "specific_ut1": "/search/?q=gambling&sources=ut1_gambling"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting sources: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

