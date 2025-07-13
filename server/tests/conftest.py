
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient

from src.main import app
from src.database.base import Base

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# 테스트용 인메모리 SQLite 데이터베이스 URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def test_session():
    """
    테스트를 위한 비동기 데이터베이스 세션을 생성하고,
    테스트가 끝나면 모든 변경사항을 롤백합니다.
    """
    # 테스트용 비동기 엔진 및 세션 메이커 생성
    engine = create_async_engine(TEST_DATABASE_URL)
    TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 데이터베이스 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 테스트 세션 시작
    async with TestSessionLocal() as session:
        yield session

    # 테스트 후 테이블 정리
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
