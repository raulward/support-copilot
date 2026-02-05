import time
import hashlib
from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np


@dataclass
class CacheItem:
    value: np.array
    expires_at: float


class QueryEmbeddingCache:
    def __init__(self, ttl_seconds: int = 600):
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, CacheItem] = {}
        self.hits = 0
        self.misses = 0

    def _key(self, text: str) -> str:
        normalized = " ".join(text.strip().lower().split())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def get(self, text: str) -> Optional[np.ndarray]:
        k = self._key(text)
        item = self._store.get(k)
        if not item:
            self.misses += 1
            return None
        if time.time() > item.expires_at:
            self._store.pop(k, None)
            self.misses += 1
            return None
        self.hits += 1
        return item.value

    def set(self, text: str, value: np.ndarray) -> None:
        k = self._key(text)
        self._store[k] = CacheItem(value=value, expires_at=time.time() + self.ttl_seconds)
