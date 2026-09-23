---
name: video-production-kit
description: |
  YouTube video editleme ve paketleme skill'i. Uzun ham video kaydından kes listesi, alt yazı (SRT),
  açıklama, bölüm zaman damgaları ve sosyal medya içeriği üretir. CapCut Mac timeline'larından
  segment-doğru ses çıkarmayı bilir. ffmpeg + Whisper turbo tabanlı.
  
  TRIGGER bu skill'i çağır:
  - kullanıcı transkript / altyazı / SRT / kes listesi / YouTube açıklaması / bölüm zaman damgası /
    X thread / IG caption ister
  - CapCut, timeline, draft_info.json, ham kayıt, video editleme bahsi geçer
  - .mov / .mp4 dosyası verilmiştir ve ondan bir çıktı istenmiştir
---

# Video Production Kit — Claude Code Skill

Bu skill, video içerik üreticileri için sık tekrarlanan editleme işlerini otomatize eder.
Tek bir orkestra şefi (ana Claude) + 5 odaklanmış subagent ile çalışır.

## Ne zaman çağrıl

Aşağıdakilerden HERHANGİ BİRİ istendiğinde bu skill aktiftir:

- "altyazı / subtitle / SRT çıkar"
- "transkript çıkar / metnini al"
- "21 dakikayı 5 dakikaya indirelim / kes listesi"
- "YouTube açıklaması / description yaz"
- "bölüm zaman damgaları / chapters"
- "X thread / Twitter post / IG caption yaz"
- "CapCut timeline'ından bilgi al"

## Pipeline (kullanıcıya sunulan akış)

```
[ham video] → transcript-agent → [transkript]
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                 ↓
              cut-list-agent    subtitle-agent    description-agent
                    ↓                 ↓                 ↓
              [kes listesi]      [SRT dosyası]    [YT açıklama+bölüm]
                                                        ↓
                                                  social-agent
                                                        ↓
                                                  [X thread + IG]
```

## Subagent'ları nasıl seçeceğin

| Kullanıcı şunu isterse | Bu agent'ı çağır |
|---|---|
| transkript, dil tanıma, "ne demiş" | `transcript-agent` |
| video kısaltma, tekrar temizleme | `cut-list-agent` |
| altyazı, SRT, caption üretimi | `subtitle-agent` |
| YouTube description, chapters | `description-agent` |
| X / Twitter / Instagram metni | `social-agent` |

Birden fazlasına ihtiyaç varsa, agent'ları **paralel** çalıştır (transcript hariç —
diğerleri ona bağımlı).

## Skript kütüphanesi

`scripts/` altında her agent'ın güvendiği yardımcılar:

- `capcut_parser.py` — CapCut Mac `draft_info.json` → segment listesi
- `extract_audio.py` — Timeline-doğru ses dosyası üretir (vol=0 muted, multi-track aware)
- `transcribe.py` — Whisper turbo + word timestamps
- `make_srt.py` — Word seviyesinden ≤3.5sn / ≤80 char SRT chunk'ları + sözlük düzeltmeleri

Bütün script'ler `python3 scripts/<file>.py --help` ile çalıştırılabilir.

## Önemli kurallar

1. **Kullanıcının video dosyasını ASLA Claude API'ye yollama.** Tüm transkripsiyon lokalde
   Whisper ile yapılır. Privacy önemli.
2. **CapCut draft dosyalarını değiştirme.** Sadece oku. Değişiklik = veri kaybı riski.
3. **Çıktıları varsayılan olarak `~/Desktop/` veya `~/Downloads/` altına yaz.**
   Kullanıcı başka yer söylediyse oraya.
4. **Türkçe sözlük düzeltmesi**: `Cloud → Claude`, `Versal → Vercel`, `Antropik → Anthropic`,
   `MTP → MCP`, `X kod → Xcode`, `Mobe AI → mob.ai`. Liste `subtitle-agent.md`'de.
5. **Yeni model adı**: kullanıcı projelerinde `claude-haiku-4-5`, `claude-sonnet-4-6`,
   `claude-opus-4-7` kullanılır. Eski model adlarını önerme.

## Kullanıcıya geri dönüş tonu

- Türkçe (kullanıcının dili). İngilizce teknik terimleri olduğu gibi bırak (transcript, SRT, agent).
- Kısa. "İşte SRT, masaüstüne yazıldı" demek yeter, uzun açıklama yazma.
- Çıktı yolunu her zaman söyle.

## Hata durumu

- ffmpeg yoksa: `brew install ffmpeg` öner
- Whisper yoksa: `pip install openai-whisper` öner
- CapCut path bulunamadı: kullanıcıya `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`
  altında hangi proje olduğunu sor
- Transkript boş çıktı: ses kanalı muted mu kontrol et (vol=0 segment problemi)
