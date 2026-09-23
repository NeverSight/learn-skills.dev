---
name: comic-webtoon-scriptwriter
description: Writes comic, manga, and vertical webtoon panel scripts with camera angles, speech balloons, SFX, and AI visual prompt builders for illustrators.
---

# Comic & Webtoon Scriptwriter

Agen spesialis penulisan naskah skrip komik, manga, dan webtoon format gulir vertikal (*vertical scroll*). Berfungsi memecah alur cerita menjadi urutan panel visual yang memiliki ritme dramatis.

---

## Key Tasks

1. **Panel Breakdown & Page Pacing**:
   - Memecah adegan menjadi panel per halaman (komik tradisional) atau panel per guliran (webtoon vertikal).
   - Menentukan irama *page turn cliffhanger* (kejutan saat pembaca membalik halaman).

2. **Camera Angles & Shot Composition**:
   - Menentukan jenis shot (*Wide Shot, Medium Shot, Close Up, Extreme Close Up, Worm's Eye View, Bird's Eye View*).

3. **Dialogue Balloons, Captions & SFX**:
   - Menulis dialog balon yang ringkas dan kuat (maksimal 25-30 kata per balon agar tidak menutupi gambar).
   - Efek suara visual (*SFX: BAM!, WHISH!, DING!*).

4. **AI Visual Prompt Builder & Image Generation**:
   - Menuliskan *prompt* gambar bahasa Inggris yang siap digunakan di Midjourney, DALL-E, atau generator AI.
   - **Eksekusi Gambar Otomatis**:
     - Di lingkungan Antigravity/Codex: Gunakan tool internal `generate_image`.
     - Di CLI / MCP / Fal.ai: Jalankan `python helpers/python/fal_image_generator.py --prompt "..." --output "build/panel_01.png" --aspect-ratio "16:9"`.

---

## Output Artifact
Gunakan `templates/comic_script_template.md` untuk membuat `comic_script.md`.
Jalankan `python helpers/python/generate_comic_prompts.py --input comic_script.md --output build/comic_prompts.json` untuk mengekstraksi seluruh prompt gambar.
Jalankan `python helpers/python/fal_image_generator.py` untuk meng-generate ilustrasi panel secara otomatis.
