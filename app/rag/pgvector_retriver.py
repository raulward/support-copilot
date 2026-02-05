from typing import List

import numpy as np
from openai import OpenAI
from sqlalchemy import text

from app.core.schemas import Chunk
from app.db.connection import get_engine
from app.rag.base import BaseRetriever
from app.rag.types import ChunkHit

EMBED_MODEL = "text-embedding-3-small"


class PgVectorRetriever(BaseRetriever):
    def __init__(self, client: OpenAI):
        self.client = client
        self.engine = get_engine()

    def _embed_query(self, query: str) -> List[float]:
        resp = self.client.embeddings.create(model=EMBED_MODEL, input=[query])
        return resp.data[0].embedding

    def retrieve(self, query: str, top_k: int = 3) -> List[ChunkHit]:
        qemb = self._embed_query(query)

        qemb_str = str(qemb)

        sql = text(
            """
            SELECT doc_id, chunk_id, content,
                   (1 - (embedding <=> :qemb)) AS score
            FROM kb_chunks
            ORDER BY embedding <=> :qemb
            LIMIT :top_k
            """
        )

        hits: List[ChunkHit] = []
        with self.engine.connect() as conn:
            rows = conn.execute(sql, {"qemb": qemb_str, "top_k": top_k}).mappings().all()

        for r in rows:
            chunk = Chunk(
                doc_id=r["doc_id"],
                chunk_id=r["chunk_id"],
                text=r["content"],
            )
            hits.append(ChunkHit(chunk=chunk, score=float(r["score"])))

        return hits
