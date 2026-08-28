# Yerel RAG Asistanı — Türkiye'nin Doğa ve Tarih Harikaları

Microsoft Foundry Local kullanarak tamamen cevrimdisi calisan bir RAG (Retrieval-Augmented Generation) soru-cevap asistani. Bilgi tabani, Turkiye'nin 6 populer gezi noktasi (Kapadokya, Pamukkale, Efes, Nemrut Dagi, Oludeniz, Safranbolu) hakkinda kisa dokumanlardan olusuyor.

## Nasil Calisir

```
Soru --> [embed] --> SQLite'ta cosine similarity ile en alakali chunk'lari bul
                              --> [baglam + soru] --> yerel LLM --> Cevap
```

1. **Ingestion** (`ingest.py`): `documents/` klasorundeki `.txt` dosyalari paragraf bazinda chunk'lara bolunur, her chunk Foundry Local'in embedding modeliyle vektorlestirilir ve SQLite veritabanina (`rag.db`) kaydedilir.
2. **Retrieval** (`retrieval.py`): Kullanici sorusu embed edilir, veritabanindaki tum chunk'larla cosine similarity hesaplanir, en alakali `top_k` chunk secilir.
3. **Generation** (`qa.py`): Secilen chunk'lar baglam olarak sisteme verilir; yerel LLM sadece bu baglama dayanarak cevap uretir, baglamda yoksa "Bu konuda bilgim yok." der. En alakali chunk'in benzerlik skoru `MIN_SIMILARITY` (0.40) esiginin altindaysa, LLM hic cagrilmadan dogrudan "Bu konuda bilgim yok." donulur — bu hem alakasiz baglamin modeli yanlis yonlendirmesini onler hem de yaniti hizlandirir.

## Kullanilan Modeller (Foundry Local)

| Amac       | Model                  | Boyut  |
|------------|-------------------------|--------|
| Embedding  | `qwen3-embedding-0.6b`  | 478 MB |
| Chat       | `phi-4-mini`             | 2.2 GB |

