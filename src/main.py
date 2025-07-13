import os
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.common.config import UPLOAD_DIR
from src.common import routers, middlewares


# 로깅 설정 (선택 사항이지만 권장)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 애플리케이션의 시작(startup) 및 종료(shutdown) 이벤트를 처리합니다.
    """
    logger.info("애플리케이션 시작 중...")
    if not os.path.exists(UPLOAD_DIR):
        try:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            logger.info(f"디렉토리 '{UPLOAD_DIR}'가 성공적으로 생성되었습니다.")
        except OSError as e:
            logger.error(f"디렉토리 '{UPLOAD_DIR}' 생성 중 오류 발생: {e}")
    else:
        logger.info(f"디렉토리 '{UPLOAD_DIR}'가 이미 존재합니다.")

    yield 

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

# Router 설정
app.include_router(routers.setup_v1_router(), prefix="/api/v1")

# 각 예외 처리기를 main.py에서 직접 등록합니다.
app.add_exception_handler(RequestValidationError, middlewares.validation_exception_handler)
app.add_exception_handler(HTTPException, middlewares.http_exception_handler)
app.add_exception_handler(Exception, middlewares.generic_exception_handler)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)