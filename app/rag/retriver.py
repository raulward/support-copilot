import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

from app.core.schemas import Chunk

CHUNK_PATHS = Path("data/kb_chunks.json")

STOPWORDS = {
    "a", "o", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "para", "por", "com", "sem", "sobre", "entre",
    "e", "ou", "mas", "que", "se", "ao", "à", "às",
    "eu", "você", "vocês", "ele", "ela", "eles", "elas",
    "meu", "minha", "seu", "sua", "seus", "suas",
    "não", "sim", "já", "só", "mais", "muito", "pouco",
    "quando", "como", "onde", "qual", "quais", "porque",
}

def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9áàâãéèêíìîóòôõúùûç\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def _keywords(text: str) -> List[str]:
    norm = _normalize(text)
    words = [w for w in norm.split(" ") if len(w) >= 3 and w not in STOPWORDS]
    return words

def load_chunks(path: Path = CHUNK_PATHS) -> List[Chunk]:
    if not path.exists():
        raise RuntimeError(
            f"Arquivo {path} não encontrado."
        )

    data = json.loads(path.read_text(encoding="utf-8"))
    chunks: List[Chunk] = []
    for row in data:
        chunks.append(
            Chunk(
                doc_id = row["doc_id"],
                chunk_id = row["chunk_id"],
                text = row["text"],
            )
        )
    return chunks

def score_chunks(query_keywords: List[str], chunk_text: str) -> int:
    hay = _normalize(chunk_text)

    score = 0
    for kw in query_keywords:
        if kw in hay:
            score += 1
    return score

def retriver(query: str, chunks: List[Chunk], top_k: int = 3, min_score: int = 1) -> List[Tuple[Chunk, int]]:

    qk = _keywords(query)
    if not qk:
        return []

    scored: List[Tuple[Chunk, int]] = []
    for c in chunks:
        s = score_chunks(qk, c.text)
        if s >= min_score:
            scored.append((c, s))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
