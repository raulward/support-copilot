import json
from pathlib import Path
from typing import List

import faiss
import numpy as np
from openai import OpenAI

from app.core.schemas import Chunk
from app.rag.base import BaseRetriever
from app.rag.types import ChunkHit

EMBED_MODEL = "text-embedding-3-small"

INDEX_PATH = Path("data/faiss.index")
META_PATH = Path("data/faiss_meta.json")


class FaissRetriever(BaseRetriever):
    def __init__(self, client: OpenAI):
        if not INDEX_PATH.exists() or not META_PATH.exists():
            raise RuntimeError("FAISS index ou meta não encontrados. Rode o indexer.")

        self.client = client
        self.index = faiss.read_index(str(INDEX_PATH))
        self.meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    def _embed_query(self, query: str) -> np.ndarray:
        resp = self.client.embeddings.create(
            model=EMBED_MODEL,
            input=[query],
        )
        vec = np.array(resp.data[0].embedding, dtype=np.float32).reshape(1, -1)
        faiss.normalize_L2(vec)
        return vec

    def retrieve(self, query: str, top_k: int = 3) -> List[ChunkHit]:
        qvec = self._embed_query(query)
        scores, indices = self.index.search(qvec, top_k)

        hits: List[ChunkHit] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            row = self.meta[idx]
            chunk = Chunk(
                doc_id=row["doc_id"],
                chunk_id=row["chunk_id"],
                text=row["text"],
            )

            hits.append(ChunkHit(chunk=chunk, score=float(score)))

        return hits
