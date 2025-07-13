import os
import aiofiles

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.providers import inject_async_session
from src.config import UPLOAD_DIR

from . import (
    crud as file_crud,
    utils as file_utils,
    models as file_models
)

@inject_async_session
async def create(
    session: AsyncSession, 
    file: UploadFile
):
    # 파일 내용 읽기
    contents = await file.read()
    
    # 저장 경로 지정 (예: uploads/ 폴더 내)
    save_path = f"{UPLOAD_DIR}/{file.filename}"

    # 비동기 쓰기
    async with aiofiles.open(save_path, 'wb') as out_file:
        await out_file.write(contents)

    # 파일 확장자 추출
    _, extension = os.path.splitext(file.filename)

    # 유틸리티 함수를 사용하여 고유한 저장용 파일명 생성
    stored_filename = file_utils.generate_uuid_stored_filename(file.filename)

    models = file_models.File(
        origin_filename=file.filename,
        stored_filename=stored_filename, # 추가
        size=len(contents),
        content_type=file.content_type,
        extension=extension.lstrip('.')
    )

    db_file = await file_crud.create(session=session, models=models)
    return db_file

