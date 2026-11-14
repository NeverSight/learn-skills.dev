---
name: prompt-motion
description: >-
  Provides a curated library of 10 hand-picked AI motion video prompts and skills,
  alongside actionable workflows for generating production-grade animations using
  HTML/CSS/WebGL + headless browser rendering (Playwright/Puppeteer/Remotion) + FFmpeg.
  Use this skill whenever the user wants motion design inspiration, video generation prompts,
  or asks the agent to actually build/render a motion graphics video.
---

# 🎬 Prompt Motion Skill & Video Production Engine

Bu yetenek (skill), hem **Claude Opus 5.5 / Codex** gibi modeller için optimize edilmiş hareketli grafik (motion design) prompt kütüphanesini barındırır hem de **Antigravity / kod çalıştırabilen AI asistanlarının "ben video render edemem" demesini engelleyip** doğrudan üretim yapmasını sağlayan standart prosedürü tanımlar.

---

## 🚀 AI Ajanı İçin Kural: "Ben Video Yapamam Deme, Render Et!"

Kullanıcı senden bir motion video, showreel, sosyal medya intro'su veya promo istediğinde **asla** "ben video modeli değilim, üretemem" deme. Bunun yerine aşağıdaki 4 adımlı endüstri standardı üretim pipeline'ını işlet:

### Adım Adım Otomatik Video Üretim Pipeline'ı:

1. **HTML5 / CSS3 / WebGL Sahnesi Oluştur:**
   - 1920x1080 (veya dikey 1080x1920) çözünürlüğünde tek sayfalık modern bir `animation.html` tasarla.
   - Ambient glowlar, CSS3 3D Transformations (`perspective`, `rotateY`, `translateZ`), Glassmorphism ve kinetik tipografi kullan.
   - Sayfaya bir `window.setFrame(progress)` fonksiyonu yerleştir (`progress`: 0.0 -> 1.0 arası değer alarak sahneyi deterministik olarak ilerletir).

2. **Headless Chrome / Playwright ile Kare Kare Yakala:**
   - Sistemde kurulu Google Chrome / Chromium ve Playwright / Puppeteer kullanarak sayfayı headless aç.
   - 30 veya 60 FPS hedefiyle döngü içinde `window.setFrame(f / TOTAL_FRAMES)` çağır ve ekran görüntülerini `frames/frame_%04d.png` olarak kaydet.

3. **FFmpeg ile Ultra HD Encode Et:**
   - Kareleri tek komutla MP4 ve animasyonlu GIF'e çevir:
     ```bash
     # 1080p MP4 Çıktısı
     ffmpeg -y -framerate 30 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p output.mp4

     # Önizleme GIF Çıktısı
     ffmpeg -y -i output.mp4 -vf "fps=15,scale=960:-1:flags=lanczos" -c:v gif output.gif
     ```

4. **Kullanıcıya Doğrudan Sun:**
   - Oluşturulan `.mp4` ve `.gif` dosya yollarını tıklanabilir markdown linkiyle kullanıcıya sun.

---

## 🎨 Hazır Prompt & Stil Kütüphanesi

Repodaki `prompts/` klasöründe yer alan 10 seçkin Claude Opus 5.5 örneğini referans al:

- **Showreel & Portfolio:** `prompts/3xtihor-0f6911.md`
- **Kinetic Typography & Self-Intro:** `prompts/1littlecoder-9fef89.md`
- **Crypto & 3D Isometric Art:** `prompts/0xevinho-3777d8.md`
- **App Store & SaaS Promo:** `prompts/allforbigfire-86ff3c.md`

Her bir markdown dosyası; kullanılan tam metin prompt'u ve `assets/gifs/` altındaki görsel referansı içerir.
