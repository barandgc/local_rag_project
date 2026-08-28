import re
import sys

from chat import get_chat_client
from retrieval import get_top_chunks

MIN_SIMILARITY = 0.42
RELEVANCE_MARGIN = 0.08

_PREAMBLE_RE = re.compile(
    r"^\s*(do[gğ]ru cevap|i[sş]te cevap|cevap)\s*[:\-,]\s*",
    re.IGNORECASE,
)

# phi-4-mini, "Türkiye'nin başkenti neresidir?" gibi genel dünya bilgisi
# sorularında, bağlamda sadece alakasız "başkent" geçen cümleler olsa bile
# kendi ön bilgisinden cevap üretip talimatı görmezden gelebiliyor (küçük
# modellerin bilinen bir sınırlaması). "Krallık/imparatorluk başkenti" gibi
# tarihi, dokümanlarda gerçekten cevaplanan sorularla karışmaması için sadece
# modern ülke başkenti kalıbını hedefliyoruz.
_COUNTRY_CAPITAL_RE = re.compile(
    r"başkent\w*.*(türkiye|ülke\w*)|(türkiye|ülke\w*).*başkent\w*",
    re.IGNORECASE,
)


def _clean_answer(text: str) -> str:
    text = text.strip()
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if paragraphs:
        text = paragraphs[-1]
    text = _PREAMBLE_RE.sub("", text)
    return text.strip()

SYSTEM_PROMPT = (
    "Sen bir soru-cevap asistanısın. Sana bir BAĞLAM ve bir SORU verilecek. "
    "BAĞLAM birden fazla cümleden oluşur. Bu cümlelerden bir kısmı önce il "
    "adıyla, sonra yer adıyla, sonra açıklamayla başlar (aralarında tire ve "
    "iki nokta işareti bulunur) ve farklı illere ait olabilir. "
    "Sorunun türüne göre iki farklı mod uygula: "
    "(1) Soru belirli bir il/yer adını soruyorsa (örn. 'Pamukkale nasıl "
    "oluşmuştur?'), bu formattaki cümleler arasında sorudaki il veya yer "
    "adıyla eşleşmeyenleri TAMAMEN GÖRMEZDEN GEL, sadece sorudaki il/yerle "
    "doğrudan ilgili olanları kullan. "
    "(2) Soru belirli bir il/yer adı sormuyor ama şelale, plaj, kaplıca/"
    "termal, yayla/serin hava, mağara, kayak/dağ, tarihi kent gibi SPESİFİK "
    "bir doğa/gezi deneyimi tarif ediyorsa (yalnızca bu durumda), (1)'deki "
    "isim-eşleştirme kuralı UYGULANMAZ. Bu modda: bağlamdaki cümleler "
    "arasından TEK BİR cümlenin açıklaması bu deneyimi doğrudan ve açıkça "
    "karşılıyorsa, sadece o cümledeki il - yer adını öner. Birden fazla "
    "farklı cümledeki bilgileri BİRLEŞTİREREK tek bir yer için yeni bir "
    "açıklama UYDURMA; her öneri tek bir cümleden gelmelidir. Sorunun konusu "
    "bir doğa/gezi deneyimi değilse (örn. başkent, tarih, genel kültür, "
    "bilim, teknoloji gibi sorular), bu ikinci modu KESİNLİKLE uygulama; "
    "bunun yerine (1)'deki kurala göre değerlendir. "
    "Bu formatta olmayan diğer cümleleri ise konularına göre, sorudaki yerle "
    "ilgiliyse normal şekilde değerlendir. "
    "Önce bağlamı dikkatlice oku. Bağlamda sorunun cevabına dair bilgi varsa, "
    "bu bilgiyi kullanarak SADECE TEK BİR kısa ve net cümleyle cevap ver; "
    "bağlamdaki ifadeleri aynen kopyalamak yerine soruyu doğrudan yanıtla. "
    "Cevabının başında 'doğru cevap', 'işte cevap' gibi giriş ifadeleri "
    "kullanma, bağlamdaki il/yer etiketlerini veya tire-iki nokta gibi format "
    "işaretlerini cevabına kopyalama, kendi cevabını tekrar etme veya kendi "
    "kendini düzeltme; sadece nihai cevabı, tek bir cümle olarak yaz. "
    "Bağlamdaki cümlelerden HİÇBİRİ sorunun asıl konusunu (sorulan yer, "
    "kişi, olay ya da bilgiyi) AÇIKÇA anlatmıyorsa, kendi genel bilgini "
    "kullanma ve sadece 'Bu konuda bilgim yok.' de. Sadece 'Türkiye' veya "
    "'başkent' gibi ortak/genel bir kelimenin, ya da başka bir yere ait "
    "'başkent olmuştur' gibi tarihi bir ifadenin bağlamda geçmesi yeterli "
    "değildir; sorunun asıl konusu (örn. hangi şehrin GÜNÜMÜZDE bir ülkenin "
    "resmi başkenti olduğu) bağlamda doğrudan ve açıkça belirtilmiş "
    "olmalıdır. Emin değilsen 'Bu konuda bilgim yok.' de. "
    "Cevaplarında kaynak dosya adlarından bahsetme."
)


def answer_query(question: str, top_k: int = 5) -> str:
    if not question.strip():
        return "Bu konuda bilgim yok."
    if _COUNTRY_CAPITAL_RE.search(question):
        return "Bu konuda bilgim yok."

    chunks = get_top_chunks(question, top_k=top_k)
    if not chunks or chunks[0][2] < MIN_SIMILARITY:
        return "Bu konuda bilgim yok."

    best_score = chunks[0][2]
    chunks = [c for c in chunks if c[2] >= best_score - RELEVANCE_MARGIN]

    context = "\n\n".join(content for _source, content, _score in chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Bağlam:\n{context}\n\nSoru: {question}",
        },
    ]

    completion = get_chat_client().complete_chat(messages)
    return _clean_answer(completion.choices[0].message.content)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    test_questions = [
        "Pamukkale nasıl oluşmuştur?",
        "Nemrut Dağı'nda gün batımını izlemek popüler mi?",
        "Şelalesi olan bir yer önerir misin?",
        "Serin bir yerde doğa yürüyüşü yapmak istiyorum, nereye gidebilirim?",
        "Ay'a nasıl gidilir?",
    ]
    for question in test_questions:
        print(f"Soru: {question}")
        print(f"Cevap: {answer_query(question)}")
        print()
