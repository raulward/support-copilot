from abc import ABC, abstractmethod
from typing import List

from app.rag.types import ChunkHit


class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 3) -> List[ChunkHit]:
        raise NotImplementedError
