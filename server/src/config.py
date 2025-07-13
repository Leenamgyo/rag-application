import os

UPLOAD_DIR = "./uploads"

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123!#")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "test-db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# LOGGER 
LOG_NAME = "bm25.server"
LOG_FILE = "app.log"
LOG_LEVEL = "INFO"  # or "DEBUG", "WARNING", etc.
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"

# 강력하고 예측 불가능한 시크릿 키를 사용해야 합니다.
# 터미널에서 `openssl rand -hex 32` 명령어로 생성할 수 있습니다.
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DEFAULT_CHUNK_SIZE = 300

class LoggerConfig:
    NAME = "server"
    LOG_FILE = "server.log"
    LEVEL = "INFO"  # or "DEBUG", "WARNING", etc.
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"