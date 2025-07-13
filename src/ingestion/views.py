from typing import Annotated

from common.routers import create_api_router
from common.config import DEFAULT_CHUNK_SIZE

from . models import (
    DocumentCreate
)


# utils에만 의존하므로 안전합니다.
router = create_api_router(__file__)


@router.post("/documents/chunks")
async def documents_chunks(
    req: DocumentCreate
):
    pass