import json
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

import faiss
import numpy as np
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



CHUNKS_PATH = Path("data/kb_chunks.json")
INDEX_PATH = Path("data/faiss.index")
META_PATH = Path("data/faiss_meta.json")

EMBED_MODEL = "text-embedding-3-small"

def load_chunks() -> List[dict]:
    if not CHUNKS_PATH.exists():
        raise RuntimeError("kb_chunks.json não existe.")
    return json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))

def embed_texts(client: OpenAI, texts: List[str]) -> np.array:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vectors = np.array([d.embedding for d in resp.data], dtype=np.float32)
    return vectors

def main():
    client = get_client()
    rows = load_chunks()

    texts = [r["text"] for r in rows]
    vectors = embed_texts(client, texts)

    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)

    index.add(vectors)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    META_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"OK: FAISS index salvo em {INDEX_PATH}")
    print(f"OK: meta salvo em {META_PATH}")
    print(f"Chunks: {len(rows)} | Dim: {dim}")


if __name__ == "__main__":
    main()
