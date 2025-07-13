from datetime import datetime
from elasticsearch_dsl import (
    Document, Text, Keyword, Date, InnerDoc, Nested, Integer, DenseVector
)
from elasticsearch_dsl.connections import get_connection

class Chunk(InnerDoc):
    """
    문서 내의 텍스트 조각(Chunk)을 나타내는 내부 문서(Inner Document)입니다.
    각 Chunk는 고유한 임베딩 벡터를 가집니다.
    """
    content = Text(
        analyzer='nori',
        fields={'raw': Keyword()} # 정렬 및 집계를 위해 원본 텍스트를 Keyword로도 저장
    )
    page_number = Integer()
    # RAG의 핵심인 벡터 검색을 위한 필드. 벡터 차원 수를 지정해야 합니다.
    # 예: 768 (bert-base-multilingual-cased)
    embedding_vector = DenseVector(dims=768, required=True)

class EsDocument(Document):
    # --- 메타데이터 필드 ---
    file_name = Keyword(required=True)
    file_type = Keyword()
    content_hash = Keyword(required=True)
    author = Keyword()
    tags = Keyword(multi=True) # 리스트 형태의 키워드 저장
    
    # --- 시간 정보 필드 ---
    created_at = Date()
    indexed_at = Date(required=True)
    
    # --- 핵심 데이터 필드 ---
    # Nested 필드를 사용하여 Chunk 객체 리스트를 독립적으로 쿼리할 수 있도록 합니다.
    chunks = Nested(Chunk)

    class Index:
        name = 'rag-documents'
