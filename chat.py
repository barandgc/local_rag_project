from embeddings import get_manager

CHAT_MODEL_ALIAS = "phi-4-mini"

_chat_client = None


def get_chat_client():
    global _chat_client
    if _chat_client is None:
        manager = get_manager()
        model = manager.catalog.get_model(CHAT_MODEL_ALIAS)
        model.download(
            lambda p: print(f"\rİndiriliyor ({CHAT_MODEL_ALIAS}): {p:.2f}%", end="")
        )
        print()
        model.load()
        _chat_client = model.get_chat_client()
        _chat_client.settings.temperature = 0.15
        _chat_client.settings.top_p = 0.9
        _chat_client.settings.max_tokens = 200
    return _chat_client
