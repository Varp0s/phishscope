from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Optional
import logging
import os
import tempfile
from pydantic import BaseModel
# Import VirusTotal scanner functions
try:
    from plugins.vt_scanner import (
        vt_upload, 
        hash_search, 
        url_search, 
        vt_report, 
        large_file_upload_url,
        upload_large_file, 
        get_large_file_upload_url
    )
except ImportError:
    # Fallback import if running from different directory
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from plugins.vt_scanner import (
        vt_upload, 
        hash_search, 
        url_search, 
        vt_report, 
        large_file_upload_url,
        upload_large_file,
        get_large_file_upload_url
    )

logger = logging.getLogger(__name__)
router = APIRouter()

class HashSearchRequest(BaseModel):
    hash: str
class URLSearchRequest(BaseModel):
    url: str
class AnalysisRequest(BaseModel):
    analysis_id: str

@router.post("/upload")
async def upload_file_to_virustotal(file: UploadFile = File(...)):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Upload file to VirusTotal
            result = vt_upload(temp_file_path)
            
            if result:
                return {
                    "status": "success",
                    "message": "File uploaded successfully",
                    "data": result
                }
            else:
                raise HTTPException(status_code=400, detail="Failed to upload file to VirusTotal")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/upload/large")
async def upload_large_file_to_virustotal(file: UploadFile = File(...)):
    try:
        # Get upload URL for large files
        upload_url_response = get_large_file_upload_url()
        
        if not upload_url_response or 'data' not in upload_url_response:
            raise HTTPException(status_code=400, detail="Failed to get upload URL for large file")
        upload_url = upload_url_response['data']
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Upload large file to VirusTotal
            result = upload_large_file(temp_file_path, upload_url)
            
            if result:
                return {
                    "status": "success",
                    "message": "Large file uploaded successfully",
                    "data": result
                }
            else:
                raise HTTPException(status_code=400, detail="Failed to upload large file to VirusTotal")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    except Exception as e:
        logger.error(f"Large file upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/upload-url")
async def get_upload_url():
    try:
        result = large_file_upload_url()
        if result:
            return {
                "status": "success",
                "message": "Upload URL retrieved successfully",
                "data": result
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to get upload URL from VirusTotal")
    
    except Exception as e:
        logger.error(f"Get upload URL error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/search/hash")
async def search_by_hash(request: HashSearchRequest):
    try:
        if not request.hash:
            raise HTTPException(status_code=400, detail="Hash is required")
        
        result = hash_search(request.hash)
        
        if result:
            return {
                "status": "success",
                "message": "Hash search completed",
                "data": result
            }
        else:
            return {
                "status": "not_found",
                "message": "No analysis found for the provided hash",
                "data": {}
            }
    
    except Exception as e:
        logger.error(f"Hash search error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/search/url")
async def search_by_url(request: URLSearchRequest):
    try:
        if not request.url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        result = url_search(request.url)
        
        if result:
            return {
                "status": "success",
                "message": "URL search completed",
                "data": result
            }
        else:
            return {
                "status": "not_found",
                "message": "No analysis found for the provided URL",
                "data": {}
            }
    
    except Exception as e:
        logger.error(f"URL search error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/analysis/report")
async def get_analysis_report(request: AnalysisRequest):
    try:
        if not request.analysis_id:
            raise HTTPException(status_code=400, detail="Analysis ID is required")
        
        result = vt_report(request.analysis_id)
        
        if result:
            return {
                "status": "success",
                "message": "Analysis report retrieved",
                "data": result
            }
        else:
            return {
                "status": "not_found",
                "message": "No report found for the provided analysis ID",
                "data": {}
            }
    
    except Exception as e:
        logger.error(f"Analysis report error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/search/hash/{hash}")
async def search_by_hash_get(hash: str):
    try:
        if not hash:
            raise HTTPException(status_code=400, detail="Hash is required")
        
        result = hash_search(hash)
        
        if result:
            return {
                "status": "success",
                "message": "Hash search completed",
                "data": result
            }
        else:
            return {
                "status": "not_found",
                "message": "No analysis found for the provided hash",
                "data": {}
            }
    
    except Exception as e:
        logger.error(f"Hash search error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/analysis/report/{analysis_id}")
async def get_analysis_report_get(analysis_id: str):
    try:
        if not analysis_id:
            raise HTTPException(status_code=400, detail="Analysis ID is required")
        
        result = vt_report(analysis_id)
        
        if result:
            return {
                "status": "success",
                "message": "Analysis report retrieved",
                "data": result
            }
        else:
            return {
                "status": "not_found",
                "message": "No report found for the provided analysis ID",
                "data": {}
            }
    
    except Exception as e:
        logger.error(f"Analysis report error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
