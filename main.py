from foundry_local_sdk import Configuration, FoundryLocalManager

MODEL_ALIAS = "qwen2.5-0.5b"


def main() -> None:
    config = Configuration(app_name="rag_project")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model(MODEL_ALIAS)
    model.download(lambda p: print(f"\rIndiriliyor: {p:.2f}%", end=""))
    print()
    model.load()

    client = model.get_chat_client()
    print("Model cevabi: ", end="")
    for chunk in client.complete_streaming_chat(
        [{"role": "user", "content": "Merhaba, kendini tanit."}]
    ):
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")
    print()

    model.unload()


if __name__ == "__main__":
    main()
