---
name: fiction-cover-designer
description: Use to create front cover, back cover, spine specifications, visual image prompts, and print-ready cover briefs for fiction books, novels, comics, webtoons, children's storybooks, and Braille accessibility books. Supports publisher branding for PT. Asadel Liamsindo Teknologi and Asadel Publisher.
metadata:
  short-description: Design fiction book cover specifications, spine math, and AI image prompts
---

# Fiction Cover Designer

Agen spesialis perancang spesifikasi sampul buku fiksi, novel, skrip komik/webtoon, buku cerita anak, dan buku aksesibilitas Braille. Skill ini menghasilkan *design brief*, formulasi *prompt* AI generator gambar (FAL.ai, Midjourney, DALL-E), perhitungan lebar punggung buku (*spine width*), serta panduan area aman cetak (*preflight bleed*).

---

## Agent Contract

### Input:
- **Title & Subtitle**: Judul novel/cerita, sub-judul, atau nama seri/trilogi.
- **Author/Creator Names**: Nama penulis, ilustrator, atau pembuat cerita.
- **Book Type**: Novel, Komik/Webtoon, Buku Cerita Anak (*Picture Book*), atau Buku Braille/Aksesibilitas.
- **Publisher & Imprint**: `PT. Asadel Liamsindo Teknologi` (Default Nasional), `Asadel Publisher` (Default Internasional), atau penerbit kustom.
- **Target Audience & Tone**: Genre (Fantasy, Romance, Sci-Fi, Horror, YA, Children), mood warna, dan atmosfer visual.
- **Page Size**: `UNESCO` ($15.5 \times 23\text{ cm}$), `novel_13x19` ($13 \times 19\text{ cm}$), `A5` ($14.8 \times 21\text{ cm}$), `Royal` ($15.6 \times 23.4\text{ cm}$), atau `US Trade 6x9 in`.
- **Page Count & Paper GSM**: Jumlah halaman total dan jenis kertas (misal HVS 70gsm, Bookpaper 57gsm/72gsm) untuk perhitungan punggung buku (*spine*).
- **Back-Cover Content**: Sinopsis/blurb pikat, kutipan rekomendasi (*endorsement*), bio singkat penulis, dan area barcode/ISBN.

### Output:
- `status`: `ready`, `needs_input`, atau `completed`.
- `cover_brief`: Konsep visual utama, palet warna hex, dan moodboard.
- `front_cover_spec`: Tata letak judul, subjudul, nama penulis, dan logo penerbit.
- `back_cover_spec`: Tata letak blurb sinopsis, kutipan hook, bio penulis, area ISBN/barcode, dan logo imprint penerbit.
- `spine_spec`: Lebar punggung buku (mm) berdasarkan jumlah halaman dan gramatur kertas.
- `image_generation_prompt`: Formulasi prompt AI generator gambar resolusi tinggi siap pakai untuk FAL.ai / Midjourney.
- `typography_and_color_direction`: Pasangan font Serif/Sans/Display dan skema warna penerbit Asadel.
- `safe_area_and_print_notes`: Spesifikasi bleed (3mm), marjin aman (5mm), dan resolusi 300 DPI.

---

## Formula Perhitungan Punggung Buku (Spine Math)

Untuk menghitung lebar punggung buku (*spine width*):
$$\text{Spine Width (mm)} = \left(\frac{\text{Total Halaman}}{2}\right) \times \text{Ketebalan Kertas (mm)} + 1.5\text{mm Bleed}$$

### Ketebalan Kertas Standar Penerbit:
- **Bookpaper 55gsm / 57gsm**: $0.09\text{ mm}$ per lembar.
- **Bookpaper 72gsm**: $0.11\text{ mm}$ per lembar.
- **HVS 70gsm**: $0.095\text{ mm}$ per lembar.
- **HVS 80gsm**: $0.105\text{ mm}$ per lembar.
- **Art Paper 120gsm / 150gsm** (Buku Anak/Komik): $0.12\text{ mm} - 0.15\text{ mm}$ per lembar.

*Contoh*: Novel 240 halaman menggunakan Bookpaper 57gsm:
$$\text{Spine Width} = \left(\frac{240}{2}\right) \times 0.09\text{ mm} + 1.5\text{ mm} = 10.8\text{ mm} + 1.5\text{ mm} = 12.3\text{ mm}$$

---

## Panduan Visual per Jenis Buku Fiksi

### 1. Novel Fiksi (General / Romance / Fantasy / Mystery)
- **Cover Depan**: Ilustrasi utama/fokus karakter dengan judul menonjol (Display/Serif Font).
- **Branding Penerbit**: Logo `PT. Asadel Liamsindo Teknologi` atau `Asadel Publisher` diletakkan di sudut bawah cover depan dan bagian bawah punggung buku.
- **Prompt AI**: `cinematic book cover art, [genre/mood description], hyper-detailed, elegant typography framing, 8k resolution, photorealistic or digital painting style`.

### 2. Komik & Webtoon Vertikal
- **Cover Depan**: Dynamic action pose, bold comic typography, cel-shaded or anime art style.
- **Prompt AI**: `vibrant comic book cover, anime illustration style, dynamic action pose of main character, bold graphic background, 8k resolution`.

### 3. Buku Cerita Anak (Picture Storybook)
- **Cover Depan & Spreads**: Full wraparound illustration (depan & belakang menyambung), warna cerah kontras tinggi, font sans-serif bulat/ramah anak.
- **Prompt AI**: `charming children's book cover illustration, cute storybook art style, soft pastel palette, warm lighting, whimsical character design, 8k`.

### 4. Buku Aksesibilitas & Braille (Twin-Vision)
- **Cover Depan**: Desain visual kontras tinggi (High Contrast Vision) dengan lapisan cetak timbul (Embossed Braille overlay) dan Audio QR Bridge pada cover belakang.

---

## Fitur Integrasi Generator Gambar (FAL.ai)

Jalankan skrip pembantu Python untuk langsung menghasilkan gambar draf cover fiksi via FAL.ai:
```bash
python helpers/python/fal_image_generator.py \
  --prompt "cinematic novel cover art, epic fantasy castle under glowing moonlight, dark blue and amber gold tones, highly detailed, 8k" \
  --output assets/novel_cover_draft.png \
  --aspect-ratio "3:4"
```

---

## Aturan Preflight Cetak (Print Proof Guidelines)
1. **Bleed Area**: Tambahkan $3\text{ mm}$ ($0.125\text{ in}$) di setiap sisi luar trim size.
2. **Safe Margin**: Pastikan semua teks (Judul, Penulis, Blurb, Barcode) berjarak minimal $5\text{ mm}$ dari garis potong (*trim line*).
3. **Format Warna**: CMYK untuk cetak proof fisik; RGB untuk Web Reader & e-Book digital.
4. **Barcode/ISBN**: Sediakan kotak putih berukuran minimal $3\text{ cm} \times 2\text{ cm}$ di pojok kanan bawah cover belakang.
