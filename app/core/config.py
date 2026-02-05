import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    retriever_backend: str = os.getenv("RETRIEVER_BACKEND", "faiss").lower()
    faiss_top_k: int = int(os.getenv("FAISS_TOP_K", "3"))
    faiss_context_k: int = int(os.getenv("FAISS_CONTEXT_K", "2"))


settings = Settings()
