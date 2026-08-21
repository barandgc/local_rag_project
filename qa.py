from chat import get_chat_client
from retrieval import get_top_chunks

MIN_SIMILARITY = 0.40

SYSTEM_PROMPT = (
    "Sen bir soru-cevap asistanisin. Sana bir BAGLAM ve bir SORU verilecek. "
    "Once baglami dikkatlice oku. Baglamda sorunun cevabina dair bilgi varsa, "
    "bu bilgiyi kullanarak kisa ve net bir cevap ver; baglamdaki ifadeleri "
    "aynen kopyalamak yerine soruyu dogrudan yanitla. "
    "Baglamda sorunun cevabiyla ilgili HICBIR bilgi yoksa, kendi genel "
    "bilgini kullanma ve sadece 'Bu konuda bilgim yok.' de. "
    "Cevaplarinda kaynak dosya adlarindan bahsetme."
)


def answer_query(question: str, top_k: int = 3) -> str:
    if not question.strip():
        return "Bu konuda bilgim yok."

    chunks = get_top_chunks(question, top_k=top_k)
    if not chunks or chunks[0][2] < MIN_SIMILARITY:
        return "Bu konuda bilgim yok."

    context = "\n\n".join(content for _source, content, _score in chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Baglam:\n{context}\n\nSoru: {question}",
        },
    ]

    completion = get_chat_client().complete_chat(messages)
    return completion.choices[0].message.content


if __name__ == "__main__":
    test_questions = [
        "Pamukkale nasil olusmustur?",
        "Nemrut Dagi'nda gun batimini izlemek populer mi?",
        "Ay'a nasil gidilir?",
    ]
    for question in test_questions:
        print(f"Soru: {question}")
        print(f"Cevap: {answer_query(question)}")
        print()
