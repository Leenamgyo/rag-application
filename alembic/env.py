import os
import sys, importlib, pkgutil
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- 프로젝트별 설정 (수정된 부분) ---

# 1. 프로젝트 루트 경로를 Python 경로에 추가합니다.
# 이렇게 하면 'src' 디렉토리에서 임포트할 수 있습니다.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import src
def import_all_models(package):
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package.__name__}.{module_name}"
        importlib.import_module(full_module_name)
        if is_pkg:
            import_all_models(importlib.import_module(full_module_name))

import_all_models(src)

from sqlmodel import SQLModel
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
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


# 모드에 따라 실행
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
