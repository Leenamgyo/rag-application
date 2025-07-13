from sqlmodel import SQLModel, Relationship
from pydantic import Field
from typing import Optional, List
from datetime import datetime
import uuid


class DocumentCreate(SQLModel):
    title: str = Field(examples="RAG란??")
    contents: str = Field(
        ..., 
        examples="""RAG(Retrieval-Augmented Generation, 검색 증강 생성)은 대규모 언어 모델(LLM)의 한계를 보완하기 위한 강력한 기술입니다.
        LLM은 훈련 데이터에 없는 최신 정보나 특정 도메인의 전문 지식에 대해 잘 알지 못하며, 때로는 환각(hallucination) 현상을 일으켜 잘못된 정보를 생성하기도 합니다.
        RAG는 이러한 문제를 해결하기 위해, 사용자의 질문에 답변하기 전에 먼저 외부 데이터베이스(Vector DB 등)에서 관련성 높은 정보를 검색합니다.
        그리고 검색된 정보를 LLM에게 컨텍스트(context)로 함께 제공하여, LLM이 더 정확하고 신뢰성 있는 답변을 생성하도록 유도합니다.
        이 과정은 크게 '인덱싱(Indexing)'과 '검색 및 생성(Retrieval & Generation)'의 두 단계로 나뉩니다.
        인덱싱 단계에서는 원본 문서를 잘게 쪼개고(Chunking), 각 조각을 벡터로 변환(Embedding)하여 데이터베이스에 저장합니다."""
    )


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    contents: str 
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # 관계: Document 1 : N DocumentChunk
    chunks: List["DocumentChunk"] = Relationship(back_populates="document")


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    contents: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    document_id: str = Field(foreign_key="documents.id")
    document: Optional[Document] = Relationship(back_populates="chunks")