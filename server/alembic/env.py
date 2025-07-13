import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- 프로젝트별 설정 (수정된 부분) ---

# 1. 프로젝트 루트 경로를 Python 경로에 추가합니다.
# 이렇게 하면 'src' 디렉토리에서 임포트할 수 있습니다.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# 2. SQLModel과 모든 모델이 정의된 파일을 직접 임포트합니다.
# 복잡한 자동 임포트 로직 대신, 이 한 줄로 모든 모델의 메타데이터를 로드할 수 있습니다.
# 이것이 Alembic이 테이블을 인식하게 하는 가장 확실한 방법입니다.
from sqlmodel import SQLModel
from src.database.models import * # User, File 등 모든 모델을 로드

# 3. Alembic이 사용할 메타데이터를 SQLModel의 것으로 지정합니다.
target_metadata = SQLModel.metadata

# --- 아래는 Alembic 기본 코드 (변경 없음) ---

# Alembic Config 객체
config = context.config

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Offline migration mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online migration mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# 모드에 따라 실행
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
