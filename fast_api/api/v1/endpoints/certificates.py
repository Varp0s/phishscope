from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import logging
from core.database import get_database
from schema.certificate import CertificateResponse, CertificateListResponse
from core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=CertificateListResponse)
async def get_certificates(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in subject_cn or domains"),
    has_domains: Optional[bool] = Query(None, description="Filter by certificates with domains"),
    db=Depends(get_database)
):
    try:
        offset = (page - 1) * limit
        
        # Simple queries without complex parameter binding
        if search and has_domains is not None:
            if has_domains:
                count_query = """
                    SELECT COUNT(*) as total FROM certificates 
                    WHERE (subject_cn ILIKE '%' || $1 || '%' OR domains ILIKE '%' || $1 || '%')
                    AND domains IS NOT NULL AND domains != ''
                """
                certificates_query = """
                    SELECT id, subject_cn, domains, created_at, updated_at
                    FROM certificates 
                    WHERE (subject_cn ILIKE '%' || $1 || '%' OR domains ILIKE '%' || $1 || '%')
                    AND domains IS NOT NULL AND domains != ''
                    ORDER BY updated_at DESC, created_at DESC                    LIMIT $2 OFFSET $3
                """
                total_result = await db.fetch_one(count_query, search)
                certificates = await db.fetch_all(certificates_query, search, limit, offset)
            else:
                count_query = """
                    SELECT COUNT(*) as total FROM certificates 
                    WHERE (subject_cn ILIKE '%' || $1 || '%' OR domains ILIKE '%' || $1 || '%')
                    AND (domains IS NULL OR domains = '')
                """
                certificates_query = """
                    SELECT id, subject_cn, domains, created_at, updated_at
                    FROM certificates 
                    WHERE (subject_cn ILIKE '%' || $1 || '%' OR domains ILIKE '%' || $1 || '%')
                    AND (domains IS NULL OR domains = '')
                    ORDER BY updated_at DESC, created_at DESC 
                    LIMIT $2 OFFSET $3                """
                total_result = await db.fetch_one(count_query, search)
                certificates = await db.fetch_all(certificates_query, search, limit, offset)
        elif search:
            count_query = """
                SELECT COUNT(*) as total FROM certificates 
                WHERE subject_cn ILIKE '%' || $1 || '%' OR domains ILIKE '%' || $1 || '%'
            """
            certificates_query = """
                SELECT id, subject_cn, domains, created_at, updated_at
                FROM certificates 
                WHERE subject_cn ILIKE '%' || $1 || '%' OR domains ILIKE '%' || $1 || '%'
                ORDER BY updated_at DESC, created_at DESC 
                LIMIT $2 OFFSET $3            """
            total_result = await db.fetch_one(count_query, search)
            certificates = await db.fetch_all(certificates_query, search, limit, offset)
        elif has_domains is not None:
            if has_domains:
                count_query = "SELECT COUNT(*) as total FROM certificates WHERE domains IS NOT NULL AND domains != ''"
                certificates_query = """
                    SELECT id, subject_cn, domains, created_at, updated_at
                    FROM certificates 
                    WHERE domains IS NOT NULL AND domains != ''
                    ORDER BY updated_at DESC, created_at DESC 
                    LIMIT $1 OFFSET $2
                """
                total_result = await db.fetch_one(count_query)
                certificates = await db.fetch_all(certificates_query, limit, offset)
            else:
                count_query = "SELECT COUNT(*) as total FROM certificates WHERE domains IS NULL OR domains = ''"
                certificates_query = """
                    SELECT id, subject_cn, domains, created_at, updated_at
                    FROM certificates 
                    WHERE domains IS NULL OR domains = ''
                    ORDER BY updated_at DESC, created_at DESC 
                    LIMIT $1 OFFSET $2
                """
                total_result = await db.fetch_one(count_query)
                certificates = await db.fetch_all(certificates_query, limit, offset)
        else:
            count_query = "SELECT COUNT(*) as total FROM certificates"
            certificates_query = """
                SELECT id, subject_cn, domains, created_at, updated_at
                FROM certificates 
                ORDER BY updated_at DESC, created_at DESC 
                LIMIT $1 OFFSET $2
            """
            total_result = await db.fetch_one(count_query)
            certificates = await db.fetch_all(certificates_query, limit, offset)
        
        total = total_result["total"] if total_result else 0
        
        # Calculate pagination info
        total_pages = (total + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1
        
        return CertificateListResponse(
            certificates=[CertificateResponse(**dict(cert)) for cert in certificates],
            pagination={
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching certificates: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{certificate_id}", response_model=CertificateResponse)
async def get_certificate(
    certificate_id: int,
    db=Depends(get_database)
):
    try:
        query = """
            SELECT id, subject_cn, domains, created_at, updated_at
            FROM certificates 
            WHERE id = $1
        """
        
        certificate = await db.fetch_one(query, certificate_id)
        
        if not certificate:
            raise HTTPException(status_code=404, detail="Certificate not found")
        
        return CertificateResponse(**dict(certificate))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching certificate {certificate_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/domains")
async def search_domains(
    query: str = Query(..., min_length=2, description="Search query for domains"),
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    db=Depends(get_database)
):
    try:
        search_query = """
            SELECT DISTINCT subject_cn, domains
            FROM certificates 
            WHERE domains ILIKE '%' || $1 || '%'
            AND domains IS NOT NULL 
            AND domains != ''
            ORDER BY subject_cn
            LIMIT $2
        """
        
        results = await db.fetch_all(search_query, query, limit)
        
        return {
            "query": query,
            "results": [dict(result) for result in results],
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching domains: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
