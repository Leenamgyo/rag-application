import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text  # ✅ 이거 추가

from src.database.base import AsyncSessionLocal


@pytest.mark.asyncio
async def test_db_connection():
    async with AsyncSessionLocal() as session:
        assert isinstance(session, AsyncSession)

        # ✅ text()로 감싸기
        result = await session.execute(text("SELECT 1 + 1"))
        value = result.scalar()
        assert value == 2