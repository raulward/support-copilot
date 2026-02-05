from dataclasses import dataclass
from typing import List

from app.core.schemas import Chunk


@dataclass(frozen=True)
class ChunkHit:
    chunk: Chunk
    score: float  
