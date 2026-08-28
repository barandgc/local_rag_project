import glob
import os
import sys
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
    pattern = os.path.join(DOCUMENTS_DIR, "**", "*.txt")
    for path in sorted(glob.glob(pattern, recursive=True)):
        source = os.path.relpath(path, DOCUMENTS_DIR)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        for chunk in chunks:
            embedding = embed(chunk)
            insert_document(source, chunk, embedding)
            total_chunks += 1

        print(f"İşlendi: {source} ({len(chunks)} chunk)")

    print(f"\nToplam {total_chunks} chunk veritabanına eklendi.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
