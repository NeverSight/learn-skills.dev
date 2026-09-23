---
name: wattpad-publisher-formatter
description: Formats, serializes, and optimizes fiction manuscripts for Wattpad. Generates 1,500-2,500 word episodes, cliffhanger endings, Wattpad tag recommendations, hook blurbs, Vote/Comment Author Notes (A/N), and 2:3 Wattpad cover prompts.
metadata:
  short-description: Serialize & format fiction stories for Wattpad web-novel publishing
---

# Wattpad Publisher Formatter

Agen spesialis penataan, serialisasi, dan optimasi cerita fiksi untuk platform **Wattpad**. Skill ini memecah naskah novel menjadi episode web-novel yang ideal untuk pembaca mobile ($1.500 - 2.500\text{ kata}$), mengoptimalkan tag rekomendasi algoritma Wattpad, menyusun *Author Notes* (A/N) pemicu Vote ⭐ & Komentar, serta menyiapkan spesifikasi cover Wattpad rasio $2:3$.

---

## Agent Contract

### Input:
- **Manuscript / Chapter Drafts**: Naskah novel utuh atau draf bab.
- **Title & Author Name**: Judul cerita dan nama pena di Wattpad.
- **Genre & Tropes**: Genre (Romance, Teen Fiction, Fantasy, Mystery, CEO, Bad Boy, Slow Burn, dll.).
- **Target Audience & Rating**: General (Semua Umur) atau Mature (18+).

### Output:
- `status`: `ready`, `needs_input`, atau `completed`.
- `wattpad_story_setup`:
  - **Judul Wattpad & Catchy Subtitle**.
  - **Sinopsis Hook Wattpad**: Di bawah 2.000 karakter dengan kutipan teaser dialog di bagian paling atas.
  - **Kategori & Rating**: Kategori utama dan label batas usia.
  - **Wattpad Hashtag Engine**: 20–30 hashtag rekomendasi pencarian (`#romance`, `#indonesia`, `#teenfiction`, `#fantasy`, dll.).
  - **Prompt Cover Wattpad**: Prompt visual gambar AI rasio $2:3$ ($512 \times 800\text{ px}$ / $1024 \times 1600\text{ px}$).
- `wattpad_episodes`: Berkas episode terpisah di folder `wattpad_build/` yang berisi:
  - Panjang kata ideal ($1.500 - 2.500\text{ kata}$ per bab).
  - *Cliffhanger* / gantung cerita di akhir bab.
  - Spasi antar-paragraf ramah *inline comment*.
  - *Author's Note* (A/N) di awal dan akhir bab untuk mendorong *Vote* ⭐ dan *Comment*.

---

## Panduan Serialisasi Bab Wattpad

### 1. Ukuran Kata Ideal per Episode
- **Panjang Ideal**: $1.500 - 2.500\text{ kata}$ per episode.
- Jika bab naskah cetak melebihi $3.500\text{ kata}$, pecah menjadi **Bagian 1** dan **Bagian 2** (misal: *Bab 12: Pengakuan (Bagian 1)* & *Bab 12: Pengakuan (Bagian 2)*).

### 2. Format Paragraf & Inline Comments
- Gunakan spasi ganda antar-paragraf agar pembaca Wattpad dapat memberikan komentar pada kalimat spesifik (*inline comments*).
- Hindari blok paragraf yang terlalu panjang (maksimal 3-4 kalimat per paragraf).

### 3. Template Author Note (A/N) & Call-to-Action (CTA)

#### A/N Pembuka (Awal Bab):
```text
Halo semuanya! Selamat membaca Bab [Nomor Bab] ❤️
Jangan lupa klik tombol Bintang ⭐ di bawah sebelum baca ya!
```

#### A/N Penutup (Akhir Bab):
```text
***
Gimana menurut kalian bab ini? Sampaikan kesan kalian di kolom komentar ya! 💬
Jangan lupa klik VOTE ⭐ dan tambahkan cerita ini ke Perpustakaan / Reading List kalian agar tidak ketinggalan update selanjutnya!

Sampai jumpa di bab berikutnya! ✨
```

---

## Generator Tag Wattpad (Wattpad Hashtag Engine)

Dapatkan kombinasi 20-30 hashtag Wattpad populer untuk meningkatkan peringkat di algoritma rekomendasi:
- **Hashtag Utama**: `#indonesia`, `#wattpadindonesia`, `#fiksi`, `#novel`
- **Hashtag Genre**: `#romance`, `#teenfiction`, `#fantasy`, `#mystery`, `#chicklit`
- **Hashtag Trope**: `#slowburn`, `#badboy`, `#ceo`, `#enemies-to-lovers`, `#fake-relationship`, `#marriage-life`
- **Hashtag Emosi**: `#bikinbaper`, `#angst`, `#sweet`, `#drama`

---

## Otomasi Pemecahan Bab via Python Helper

Jalankan skrip Python helper untuk memecah naskah novel utuh menjadi berkas episode Wattpad siap pakai:
```bash
python helpers/python/format_wattpad_chapters.py \
  --input chapters/full_manuscript.md \
  --output-dir wattpad_build \
  --title "Judul Novel Wattpad" \
  --author "Nama Pena Penulis"
```

Skrip akan membuat:
1. `wattpad_build/wattpad_story_setup.md` (Sinopsis, 25 Hashtag, Prompt Cover 2:3, Rating).
2. `wattpad_build/episode_001.md`, `episode_002.md`, dst. (Terformat A/N Vote & Comment).
