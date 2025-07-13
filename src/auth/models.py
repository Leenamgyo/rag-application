from sqlmodel import SQLModel, Field
from typing import Optional

from src.database.models import BaseModel, TimeStampMixin

class User(BaseModel, table=True):
    """
    사용자 정보를 저장하는 테이블 모델입니다.
    """
    __tablename__ = "users"

    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
