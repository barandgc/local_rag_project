import sys
import time

from qa import answer_query

# (soru, tip) - tip: "cevaplanabilir" (dokümanlarda karşılığı var) veya
# "cevaplanamaz" (dokümanlarda karşılığı yok, "bilmiyorum" beklenir)
TEST_CASES = [
    ("Kapadokya'daki peri bacaları nasıl oluştu?", "cevaplanabilir"),
    ("Pamukkale'deki Kleopatra Havuzu'nun özelliği nedir?", "cevaplanabilir"),
    ("Efes'te bulunan ünlü kütüphanenin adı nedir?", "cevaplanabilir"),
    ("Nemrut Dağı UNESCO listesine hangi yıl alındı?", "cevaplanabilir"),
    ("Ölüdeniz hangi spor için ünlüdür?", "cevaplanabilir"),
    ("Safranbolu evleri hangi dönemden kalmadır?", "cevaplanabilir"),
    ("Antalya'da Kaleiçi neyle bilinir?", "cevaplanabilir"),
    ("Aydın'daki Milet Antik Kenti neyle bilinir?", "cevaplanabilir"),
    ("Zonguldak'taki Gökgöl Mağarası ne ile bilinir?", "cevaplanabilir"),
    ("Bartın'daki Amasra neyle bilinir?", "cevaplanabilir"),
    ("Şelalesi olan bir yer önerir misin?", "cevaplanabilir_oneri"),
    ("Serin bir yerde doğa yürüyüşü yapmak istiyorum, nereye gidebilirim?", "cevaplanabilir_oneri"),
    ("Deniz kenarında sıcak bir tatil yeri önerir misin?", "cevaplanabilir_oneri"),
    ("Kayak yapabileceğim bir yer var mı?", "cevaplanabilir_oneri"),
    ("Türkiye'nin başkenti neresidir?", "cevaplanamaz"),
    ("En iyi Python kütüphaneleri nelerdir?", "cevaplanamaz"),
    ("Ay'a nasıl gidilir?", "cevaplanamaz"),
    ("", "edge_case_bos_sorgu"),
    ("Bana bir şeyler anlat.", "edge_case_cok_genel"),
]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    results = []
    for question, category in TEST_CASES:
        start = time.perf_counter()
        answer = answer_query(question)
        elapsed = time.perf_counter() - start

        print(f"[{category}] Soru: {question or '(boş)'}")
        print(f"  Cevap ({elapsed:.2f}s): {answer}")
        print()

        results.append((question, category, answer, elapsed))

    avg_time = sum(r[3] for r in results) / len(results)
    print("=" * 60)
    print(f"Toplam soru: {len(results)}")
    print(f"Ortalama yanıt süresi: {avg_time:.2f} saniye")


if __name__ == "__main__":
    main()
