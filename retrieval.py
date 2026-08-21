from typing import List, Tuple

from db import get_all_documents
from embeddings import embed
from similarity import cosine_similarity


def get_top_chunks(query: str, top_k: int = 3) -> List[Tuple[str, str, float]]:
    query_embedding = embed(query)
    documents = get_all_documents()

    scored = [
        (source, content, cosine_similarity(query_embedding, embedding))
        for _id, source, content, embedding in documents
    ]
    scored.sort(key=lambda item: item[2], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    test_queries = [
        "Pamukkale nasil olusmustur?",
        "Nemrut Dagi'nda ne gorebilirim?",
        "Yamac parasutu icin nereye gidilir?",
    ]
    for query in test_queries:
        print(f"Sorgu: {query}")
        for source, content, score in get_top_chunks(query, top_k=2):
            print(f"  [{score:.4f}] ({source}) {content[:80]}...")
        print()
