import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Pydantic 모델 등에서 발생하는 요청 유효성 검사 오류를 처리합니다.
    """
    logger.error(f"요청 유효성 검사 오류: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "요청 데이터의 형식이 올바르지 않습니다.", "errors": exc.errors()},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    코드 내에서 명시적으로 발생시킨 HTTPException을 처리합니다.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    처리되지 않은 모든 예외를 잡아 500 Internal Server Error로 응답합니다.
    """
    logger.error(f"예상치 못한 오류 발생: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부에서 오류가 발생했습니다."},
    )
