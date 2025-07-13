import pytest
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import io

from src.files.services import create_file
from src.files.models import File

@pytest.mark.asyncio
async def test_create_file_service(test_session: AsyncSession):
    """
    create_file 서비스 함수가 정상적으로 동작하는지 테스트합니다.
    """
    # 1. 테스트 준비 (Arrange)
    test_filename = "test_image.png"
    test_content = b"This is a test image content."
    
    # 실제 UploadFile 객체처럼 동작하는 mock 객체 생성
    mock_file = UploadFile(
        filename=test_filename,
        file=io.BytesIO(test_content)
    )

    # 2. 함수 실행 (Act)
    # 서비스 함수를 호출하여 파일 레코드를 생성합니다.
    # @inject_async_session 데코레이터가 세션을 관리하므로,
    # 테스트에서는 세션을 직접 주입하여 테스트합니다.
    created_db_file = await create_file(session=test_session, file=mock_file)

    # 3. 결과 검증 (Assert)
    assert created_db_file is not None
    assert created_db_file.origin_filename == test_filename
    assert created_db_file.size == len(test_content)
    assert created_db_file.extension == "png"
    assert created_db_file.id is not None # DB에 저장되었으므로 ID가 있어야 함

    # 데이터베이스에서 직접 조회하여 다시 한번 검증
    result = await test_session.execute(select(File).filter(File.id == created_db_file.id))
    retrieved_file = result.scalar_one_or_none()

    assert retrieved_file is not None
    assert retrieved_file.origin_filename == test_filename
    assert ".png" in retrieved_file.stored_filename # 고유 파일명에 확장자가 포함되었는지 확인
