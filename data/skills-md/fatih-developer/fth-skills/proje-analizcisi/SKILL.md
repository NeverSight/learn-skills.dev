---
name: proje-analizcisi
description: "Mevcut bir yazılım projesini derinlemesine analiz eder ve docs/analyze/ klasörüne 3-4 adet kapsamlı rapor üretir. 'Projeyi analiz et', 'kod analizi yap', 'proje inceleme', 'mimari rapor', 'teknik borç', 'proje değerlendirme', 'codebase analiz' gibi ifadeler geçtiğinde tetikle. Proje dizini veya repo URL'i verildiğinde çalışır. API endpoint'leri tespit edilirse otomatik olarak 4. raporu da üretir."
---

# Proje Analizcisi Skill

**Çıktılar:**
- `docs/analyze/01-proje-genel-bakis.md`
- `docs/analyze/02-mimari-ve-kod-kalitesi.md`
- `docs/analyze/03-riskler-ve-oneriler.md`
- `docs/analyze/04-api-endpoint-listesi.md` (sadece API varsa)

Projeyi sistematik olarak tara, derin analiz yap, bulgularını 3 (API varsa 4) ayrı rapora dönüştür ve `docs/analyze/` klasörüne kaydet.

**Temel kural:** Yüzeysel geçme. Her başlık için gerçekten koda bak, dosyaları oku, örnek ver. Rapor somut bulgular içermeli — genel geçer değerlendirme yapma.

---

## AŞAMA 1 — Proje Keşfi (Önce Bunu Yap)

Analiz başlamadan projeyi tanı. Keşif betiğini çalıştır:

```bash
bash ~/.gemini/antigravity/skills/proje-analizcisi/scripts/phase1_discovery.sh
```

**Keşif sonrası şunları not et:**
- Ana dil(ler) ve framework(ler)
- Proje tipi: monolith / microservice / monorepo / library
- Paket yöneticisi
- Test varlığı: var mı, yaygın mı?
- API tipi: REST / GraphQL / gRPC / WebSocket / yok

---

## AŞAMA 2 — Derin Analiz

Her kategoride koda gir, oku, somut bulgular çıkar. Analiz betiğini çalıştır:

```bash
bash ~/.gemini/antigravity/skills/proje-analizcisi/scripts/phase2_analysis.sh
```

