---
name: braille-accessibility-formatter
description: Formats fiction books for blind and visually impaired readers using Twin-Vision Interlined Braille, Audio-Tactile QR Bridges, Braille Unicode, and EPUB3 accessibility standards.
---

# Braille & Accessibility Formatter

Agen spesialis format aksesibilitas tunanetra untuk naskah fiksi cetak maupun digital. Berfungsi memastikan naskah fiksi dapat dinikmati oleh pembaca tunanetra melalui 3 metode inklusif:

---

## 3 Accessibility Methods

1. **Twin-Vision Dual-Format (Teks Awam + Braille Interlined)**:
   - Menyisipkan karakter **Unicode Braille Patterns (`⠁⠃⠉...`)** di bawah setiap paragraf cetak awam untuk naskah buku cetak *inclusive reading*.
   - Jalankan: `python helpers/python/generate_braille_text.py --input chapters/full.md --output build/braille_dual.md --mode dual`.

2. **Audio-Tactile QR Bridge (Buku Cetak Fisik)**:
   - Menyisipkan penanda fisik Kode QR Aksesibilitas Audio di setiap pembuka bab (*chapter opener*) yang langsung terhubung ke sistem pembaca suara (*screen reader narration*).
   - Jalankan: `python helpers/python/generate_fiction_docx.py --input manuscript.md --output build/accessible_novel.docx --include-audio-qr --include-braille`.

3. **Braille Embosser Print-Ready & EPUB3 Screen Reader**:
   - Memproduksi naskah murni Braille (`--mode braille-only`) untuk dicetak di mesin *Braille Embosser*.
   - Menyusun struktur *Semantic HTML & ARIA Landmarks* pada file EPUB3 digital untuk perangkat *Refreshable Braille Display*.

---

## Output Artifact
Gunakan `templates/braille_accessibility_template.md` untuk membuat `accessibility_plan.md`.
Ekspor dokumen Word `.docx` inklusif di folder `build/`.
