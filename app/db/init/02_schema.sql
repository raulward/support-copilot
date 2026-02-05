CREATE TABLE IF NOT EXISTS kb_chunks (
  id UUID PRIMARY KEY,
  doc_id TEXT NOT NULL,
  chunk_id TEXT NOT NULL UNIQUE,
  content TEXT NOT NULL,
  embedding VECTOR(1536)
);
