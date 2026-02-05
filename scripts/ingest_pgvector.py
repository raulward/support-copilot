import json
import os
import uuid
from pathlib import Path
from typing import List

import numpy as np
from openai import OpenAI
from sqlalchemy import text

from app.db.connection import get_engine
from dotenv import load_dotenv

CHUNKS_PATH = Path("data/kb_chunks.json")
EMBED_MODEL = "text-embedding-3-small"


from openai import OpenAI

# Refatorar depois
load_dotenv()

_client: OpenAI | None = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não configurada.")
        _client = OpenAI(api_key=api_key)
    return _client


def load_rows() -> List[dict]:
    if not CHUNKS_PATH.exists():
        raise RuntimeError("data/kb_chunks.json não encontrado. Rode scripts/ingest_kb.py primeiro.")
    return json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))


def embed_texts(client: OpenAI, texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    engine = get_engine()
    client = get_client()

    rows = load_rows()
    texts = [r["text"] for r in rows]

    embeddings = embed_texts(client, texts)

    upsert_sql = text(
        """
        INSERT INTO kb_chunks (id, doc_id, chunk_id, content, embedding)
        VALUES (:id, :doc_id, :chunk_id, :content, :embedding)
        ON CONFLICT (chunk_id) DO UPDATE SET
          doc_id = EXCLUDED.doc_id,
          content = EXCLUDED.content,
          embedding = EXCLUDED.embedding
        """
    )

    with engine.begin() as conn:
        for r, emb in zip(rows, embeddings):
            conn.execute(
                upsert_sql,
                {
                    "id": str(uuid.uuid4()),
                    "doc_id": r["doc_id"],
                    "chunk_id": r["chunk_id"],
                    "content": r["text"],
                    "embedding": str(emb),
                },
            )

    print(f"OK: inseridos/atualizados {len(rows)} chunks em kb_chunks.")


if __name__ == "__main__":
    main()
