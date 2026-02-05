CREATE INDEX IF NOT EXISTS kb_chunks_embedding_idx
ON kb_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

ANALYZE kb_chunks;
