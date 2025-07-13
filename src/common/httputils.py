from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    """
    API 표준 성공 응답 모델입니다.
    제네릭을 사용하여 'data' 필드의 타입을 유연하게 지정할 수 있습니다.
    """
    message: str = Field("Request was successfully processed.", description="응답 메시지")
    data: Optional[T] = Field(None, description="실제 응답 데이터")


class ErrorResponse(BaseModel):
    """
    API 표준 오류 응답 모델입니다.
    """
    message: str = Field(..., description="오류에 대한 요약 메시지")
    code: Optional[str] = Field(None, description="커스텀 에러 코드 (ex. FILE_NOT_FOUND)")
    detail: Optional[Any] = Field(None, description="오류에 대한 상세 정보 (선택 사항)")
