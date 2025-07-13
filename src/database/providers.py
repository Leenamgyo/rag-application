from typing import AsyncGenerator
from functools import wraps

# 수정: 설정 부분을 base.py에서 가져옵니다.
# 참고: 동기 세션을 사용하려면 src/database/base.py에 Session, SessionLocal이 정의되어 있어야 합니다.
from src.database.base import AsyncSession, AsyncSessionLocal, SessionLocal

# --- FastAPI Depends용 세션 주입 함수 ---

async def provide_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Depends() 전용 비동기 세션 주입기.
    이 함수는 FastAPI가 요청 단위로 트랜잭션을 관리하는 것을 전제로 합니다.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# --- 데코레이터 기반 세션 주입기 (비동기) ---
def inject_async_session(func):
    """
    비동기 함수에 데이터베이스 세션을 주입하고 트랜잭션을 관리하는 데코레이터입니다.
    함수 실행 성공 시 commit, 실패 시 rollback을 수행합니다.
    """
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        # 외부에서 세션이 이미 주입된 경우, 트랜잭션 관리는 외부의 책임으로 간주합니다.
        if 'session' in kwargs and isinstance(kwargs['session'], AsyncSession):
            return await func(*args, **kwargs)

        async with AsyncSessionLocal() as session:
            try:
                kwargs['session'] = session
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                # 발생한 예외를 다시 던져서 호출자가 오류를 인지할 수 있도록 합니다.
                raise e
    return async_wrapper

# --- 데코레이터 기반 세션 주입기 (동기) ---

def inject_sync_session(func):
    """
    동기 함수에 데이터베이스 세션을 주입하고 트랜잭션을 관리하는 데코레이터입니다.
    함수 실행 성공 시 commit, 실패 시 rollback을 수행합니다.
    """
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        # 외부에서 세션이 이미 주입된 경우, 트랜잭션 관리는 외부의 책임으로 간주합니다.
        if 'session' in kwargs and isinstance(kwargs['session'], Session):
            return func(*args, **kwargs)

        with SessionLocal() as session:
            try:
                kwargs['session'] = session
                result = func(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                # 발생한 예외를 다시 던져서 호출자가 오류를 인지할 수 있도록 합니다.
                raise e
    return sync_wrapper