> Not: Ilk denemede chat modeli olarak `qwen2.5-0.5b` kullanıldı ancak cok kucuk oldugu icin (ozellikle Turkce'de) tutarsiz/halusinasyonlu cevaplar uretti. `phi-4-mini`'ye gecince cevap kalitesi buyuk olcude iyilesti — bu, RAG projelerinde chat modeli seciminin embedding modeli kadar onemli oldugunu gosteren iyi bir ders.

## Proje Yapisi

```
rag_project/
  documents/          # Bilgi tabani (6 .txt dosyasi)
  embeddings.py        # Foundry Local embedding client (singleton)
  chat.py               # Foundry Local chat client (singleton)
  db.py                 # SQLite: documents(id, source, content, embedding)
  similarity.py         # Cosine similarity
  ingest.py              # Dokumanlari chunk'la, embed et, SQLite'a yaz
  retrieval.py            # get_top_chunks(query, top_k)
  qa.py                    # answer_query(question) - uctan uca RAG
  test_qa.py                # Cevaplanabilir/cevaplanamaz soru testleri + sure olcumu
  app.py                      # Flask web arayuzu
  templates/index.html         # Sohbet arayuzu (HTML/CSS/JS)
  main.py                    # Hafta 1 "hello model" testi
  requirements.txt
  .gitignore
```

## Calistirma

```powershell
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# Bilgi tabanini SQLite'a yukle (bir kez calistirilir, dokumanlar degistiginde tekrar calistirilir)
venv\Scripts\python ingest.py

# Test sorulariyla dogrula
venv\Scripts\python test_qa.py

# Web arayuzunu baslat (http://127.0.0.1:5000)
venv\Scripts\python app.py

# Tek bir soru sormak icin (Python icinden)
python -c "from qa import answer_query; print(answer_query('Pamukkale nasil olusmustur?'))"
```

## Test Sonuclari (`test_qa.py`)

11 soruluk test setiyle (6 cevaplanabilir, 3 kapsam-disi, 2 edge case) olculdu:

| Asama | Ortalama yanit suresi | Not |
|---|---|---|
| Ilk versiyon (esik yok, ham prompt) | ~11.5s | 3 cevaplanabilir soruda yanlislikla "bilmiyorum" dendi; bir kapsam-disi soruda ("Turkiye'nin baskenti") model halusinasyon yaparak yanlis cevap uretti |
| Iyilestirilmis prompt + `MIN_SIMILARITY` esigi | **~7.2s** | 6/6 cevaplanabilir soru dogru; kapsam-disi ve edge-case sorular esik sayesinde LLM'e gitmeden (<1s) dogru sekilde reddedildi |

**Ogrenilen dersler:**
- Retrieval katmani (embedding + cosine similarity) baslangictan itibaren dogru calisiyordu — sorunlar hep generation (LLM) katmanindaydi. Hata ayiklarken once retrieval'i, sonra prompt'u, sonra modeli kontrol etmek dogru sirayla ilerlemeyi sagladi.
- Kucuk chat modelleri (0.5B) Turkce'de RAG talimatlarini takip etmekte ciddi zorlaniyor; 2B+ modele (`phi-4-mini`) gecmek tek basina buyuk fark yaratti.
- Benzerlik esigi eklemek, hem yanlis/halusinasyonlu cevaplari azaltti hem de kapsam-disi sorularda LLM cagrisini atlayarak performansi iyilestirdi — retrieval skorunu "guven sinyali" olarak kullanmak ucuz ve etkili bir guvenlik onlemi.
- **Bilinen ac sorun**: "Safranbolu evleri hangi donemden kalmadir?" sorusu, dogru chunk'lar (skor 0.62-0.64) bağlamda olmasina ragmen bazi calistirmalarda hala yanlislikla "bilmiyorum" cevabini uretebiliyor — bu, kucuk modelin calistirmalar arasi tutarsizligindan (non-determinism) kaynaklanan, tamamen cozulememis bir sinirlama olarak dokumante edildi.

## Tasarim Kararlari

- **Chunk stratejisi**: Her dokuman paragraf bazinda (bos satirla ayrilmis) chunk'lara bolunuyor — 6 dokuman x 3 paragraf = 18 chunk. Kisa dokumanlar icin bu, cumle bazli bolmeden daha anlamli baglam parcalari verdi.
- **Embedding depolama**: Basitlik ve okunabilirlik icin embedding vektorleri SQLite'ta JSON string olarak saklaniyor (BLOB/numpy yerine). Kucuk veri setleri icin performans farki onemsiz.
- **Sorumlu cikti**: Sistem prompt'u modele sadece baglamdaki bilgiyi kullanmasini ve bilmiyorsa "Bu konuda bilgim yok." demesini soyluyor; bos sorgular LLM'e gitmeden dogrudan bu cevabi donduruyor.
- **Web arayuzu**: `app.py` (Flask) + `templates/index.html` — sohbet tarzi, ornek soru chip'leri ve yanit suresi gosterimi olan basit bir web arayuzu. Flask baslarken embedding/chat modellerini onceden yukler, boylece ilk kullanici istegi model indirme/yukleme suresiyle geciktirilmez.

## Bilinen Kisitlamalar

- Kucuk yerel modeller (0.5B-2B parametre) genel amacli bulut modelleri kadar guclu degil; karmasik veya cok adimli sorularda cevap kalitesi dusebilir.
- Cosine similarity retrieval, chunk sayisi arttikca (binlerce chunk) yavaslayabilir; bu olcekte (18 chunk) sorun degil.
- Bilgi tabani sadece 6 dokumanla sinirli; kapsam disi sorularda model doğru sekilde "bilmiyorum" diyor ama bu davranis kucuk modellerde her zaman garanti degil.
- `MIN_SIMILARITY` esigi tematik olarak yakin ama yine de cevaplanamaz sorularda (ör. "Turkiye'nin baskenti neresidir?" — Turkiye gezi dokumanlarina anlamca yakin oldugu icin skor esigi asabiliyor) tam koruma saglamiyor; bu durumlarda son savunma hatti hala sistem prompt'u.
- Yanit sureleri (7-23 saniye) roadmap'teki 1-3 saniyelik hedefin uzerinde; bu, CPU/GPU'ya bagli yerel cikarimin dogal bir sonucu. Daha kucuk bir chat modeli veya donanim hizlandirmasi (NPU/GPU) sureyi azaltabilir ama cevap kalitesiyle bir denge (trade-off) gerektirir.
