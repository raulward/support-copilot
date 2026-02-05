from openai import OpenAI

from app.core.config import settings
from app.rag.base import BaseRetriever
from app.rag.faiss_retriever import FaissRetriever
from app.rag.pgvector_retriver import PgVectorRetriever


def build_retriever(client: OpenAI) -> BaseRetriever:
    backend = settings.retriever_backend

    if backend == "faiss":
        return FaissRetriever(client=client)

    if backend == "pgvector":
        return PgVectorRetriever(client=client)

    if backend == "naive":
        raise NotImplementedError("naive retriever ainda não implementado")

    raise ValueError(f"RETRIEVER_BACKEND inválido: {backend}")
