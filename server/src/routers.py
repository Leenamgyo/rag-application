from fastapi import APIRouter
from pathlib import Path

def create_api_router(path: str = __file__) -> APIRouter:
    auto_prefix = Path(path).parent.name
    return APIRouter(
        prefix=f"/{auto_prefix}",
        tags=[auto_prefix.capitalize()]
    )

def setup_v1_router() -> APIRouter:
    from src.documents.views import router as documents_router
    from src.files.views import router as file_router
    from src.auth.views import router as auth_router

    v1_router = APIRouter()
    v1_router.include_router(documents_router)
    v1_router.include_router(file_router)
    v1_router.include_router(auth_router)
    return v1_router


