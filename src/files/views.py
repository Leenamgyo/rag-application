import os 

from fastapi import (
    UploadFile, File,
    status
)

from src.common.httputils import StandardResponse
from src.common.routers import create_api_router

from . import services as svc

# utils에만 의존하므로 안전합니다.
router = create_api_router(__file__)

@router.post(
    "/upload", 
    status_code=status.HTTP_201_CREATED,
    response_model=StandardResponse,
)
async def upload_and_save_metadata(
    file: UploadFile = File(...)
):
    """파일을 업로드하고, 그 메타데이터를 데이터베이스에 저장합니다."""
    
    response = await svc.create(file=file)
    
    return StandardResponse(data=response)
    
