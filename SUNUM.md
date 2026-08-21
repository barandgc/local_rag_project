# Final Sunum — Yerel RAG Asistani

## 1. Problem Tanimi

Genel amacli LLM'ler, ozel/guncel/dar kapsamli bilgi konusunda ya yanlis cevap verir ya da "bilmiyorum" yerine halusinasyon yapar. Bu proje, **tamamen cevrimdisi calisan** ve **sadece kendisine verilen dokumanlara dayanarak** cevap ureten bir soru-cevap asistani gelistiriyor — internet baglantisi veya bulut API'si gerektirmeden. Ornek senaryo: Turkiye'nin 6 gezi noktasi hakkinda bir "gezi rehberi asistani".

## 2. Mimari

```
Kullanici Sorusu
      |
      v
[embed] --(qwen3-embedding-0.6b)-->  sorgu vektoru
      |
      v
SQLite'taki 18 chunk ile cosine similarity  --> en alakali top-3 chunk
      |
      v
   skor < 0.40 ?  --evet--> "Bu konuda bilgim yok." (LLM cagrilmaz)
      |
     hayir
      v
[baglam + soru] --(phi-4-mini)--> Cevap
```

Tum bilesenler Microsoft Foundry Local uzerinden, cihaz uzerinde (NPU/GPU/CPU) calisir; hicbir veri disariya cikmaz.

## 3. Ana Ozellikler

- **Ingestion pipeline** (`ingest.py`): dokumanlari paragraf bazinda chunk'lara boler, embed eder, SQLite'a yazar.
- **Retrieval** (`retrieval.py`): `get_top_chunks(query, top_k)` — saf Python cosine similarity, ekstra kutuphane gerektirmez.
- **Guvenli generation** (`qa.py`): sistem prompt'u modeli sadece baglama sadik kalmaya zorlar; benzerlik esigi dusuk-alakali sorularda LLM'i devre disi birakir.
- **Sistematik test** (`test_qa.py`): 11 soruluk, cevaplanabilir/cevaplanamaz/edge-case kategorili test seti + otomatik sure olcumu.

## 4. Canli Demo Sorulari

| Soru | Beklenen davranis |
|---|---|
| "Pamukkale'deki Kleopatra Havuzu'nun ozelligi nedir?" | Baglamdan dogru, kisa cevap |
| "Nemrut Dagi UNESCO listesine hangi yil alindi?" | "1987" |
| "Ay'a nasil gidilir?" | "Bu konuda bilgim yok." (kaynaksiz, hizli) |
| (bos sorgu) | "Bu konuda bilgim yok." (LLM'e gitmeden) |

## 5. Ogrenilen Dersler

1. **Retrieval'i once dogrula, sonra generation'i suclama.** Ilk basarisiz testlerde sorunun LLM'de mi yoksa retrieval'da mi oldugunu ayirt etmek kritik oldu — retrieval her zaman dogru chunk'i buluyordu, sorun prompt ve model boyutundaydi.
2. **Model boyutu = kalite.** `qwen2.5-0.5b` (chat icin) Turkce'de tutarsiz/halusinasyonlu cevaplar uretti; `phi-4-mini`'ye (2.2 GB) gecmek tek basina en buyuk kalite sicramasini sagladi.
3. **Benzerlik skoru ucretsiz bir guven sinyalidir.** `MIN_SIMILARITY` esigi eklemek hem yanlis cevaplari azalttı hem de kapsam-disi sorularda LLM cagrisini atlayarak yaniti ~35% hizlandirdi (11.5s -> 7.2s ortalama).
4. **Kucuk modeller mukemmel degil.** Bazi cevaplanabilir sorularda (ör. "Safranbolu evleri hangi donemden kalmadir?") model calistirmadan calistirmaya tutarsiz davranabiliyor — bu, "tamamlanmamislik" degil, kucuk yerel modellerle calismanin dogal ve dokumante edilmesi gereken bir sinirlamasi.

## 6. Sinirlamalar ve Sonraki Adimlar

- Yanit sureleri (7-23s) roadmap hedefinin (1-3s) uzerinde — daha kucuk/hizlandirilmis model veya donanim iyilestirmesiyle azaltilabilir.
- Bilgi tabani sadece 6 dokumanla sinirli; genisletmek icin tek yapilmasi gereken `documents/` klasorune yeni `.txt` dosyasi ekleyip `ingest.py`'yi yeniden calistirmak.
- Arayuz bilincli olarak eklenmedi; proje pipeline dogrulugu uzerine odaklandi.
