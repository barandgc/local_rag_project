import time

from qa import answer_query

# (soru, tip) - tip: "cevaplanabilir" (dokumanlarda karsiligi var) veya
# "cevaplanamaz" (dokumanlarda karsiligi yok, "bilmiyorum" beklenir)
TEST_CASES = [
    ("Kapadokya'daki peri bacalari nasil olustu?", "cevaplanabilir"),
    ("Pamukkale'deki Kleopatra Havuzu'nun ozelligi nedir?", "cevaplanabilir"),
    ("Efes'te bulunan unlu kutuphanenin adi nedir?", "cevaplanabilir"),
    ("Nemrut Dagi UNESCO listesine hangi yil alindi?", "cevaplanabilir"),
    ("Oludeniz hangi spor icin unludur?", "cevaplanabilir"),
    ("Safranbolu evleri hangi donemden kalmadir?", "cevaplanabilir"),
    ("Turkiye'nin baskenti neresidir?", "cevaplanamaz"),
    ("En iyi Python kutuphaneleri nelerdir?", "cevaplanamaz"),
    ("Ay'a nasil gidilir?", "cevaplanamaz"),
    ("", "edge_case_bos_sorgu"),
    ("Bana bir seyler anlat.", "edge_case_cok_genel"),
]


def main() -> None:
    results = []
    for question, category in TEST_CASES:
        start = time.perf_counter()
        answer = answer_query(question)
        elapsed = time.perf_counter() - start

        print(f"[{category}] Soru: {question or '(bos)'}")
        print(f"  Cevap ({elapsed:.2f}s): {answer}")
        print()

        results.append((question, category, answer, elapsed))

    avg_time = sum(r[3] for r in results) / len(results)
    print("=" * 60)
    print(f"Toplam soru: {len(results)}")
    print(f"Ortalama yanit suresi: {avg_time:.2f} saniye")


if __name__ == "__main__":
    main()
