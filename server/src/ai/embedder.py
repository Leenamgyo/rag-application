# rag_service/chunking/embedder.py
from typing import List
from transformers import AutoTokenizer, AutoModel
import torch

class HuggingFaceEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]  # [CLS] token
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings.tolist()