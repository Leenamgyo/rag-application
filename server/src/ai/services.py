# src/ai/services.py
from src.ai.splitter import split_text
from src.ai.embedder import HuggingFaceEmbedder

def process_document(text: str):
    print("[*] 원본 텍스트 길이:", len(text))

    # 1. 청크 분할
    chunks = split_text(text, max_tokens=200, overlap=20)
    print(f"[*] 총 {len(chunks)}개의 청크 생성됨")

    # 2. 임베딩
    embedder = HuggingFaceEmbedder()
    vectors = embedder.embed(chunks)

    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        print(f"\n--- 청크 {i+1} ---")
        print("텍스트:", chunk[:100], "...")
        print("벡터 (앞부분):", vector[:5])

    return chunks, vectors
