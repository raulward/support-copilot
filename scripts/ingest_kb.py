import json
from pathlib import Path
import os

from app.rag.chunking import chunk_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = PROJECT_ROOT / "kb"

OUT_PATH = Path("./data/kb_chunks.json")

def main():
    if not KB_DIR.exists():
        raise RuntimeError("Pasta kb/ não existe.")

    md_files = sorted(KB_DIR.glob("*.md"))
    if not md_files:
        print("cwd:", os.getcwd())
        print("pasta_kb:", KB_DIR.resolve())
        print("mds:", list(KB_DIR.glob("*.md")))
        raise RuntimeError("Nenhum arquivo .md encontrado na pasta.")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    per_doc_counts = {}

    from time import perf_counter

    for file_path in md_files:
        doc_id = file_path.stem
        t_doc = perf_counter()

        text = file_path.read_text(encoding="utf-8")
        print(f"[ingest] {doc_id}: {len(text)} chars")

        t0 = perf_counter()
        print("[ingest] chunking...")
        chunks = chunk_text(doc_id=doc_id, text=text)
        print(f"[ingest] chunks: {len(chunks)}")


        per_doc_counts[doc_id] = len(chunks)

        for c in chunks:
            all_chunks.append({"doc_id": c.doc_id, "chunk_id": c.chunk_id, "text": c.text})

        print(f"[done]   {doc_id}: total {(perf_counter()-t_doc):.2f}s")


    OUT_PATH.write_text(
        json.dumps(all_chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


    total = len(all_chunks)
    print(f"OK: gerados {total} chunks em {OUT_PATH}")
    print("Chunks por documento:")
    for doc_id, count in per_doc_counts.items():
        print(f"- {doc_id}: {count}")



if __name__ == "__main__":
    main()
