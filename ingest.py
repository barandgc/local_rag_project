import glob
import os
from typing import List

from db import clear_documents, init_db, insert_document
from embeddings import embed

DOCUMENTS_DIR = "documents"


def chunk_text(text: str) -> List[str]:
    paragraphs = [p.strip() for p in text.split("\n\n")]
    return [p for p in paragraphs if p]


def main() -> None:
    init_db()
    clear_documents()

    total_chunks = 0
    for path in sorted(glob.glob(os.path.join(DOCUMENTS_DIR, "*.txt"))):
        source = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        for chunk in chunks:
            embedding = embed(chunk)
            insert_document(source, chunk, embedding)
            total_chunks += 1

        print(f"Islendi: {source} ({len(chunks)} chunk)")

    print(f"\nToplam {total_chunks} chunk veritabanina eklendi.")


if __name__ == "__main__":
    main()
