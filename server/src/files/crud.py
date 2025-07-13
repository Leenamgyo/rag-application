from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.files.models import File
from src.database.providers import inject_async_session

@inject_async_session
async def create(session: AsyncSession, models: File) -> File:
    session.add(models)
    return models

@inject_async_session
async def get_files(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[File]:
    """
    파일 레코드 목록을 조회합니다. (페이지네이션)
    """
    result = await session.execute(select(File).offset(skip).limit(limit))
    return result.scalars().all()

@inject_async_session
async def get_file(session: AsyncSession, file_id: int) -> File | None:
    """
    ID를 기준으로 파일 레코드를 조회합니다.
    """
    result = await session.execute(select(File).filter(File.id == file_id))
    return result.scalar_one_or_none()