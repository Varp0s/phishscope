from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any

class CertificateBase(BaseModel):
    subject_cn: str = Field(..., description="Certificate subject common name")
    domains: Optional[str] = Field(None, description="Associated domains")

class CertificateResponse(CertificateBase):
    id: int = Field(..., description="Certificate ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True

class PaginationInfo(BaseModel):
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")

class CertificateListResponse(BaseModel):
    certificates: List[CertificateResponse] = Field(..., description="List of certificates")
    pagination: PaginationInfo = Field(..., description="Pagination information")

class CertificateCreate(CertificateBase):    
    pass

class CertificateUpdate(BaseModel):
    subject_cn: Optional[str] = Field(None, description="Certificate subject common name")
    domains: Optional[str] = Field(None, description="Associated domains")
