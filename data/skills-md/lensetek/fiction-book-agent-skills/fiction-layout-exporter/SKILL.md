---
name: fiction-layout-exporter
description: Formats fiction manuscripts into publisher-ready print layouts (Novel 13x19 cm & A5 DOCX/PDF) and digital e-book formats (EPUB & Mobile Web Reader).
---

# Fiction Layout Exporter

Agen spesialis penata letak dan penyiapan berkas publikasi cetak & digital untuk naskah fiksi.

---

## Export Modes & Presets

### 1. Buku Cetak Physical Print Layout (.docx & .pdf)
Jalankan skrip Python helper untuk menghasilkan format Word siap cetak:
```bash
python helpers/python/generate_fiction_docx.py \
  --input chapters/full_manuscript.md \
  --output build/manuscript_novel_13x19.docx \
  --preset novel_13x19 \
  --title "Judul Novel Anda" \
  --author "Nama Penulis"
```
- **Fasilitas Penataan Cetak & Preset Penerbit**:
  - `asadel-id`: **PT. Asadel Liamsindo Teknologi** (Default Nasional: UNESCO $15.5 \times 23\text{ cm}$, Georgia 10.5pt, Inter Bold, Deep Marine Blue & Amber Gold).
  - `asadel-intl`: **Asadel Publisher** (Default Internasional: Royal $15.6 \times 23.4\text{ cm}$, Palatino 10.5pt, Inter Bold, Midnight Blue & Gold).
  - `novel_13x19`: Standard Novel Indonesia ($13 \times 19\text{ cm}$, Garamond 11pt).
  - `A5`: Standard A5 ($14.8 \times 21\text{ cm}$).
  - `A4`: Standard A4 Script/Storybook ($21 \times 29.7\text{ cm}$).
  - Marjin Jilid (*Gutter Margin*): $2.2\text{ cm} - 2.5\text{ cm}$ marjin dalam untuk lekukan jilid buku.
  - Halaman Bab Baru (*Recto Odd-Page Break*): Bab baru selalu dimulai di halaman ganjil (halaman kanan).
  - Judul Bab (*Chapter Opener*): Diturunkan 100-120pt dari marjin atas.
  - Paragraf Pembuka Bab: Tidak menggunakan indentasi (*no first-line indent*). Paragraf berikutnya menggunakan indentasi 0.7 cm, rata kanan-kiri (*justified*).
  - Daftar Isi Dinamis: Menggunakan kode XML Word Field Code (`TOC \o "1-3" \h \z \u`).

### 2. Digital E-Book & Mobile Web Reader
- Menghasilkan file EPUB terstruktur.
- Mengompilasi aplikasi pembaca digital responsive mobile-first di folder `web_reader/`.

---

## Output Artifact
File `.docx` di folder `build/`, file `.epub`, dan aplikasi Web Reader siap buka di `web_reader/index.html`.
