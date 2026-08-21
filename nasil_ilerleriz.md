# Nasıl İlerleriz: Foundry Local ile Yerel RAG Yaz Okulu — Yol Haritası

Bu belge, "Local RAG AI Assistant with Microsoft Foundry Local" planına dayanarak hazırlanmış, doğrudan uygulanabilir bir aksiyon rehberidir. Amaç: yeni başlayan bilgisayar bilimi öğrencilerine, tamamen çevrimdışı çalışan bir RAG (Retrieval-Augmented Generation) soru-cevap asistanını 5-6 haftada, adım adım inşa ettirmek.

---

## 0. Programdan Önce: Eğitmen Hazırlığı (Hafta 0)

Programın ilk gününden önce tamamlanması gereken işler:

- [ ] Foundry Local'ı kendi makinende (Windows ve varsa macOS) kur ve test et — öğrencilere yardım edebilmek için kurulum sürecini önceden bizzat yaşa.
- [ ] 5–10 adet kısa doküman seç (teknik makale, ürün SSS'si, ders notu vb.) — bunlar öğrencilerin bilgi tabanını oluşturacak.
- [ ] Öğrencilerin bilgisayarlarının minimum donanım gereksinimlerini (CPU/GPU/NPU, disk alanı) karşıladığından emin ol.
- [ ] Python, pip, VS Code gibi temel araçların tüm öğrenci makinelerinde kurulu olduğunu doğrula.
- [ ] Referans kaynakları (aşağıdaki "Kaynaklar" bölümü) bir okuma listesi halinde öğrencilerle paylaş.
- [ ] Takımları oluştur (bireysel ya da küçük gruplar halinde ilerlenecekse).

---

## Faz 1 — Temel Öğrenme (Hafta 1–2)

**Hedef:** Hafta 2 sonunda öğrenciler RAG'ın nasıl çalıştığını anlamalı, Foundry Local kurulu ve test edilmiş olmalı, örnek bir SQLite veritabanı oluşturulmuş olmalı.

### Hafta 1: RAG Kavramı & Yerel AI Kurulumu

- [ ] **RAG'a giriş:** Genel bir LLM'e alana özgü bir soru sorup yanlış cevap almasını göster, ardından RAG'ın "retrieve, augment, generate" adımlarını anlat.
  - *Egzersiz:* Q&A rol yapma — biri "retriever" (ilgili paragrafı bulan), diğeri "LLM" (bu bilgiyle cevap üreten) rolünü oynar.
- [ ] **Foundry Local & ortam kurulumu:** Foundry Local'ın ne olduğunu, tamamen cihaz üzerinde (offline) çalıştığını anlat.
  - *Egzersiz:* Her öğrencinin makinesine Foundry Local SDK'yı kurdur (`pip install foundry-local-sdk` veya işletim sistemine özgü varyant). "Hello Model" testi yaptır: küçük bir model (örn. phi-1.5-mini) yükleyip basit bir tamamlama üretsin.
- [ ] **Temel Python proje yapısı:** `main.py`, `if __name__ == "__main__": main()` deseni, `requirements.txt` ile bağımlılık yönetimi.
  - *Egzersiz:* İskelet proje klasörü oluştur, `main.py` ile basit bir selamlama yazdır.

**Hafta 1 sonu kilometre taşı:** ✅ Herkeste Foundry Local kurulu ve çalışıyor, temel proje klasörü hazır, basit bir çıkarım (inference) test edilmiş.

### Hafta 2: Embeddings, Vektör Arama & SQLite

- [ ] **Embeddings & vektör benzerliği:** Metin embedding'lerinin ne olduğunu, benzer metinlerin benzer vektörlere karşılık geldiğini, cosine similarity ile ölçüldüğünü anlat.
  - *Egzersiz:* Örnek cümlelerden embedding üret (örn. qwen3-embedding-0.6b), bir sorgu için en yakın eşleşmeyi bulan basit bir döngü yazdır.
- [ ] **SQLite ile embedding saklama/sorgulama:** SQLite'ın sunucusuz, tek dosyalık yapısını ve temel SQL işlemlerini (tablo oluşturma, ekleme, sorgulama) anlat.
  - *Egzersiz:* `id`, `content`, `embedding` alanlarına sahip bir `documents` tablosu oluştur, birkaç örnek satır ekleyip sorgulat.
- [ ] **Temel prompt engineering:** Sistem/kullanıcı prompt ayrımı, "bağlamda yoksa bilmiyorum de" gibi temel kurallar.
  - *Egzersiz:* Aynı soruyu bağlamlı/bağlamsız bir genel AI'a (Bing Chat, ChatGPT) sorup farkı gözlemlet.

**Hafta 2 sonu kilometre taşı:** ✅ RAG, Foundry Local, embeddings ve SQLite konusunda temel bilgi edinildi; test SQLite veritabanı oluşturuldu (veya şeması tasarlandı); hands-on geliştirmeye hazır.

---

## Faz 2 — Proje Geliştirme (Hafta 3–4)

**Hedef:** Fonksiyonel bir yerel RAG uygulaması geliştirmek — veri alımı, vektörleştirme, retrieval ve LLM entegrasyonu.

### Hafta 3: Veri Alımı & Retrieval Pipeline

- [ ] **Bilgi tabanı tasarımı:** Seçilen 5–10 dokümanı belirle, dokümanları parçalara (chunk, ~1–3 paragraf) bölme stratejisini tartış.
- [ ] **Veri alım (ingestion) script'i yazdır:**
  1. Dokümanları chunk'lara böl.
  2. Her chunk için Foundry Local embedding modeliyle embedding hesapla.
  3. Chunk + embedding'i SQLite'a kaydet.
  - *Test:* İşlem sonrası veritabanındaki kayıt sayısını doğrula.
- [ ] **Retrieval fonksiyonunu yazdır:** `get_top_chunks(query)` — sorguyu embed et, SQLite'taki tüm embedding'lerle cosine similarity hesapla, en alakalı 2–3 chunk'ı döndür.
  - *Test:* Dokümanlarda cevabı bilinen sorularla fonksiyonu dene, getirilen chunk'ların alakalı olduğunu doğrula.

**Hafta 3 sonu kilometre taşı:** ✅ Embedding'lerle doldurulmuş bir SQLite veritabanı ve çalışan bir retrieval fonksiyonu hazır.

### Hafta 4: LLM Entegrasyonu & Uygulama Montajı

- [ ] **Yerel LLM entegrasyonu:** Foundry Local üzerinden küçük bir sohbet modeli (örn. Phi-3.5 Mini) yükle, chat completion API'sini kullan.
  - *Egzersiz:* `answer_query(user_question)` fonksiyonunu yaz — `get_top_chunks()` ile bağlamı al, sistem mesajıyla (sadece bağlamı kullan) birlikte modele gönder. Uçtan uca test et.
- [ ] **Arayüz seçimi ve geliştirme** (biri seçilir):
  - [ ] **Seçenek A — CLI:** En basit yol, `input()` ile soru al, cevabı yazdır.
  - [ ] **Seçenek B — Streamlit/Gradio:** Web tabanlı basit arayüz.
  - [ ] **Seçenek C — HTML+JS + Flask/Express backend:** İleri seviye öğrenciler veya stretch goal için.
- [ ] **Sorumlu çıktı kontrolleri:** Bağlam yetersizse "bilmiyorum" desin, kaynak adlarını cevaba dahil etme (opsiyonel: "Document X'e göre...").

**Hafta 4 sonu kilometre taşı:** ✅ Her takımda, kullanıcı sorusunu alıp SQLite tabanlı bilgi tabanından bilgi çekerek yerel LLM ile cevap üreten çalışan bir Q&A uygulaması var. Temel proje işlevselliği tamamlandı.

---

## Faz 3 — Test, Değerlendirme & Dokümantasyon (Hafta 5–6)

**Hedef:** Uygulamayı test etmek, performansı değerlendirmek, dokümantasyon ve sunum hazırlamak.

### Hafta 5: Sistem Testi & Değerlendirme

- [ ] **Fonksiyonel testler:** Cevaplanabilir/cevaplanamaz soru setleri hazırlat; sistemin doğru cevap verdiğini, bilgi eksikse fallback mesajı döndürdüğünü, edge case'leri (boş sorgu, çok genel soru) idare ettiğini doğrula. Takımlar arası soru değişimi ile "gerçek kullanıcı" simülasyonu yapılabilir.
- [ ] **Performans & debug:** Yanıt sürelerinin makul olduğunu (~1–3 saniye) kontrol et; yavaşsa chunk sayısını azaltma, daha küçük model kullanma veya embedding cache'leme gibi optimizasyonları tartış.
- [ ] **Değerlendirme & iyileştirme:** Cevapların doğruluğunu, açıklığını, kaynak gösterip göstermediğini gözden geçirt; gerekirse prompt formatını veya chunk bölme stratejisini iyileştir.

**Hafta 5 ortası kilometre taşı:** ✅ Test sonuçları dokümante edildi — denenen sorgular ve doğru/uygun olup olmadıkları listelendi; eksiklikler belirlendi ve son düzenlemeler planlandı.

### Hafta 6 (veya Hafta 5 sonu): Dokümantasyon & Final Sunumu

- [ ] **Proje dokümantasyonu:** Her takım kısa bir Proje Raporu/README yazsın — amaç, nasıl çalıştığı, çalıştırma talimatları, tasarım kararları ve kısıtlamalar.
- [ ] **Kod temizliği:** Debug print'lerini kaldır, ana bölümlere açıklayıcı yorumlar ekle, kod stilini tutarlı hale getir; (opsiyonel) versiyon kontrolüne kısa değin.
- [ ] **Final sunum hazırlığı:** Her grup kısa bir demo + sunum hazırlasın:
  - Problem tanımı (hangi senaryo/ihtiyaç hedefleniyor?)
  - Ana özellikler/bileşenler (RAG nasıl kullanıldı, hangi veri kaynakları?)
  - Canlı demo (örnek sorular, biri kaynak gösteren, biri "bilmiyorum" diyen)
  - Öğrenilen dersler (1-2 içgörü/zorluk)

**Hafta 6 sonu kilometre taşı:** ✅ Tüm takımların dokümantasyonu tamamlanmış projeleri var, sunum/demo prova edilmiş. Program, her takımın kendi yerel RAG asistanını sunduğu bir demo günüyle sona erer.

---

## Kaynaklar

- Microsoft Tech Community — [Building Your First Local RAG Application with Foundry Local](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/building-your-first-local-rag-application-with-foundry-local/4501968)
- Microsoft Learn — [What is Foundry Local?](https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local)
- Microsoft Learn — [Tutorial: Build a RAG application](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)
- Microsoft Learn — [SQLite ile veri erişimi](https://learn.microsoft.com/en-us/windows/apps/develop/data-access/sqlite-data-access)
- Microsoft Learn — [Prompt engineering techniques](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering)
- SQLite resmi site — [sqlite.org](https://sqlite.org/index.html)

## Dikkat Edilmesi Gerekenler / Riskler

- Öğrenci makineleri arasında donanım farklılıkları (CPU/GPU/NPU) model seçimini ve performansı etkileyebilir — küçük modellerle (Phi-3.5 Mini, phi-1.5-mini gibi) başlamak riski azaltır.
- Program "tam zamanlı bir aylık" olarak tasarlanmış; zaman daralırsa Faz 3 (test + dokümantasyon) Hafta 5 sonuna sıkıştırılabilir — planın kendisi buna izin veriyor.
- Windows ve macOS kurulum farklılıkları için Hafta 1'de her iki platformu da test etmek önemli.
- Gelişmiş arayüz seçenekleri (Streamlit/Gradio, HTML+JS) zaman kısıtlıysa stretch goal olarak bırakılmalı; CLI seçeneği tamamlanmayı garanti eder.
