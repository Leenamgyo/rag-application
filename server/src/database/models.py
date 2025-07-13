from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func

# --- Mixin Class for Reusable Columns ---
# 이 클래스는 테이블로 생성되지 않으며, 공통 컬럼 정의를 제공합니다.
class TimeStampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )

# --- Abstract Base Model ---
# 모든 모델이 상속받는 추상 베이스 모델입니다.
# 이제 공통 필드는 TimeStampMixin으로 이동했습니다.
class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

