from typing import Optional
from sqlmodel import SQLModel, Field
from src.database.models import BaseModel, TimeStampMixin

# --- Concrete Table Models ---
class File(BaseModel, TimeStampMixin, table=True):
    """
    업로드된 파일 정보를 저장하는 테이블 모델입니다.
    """
    __tablename__ = "files"

    origin_filename: str = Field(index=True)
    stored_filename: str = Field(index=True)
    dir_path: str = Field(default="/")
    extension: str
    size: int
    content_type: str

    def __repr__(self):
        return (
            f"<File(id={self.id}, origin_filename='{self.origin_filename}', "
            f"size={self.size})>"
        )

