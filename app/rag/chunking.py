from typing import List
from app.core.schemas import Chunk


def chunk_text(
    doc_id: str,
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[Chunk]:

    if overlap >= chunk_size:
        raise ValueError("overlap deve ser menor que chunk_size")

    cleaned = text.strip()
    n = len(cleaned)            
    chunks: List[Chunk] = []

    start = 0
    idx = 0

    while start < n:
        end = min(start + chunk_size, n)
        piece = cleaned[start:end].strip()

        if piece:
            chunks.append(
                Chunk(
                    doc_id=doc_id,
                    chunk_id=f"{doc_id}::c{idx}",
                    text=piece,
                )
            )
            idx += 1

        if end >= n:
            break

        next_start = end - overlap
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks
