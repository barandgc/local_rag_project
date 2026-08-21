from typing import List

from foundry_local_sdk import Configuration, FoundryLocalManager

EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b"

_embedding_client = None


def get_manager() -> FoundryLocalManager:
    if FoundryLocalManager.instance is None:
        config = Configuration(app_name="rag_project")
        FoundryLocalManager.initialize(config)
    return FoundryLocalManager.instance


def get_embedding_client():
    global _embedding_client
    if _embedding_client is None:
        manager = get_manager()
        model = manager.catalog.get_model(EMBEDDING_MODEL_ALIAS)
        model.download(
            lambda p: print(f"\rIndiriliyor ({EMBEDDING_MODEL_ALIAS}): {p:.2f}%", end="")
        )
        print()
        model.load()
        _embedding_client = model.get_embedding_client()
    return _embedding_client


def embed(text: str) -> List[float]:
    response = get_embedding_client().generate_embedding(text)
    return response.data[0].embedding
