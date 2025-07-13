# rag_service/chunking/splitter.py
from typing import List

def split_text(text: str, max_tokens: int = 200, overlap: int = 20) -> List[str]:
    """텍스트를 max_tokens 단위로 나누되 overlap을 고려함."""
    import tiktoken  # openai tokenizer도 사용 가능

    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = tokenizer.decode(tokens[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap

    return chunks