# src/auth/schemas.py
from pydantic import BaseModel, EmailStr

# 토큰 스키마
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# 사용자 기본 스키마
class UserBase(BaseModel):
    username: str
    email: EmailStr

# 사용자 생성 시 받을 데이터 (비밀번호 포함)
class UserCreate(UserBase):
    password: str

# DB에서 읽어올 때 사용할 스키마 (해시된 비밀번호 포함)
class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True # SQLAlchemy 모델과 매핑되도록 설정

# API 응답으로 보낼 사용자 정보 (비밀번호 제외)
class UserPublic(UserBase):
    id: int

    class Config:
        orm_mode = True