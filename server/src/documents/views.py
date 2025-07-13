from typing import Annotated

from src.routers import create_api_router
from src.config import DEFAULT_CHUNK_SIZE

from . models import (
    DocumentCreate
)


# utils에만 의존하므로 안전합니다.
router = create_api_router(__file__)


@router.post("/chunks")
async def process_document_endpoint(
    req: DocumentCreate
):
    # 1. 처리할 문서 정의
    sample_document = """
        RAG(Retrieval-Augmented Generation, 검색 증강 생성)은 대규모 언어 모델(LLM)의 한계를 보완하기 위한 강력한 기술입니다.
        LLM은 훈련 데이터에 없는 최신 정보나 특정 도메인의 전문 지식에 대해 잘 알지 못하며, 때로는 환각(hallucination) 현상을 일으켜 잘못된 정보를 생성하기도 합니다.
        RAG는 이러한 문제를 해결하기 위해, 사용자의 질문에 답변하기 전에 먼저 외부 데이터베이스(Vector DB 등)에서 관련성 높은 정보를 검색합니다.
        그리고 검색된 정보를 LLM에게 컨텍스트(context)로 함께 제공하여, LLM이 더 정확하고 신뢰성 있는 답변을 생성하도록 유도합니다.
        이 과정은 크게 '인덱싱(Indexing)'과 '검색 및 생성(Retrieval & Generation)'의 두 단계로 나뉩니다.
        인덱싱 단계에서는 원본 문서를 잘게 쪼개고(Chunking), 각 조각을 벡터로 변환(Embedding)하여 데이터베이스에 저장합니다.
    """
    # 4. JSON으로 반환할 데이터 구성
    processed_data = [
        {
            "chunk_id": i + 1,
            "text": chunk.strip(),
            "vector_sample": vector[:5] # 벡터 샘플
        }
        for i, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]

    return {
        "status": "success",
        "original_text_length": len(sample_document),
        "total_chunks": len(chunks),
        "processed_data": processed_data,
    }
    
async def process_document(document_content: str):
    # TODO: 실제 문서 처리 로직 구현
    return [document_content], [[0.1, 0.2, 0.3, 0.4, 0.5]]


