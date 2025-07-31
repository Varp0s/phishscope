from fastapi import APIRouter
from .endpoints import certificates, statistics, health, virustotal, search

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    certificates.router,
    prefix="/certificates",
    tags=["certificates"]
)

api_router.include_router(
    statistics.router,
    prefix="/stats",
    tags=["statistics"]
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["search"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)


api_router.include_router(
    virustotal.router,
    prefix="/vt",
    tags=["virustotal"]
)