Senaryonun çıktılarını dikkatle incele. Betik şunları içerir:
- Mimari (klasör yapıları, büyük dosyalar, circular dependency ipuçları)
- Kod Kalitesi (TODO'lar, `any` kullanımı, console.log'lar, tekrar eden kod blokları, hata yönetimi)
- Güvenlik (hardcoded secret'ler, .env sızmaları, SQL injection riski, güvensiz paketler, auth middleware)
- Performans (N+1 sorgu riski, ağır bundle'lar, önbellek kullanımı, async/await durumları)
- Testler (dosyalar ve yapılandırma oranları)
- API tespiti (REST endpoint'leri, FastAPI/Django route'ları, GraphQL tipleri, Swagger/OpenAPI dosyaları)

---

## AŞAMA 3 — Rapor Üretimi

`docs/analyze/` klasörünü oluştur ve 3 (veya 4) raporu kaydet.

```bash
mkdir -p docs/analyze
```

---

### RAPOR 1: `01-proje-genel-bakis.md`

```markdown
# Proje Genel Bakış

> Analiz tarihi: [TARIH]
> Analiz eden: Proje Analizcisi Skill v1.0

## Özet Kartı

| Özellik | Değer |
|---------|-------|
| Proje adı | [package.json name veya klasör adı] |
| Proje tipi | [Monolith / Microservice / Monorepo / Library] |
| Ana dil | [TypeScript / Python / Go / ...] |
| Framework | [Hono / FastAPI / Express / Next.js / ...] |
| Paket yöneticisi | [bun / pnpm / yarn / pip / ...] |
| Toplam kaynak dosyası | [N] |
| Toplam kod satırı | [N] |
| Test kapsamı | [Var / Yok / Kısmi] |
| API tipi | [REST / GraphQL / gRPC / Yok] |
| Son commit | [tarih] |
| Aktif geliştirici | [N kişi] |

## Proje Amacı

[package.json description veya README'den özet — kendi cümlelerinle açıkla]

## Klasör Yapısı

[find çıktısından temiz bir ağaç göster, her klasörün amacını bir satırla açıkla]

## Teknoloji Yığını

### Üretim Bağımlılıkları
[Her önemli paketi listele, amacını yaz]

### Geliştirme Araçları
[Test, lint, build araçlarını listele]

## Geliştirme Süreci Göstergeleri

| Gösterge | Değer | Yorum |
|----------|-------|-------|
| Son 3 ay commit | [N] | [aktif / düşük / yok] |
| Test / kaynak oranı | [%N] | [iyi / orta / yetersiz] |
| TODO sayısı | [N] | [temiz / dikkat / sorunlu] |
| Dokümantasyon | [Var / Kısmi / Yok] | |

## Güçlü Yönler

[Gerçekten iyi olan şeyleri yaz — somut, kod referanslı]

## Zayıf Yönler

[Somut sorunlar — "genel olarak kötü" değil, "X dosyasında Y sorunu var" gibi]
```

---

### RAPOR 2: `02-mimari-ve-kod-kalitesi.md`

```markdown
# Mimari ve Kod Kalitesi Analizi

## Mimari Değerlendirme

### Katman Yapısı
[Katmanlar var mı? Controller/Service/Repository ayrımı? Somut örnekler ver]

### Bağımlılık Yönetimi
[Circular dependency var mı? Import zinciri mantıklı mı?]

### Modülerlik Skoru
[ ⭐⭐⭐⭐⭐ ] — [gerekçe]

## Kod Kalitesi Metrikleri

| Metrik | Değer | Durum |
|--------|-------|-------|
| En büyük dosya | [dosya adı: N satır] | [✅ / ⚠️ / 🔴] |
| any kullanımı (TS) | [N adet] | [✅ / ⚠️ / 🔴] |
| TODO/FIXME sayısı | [N] | [✅ / ⚠️ / 🔴] |
| console.log (prod) | [N] | [✅ / ⚠️ / 🔴] |
| try/catch oranı | [N try, N catch] | [✅ / ⚠️ / 🔴] |

## Dikkat Gerektiren Dosyalar

[En büyük, en karmaşık, en çok TODO içeren dosyaları listele — neden riskli olduğunu açıkla]

### [dosya-adi.ts] — [N satır]
> Neden dikkat: [açıklama]
> Öneri: [ne yapılmalı]

## Tekrar Eden Kod (DRY İhlalleri)

[Benzer mantık farklı yerlerde mi yazılmış? Somut örnekler]

## Error Handling Kalitesi

[try/catch var mı? Hata mesajları anlamlı mı? Unhandled promise rejection riski?]

## Tip Güvenliği (TypeScript)

[any kullanımı, strict mode açık mı, tip tanımları eksiksiz mi?]

## Genel Kod Kalitesi Skoru

```
Mimari      : [1-10] / 10
Okunabilirlik: [1-10] / 10  
Sürdürülebilirlik: [1-10] / 10
Test Kapsamı: [1-10] / 10
─────────────────────────
Genel       : [ortalama] / 10
```

## En İyi Yazılmış Bölümler

[Gerçekten iyi olan kod parçaları — somut örnek ver]

## En Çok İyileştirme Gereken Bölümler

[Somut, öncelikli iyileştirme önerileri — her biri için tahmini efor belirt]
```

---

### RAPOR 3: `03-riskler-ve-oneriler.md`

```markdown
# Riskler ve Öneriler

## Risk Matrisi

| Risk | Kategori | Etki | Olasılık | Öncelik |
|------|----------|------|----------|---------|
| [risk adı] | [Güvenlik/Performans/Teknik Borç/Operasyon] | [Yüksek/Orta/Düşük] | [Y/O/D] | [🔴/🟡/🟢] |

## 🔴 Kritik Riskler (Hemen Müdahale)

### [Risk Adı]
**Kategori:** [Güvenlik / Performans / ...]
**Nerede:** [dosya:satır veya modül]
**Sorun:** [somut açıklama]
**Kanıt:** [grep çıktısı veya kod örneği]
**Düzeltme:** [adım adım ne yapılmalı]
**Tahmini Efor:** [1 saat / 1 gün / 1 hafta]

## 🟡 Önemli Riskler (Kısa Vadede Ele Al)

[Aynı format — 3-5 risk]

## 🟢 İyileştirme Önerileri (Uzun Vade)

[Aynı format — 3-5 öneri]

## Güvenlik Analizi

### Pozitif Bulgular
[İyi güvenlik pratikleri — somut]

### Endişe Verici Bulgular
[Somut güvenlik açıkları veya riskler]

## Performans Analizi

### Darboğaz Adayları
[N+1 sorgu, ağır paket, cache eksikliği, async sorunları]

### İyileştirme Fırsatları
[Somut öneriler ve beklenen kazanım]

## Teknik Borç Envanteri

| Borç | Dosya/Modül | Tahmini Efor | Öncelik |
|------|-------------|--------------|---------|
| [açıklama] | [yer] | [efor] | [🔴/🟡/🟢] |

## Önerilen Eylem Planı

### Bu Hafta
1. [en kritik, somut adım]
2. [...]

### Bu Ay
1. [önemli iyileştirmeler]
2. [...]

### Uzun Vade (3-6 Ay)
1. [mimari iyileştirmeler]
2. [...]

## Genel Sağlık Skoru

```
Güvenlik     : [1-10] / 10
Performans   : [1-10] / 10
Sürdürülebilirlik: [1-10] / 10
Test Kapsamı : [1-10] / 10
Dokümantasyon: [1-10] / 10
─────────────────────────────
Proje Sağlığı: [ortalama] / 10
```
```

---

### RAPOR 4: `04-api-endpoint-listesi.md` (Sadece API Varsa)

```markdown
# API Endpoint Listesi

> Otomatik tarama ile oluşturulmuştur.
> Tarih: [TARIH]

## Özet

| Metrik | Değer |
|--------|-------|
| Toplam endpoint | [N] |
| GET | [N] |
| POST | [N] |
| PUT/PATCH | [N] |
| DELETE | [N] |
| Auth gerektiren | [N] (tahmini) |
| Dokümante edilmiş | [N] |

## Endpoint Katalogu

### [/api/auth] — Kimlik Doğrulama
| Metot | Path | Açıklama | Auth | Kaynak Dosya |
|-------|------|----------|------|--------------|
| POST | /api/auth/register | Kullanıcı kaydı | ❌ | src/routes/auth.ts:12 |
| POST | /api/auth/login | Giriş | ❌ | src/routes/auth.ts:28 |
| POST | /api/auth/logout | Çıkış | ✅ | src/routes/auth.ts:45 |
| GET | /api/auth/me | Mevcut kullanıcı | ✅ | src/routes/auth.ts:58 |

### [/api/...] — [diğer gruplar]
[aynı format — endpoint'leri gruplandır]

## Auth Gereksinim Analizi

[Hangi endpoint'ler korumalı, hangisi açık? Eksik auth var mı?]

## Eksik Dokümantasyon

[Swagger/OpenAPI tanımı olmayan endpoint'ler]

## Güvenlik Notları

[Rate limit eksik mi? Input validation var mı? CORS ayarı nasıl?]

## Tavsiyeler

[OpenAPI spec üretimi, versiyon stratejisi, eksik endpoint'ler]
```

---

## AŞAMA 4 — Dosyaları Kaydet

```bash
# Klasörü oluştur
mkdir -p docs/analyze

# Raporları kaydet
# (Her raporu ayrı write_file çağrısıyla kaydet)

# Özet göster
echo "✅ Analiz tamamlandı"
echo "📁 docs/analyze/"
ls -la docs/analyze/
```

---

## Kalite Kontrol

Her raporu kaydetmeden önce şu kontrolleri yap:

```
□ Genel geçer ifade yok — her cümle somut veri veya bulgua dayalı
□ Kod referansları var — "X dosyası N satır", "Y fonksiyonu Z problemi"
□ Sayısal metrikler gerçek (grep/wc çıktısından)
□ Risk öncelikleri mantıklı — her şey kırmızı değil
□ Öneriler uygulanabilir — "kodu iyileştir" değil, "X yapılmalı"
□ Skorlar gerekçeli — neden 7/10? çünkü...
□ API raporu: her endpoint için kaynak dosya referansı var
```

---

## Hata Senaryoları

**Git repo değilse:**
→ Git istatistiklerini atla, diğer her şeyi analiz et

**Çok büyük proje (>50K satır):**
→ Her kategoriden örneklem al, raporda bunu belirt

**Test hiç yoksa:**
→ Test kapsamı: 0% olarak raporla, tavsiyeler bölümüne test stratejisi ekle

**API tespiti belirsizse:**
→ "API tespit edilemedi" yaz, 4. rapor üretme — şüpheli dosyaları listele

**İzin hatası:**
→ Erişilemeyen dosyaları atla, raporda belirt

---

## Ne Zaman Atlarsın

- Proje dizini verilmemişse ve kullanıcı sadece genel soru soruyorsa
- Analiz edilecek kod yoksa (boş proje, sadece config dosyaları)
