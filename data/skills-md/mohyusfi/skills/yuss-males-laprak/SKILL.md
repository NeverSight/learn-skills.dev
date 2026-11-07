---
name: yuss-males-laprak
description: Buat dan format laporan praktikum akademik ke format Microsoft Word (.docx) dengan margin 4-4-3-3 cm, Times New Roman 12 pt, 1.5 spasi, heading MS Office native (terintegrasi Navigation Pane), aturan cetak miring istilah non-KBBI, sitasi APA 7th edition, pembersihan foto modul asdos menjadi placeholder gambar, hierarki list angka (1. 2. 3.) lalu huruf (a. b. c.) dengan text indent 0.75 cm, page break mutlak per bab tanpa menggabungkan bab di halaman yang sama (halaman sampul tersendiri, Bab II di halaman baru), teks Bab II & Bab III verbatim sesuai modul asdos tanpa perubahan kalimat kecuali ekspansi halaman penuh + sitasi pada Bab II jika belum full, serta kesimpulan kumulatif otomatis.
---

# Yuss Males Laprak Skill

Skill ini memandu agen untuk membuat dan menyusun laporan praktikum mahasiswa ke dalam format dokumen Microsoft Word (`.docx`) siap kumpul dengan standar tata tulis akademik perguruan tinggi yang presisi.

---

## 1. Aturan Wajib & Validasi Input Awal

### [PENTING] Meminta Modul Asdos
> **Aturan Wajib**: Jika pengguna meminta pembuatan laporan praktikum tetapi **belum melampirkan modul atau teks materi dari asdos** (baik berupa file PDF, docx, maupun teks perintah praktikum), agen **WAJIB LANGSUNG MEMINTA** modul dari asdos terlebih dahulu kepada pengguna sebelum melakukan proses pembuatan laporan.

Contoh pesan jika modul belum disertakan:
> *"Mohon sertakan atau beritahukan lokasi file modul dari asdos (PDF/Word/teks materi praktikum) terlebih dahulu agar Bab II Landasan Teori dan Bab III Langkah Kerja dapat disalin dan disusun sesuai standar praktikum."*

---

## 2. Profil & Konfigurasi Standar Mahasiswa

Secara default, identitas mahasiswa yang digunakan adalah:
- **Nama**: `MOH. YUSFI LAKHAFIDUN`
- **NIM**: `F5512520089`
- **Kelas**: `Informatika C` (atau `TI C`)

*(Identitas ini dapat disesuaikan jika pengguna secara eksplisit meminta identitas lain).*

---

## 3. Standar Format Dokumen Word (.docx)

Dokumen output harus memenuhi standar tata tulis akademik resmi:
1. **Ukuran Kertas**: A4 (21,0 cm × 29,7 cm).
2. **Margin Halaman**:
   - Atas (*Top*): **4,0 cm**
   - Kiri (*Left*): **4,0 cm**
   - Bawah (*Bottom*): **3,0 cm**
   - Kanan (*Right*): **3,0 cm**
   *(Format Akademik 4-4-3-3)*.
3. **Tipografi & Spasi**:
   - Font: **Times New Roman**, 12 pt (seluruh teks dokumen), 11 pt (italic bold abu-abu `#646464` untuk placeholder gambar).
   - Spasi Baris: **1,5 spasi** (`line = 360`, `lineRule = auto`).
   - Warna Font: Hitam Pekat (`#000000`).
   - Perataan Paragraf: Rata Kiri-Kanan (*Justified*).
   - Indentasi Baris Pertama Paragraf: **1,27 cm** (*0,5 inci*).
4. **Hierarki & Format List Native MS Word (Numbering & Lettering)**:
   - **Implementasi Native Word (`<w:numPr>`)**:
     Seluruh penomoran daftar menggunakan elemen native OpenXML `<w:numPr>` agar di Microsoft Word toolbar ribbon penomoran otomatis **menyala** dan penomoran otomatis **berjalan (auto-continue)** saat menekan Enter.
   - **Urutan Hierarki Penomoran**:
     - **Level 1**: Angka Arab (`1.`, `2.`, `3.`, dst.)
     - **Level 2**: Huruf kecil (`a.`, `b.`, `c.`, dst.)
     - **Level 3**: Angka kurung tutup (`1)`, `2)`, `3)`, dst.)
   - **Text Indent**: **0,75 cm** (*hanging indent*).
     - Jarak penjorokan dari simbol nomor/huruf ke permulaan teks isi adalah **0,75 cm**.
     - Baris kedua dan seterusnya lurus sejajar dengan awal baris pertama teks isi.
   - **Pola Penjajaran (Alignment) List, Gambar, & Paragraf Penjelasan**:
     Berdasarkan struktur materi dari asdos, gunakan pola berikut:
     - **Pola 1 (List Langsung Setelah Sub-Judul - Standar Utama Bab III & IV)**:
       Jika daftar list langsung menyusul setelah sub-judul (Heading 3):
       - Nomor list (`1.`, `2.`, dst.) berada pada posisi **2,54 cm** (sejajar lurus dengan huruf pertama judul sub-bab di tab stop 2,54 cm).
       - Teks permulaan isi list berada pada posisi **3,29 cm** (2,54 cm + hanging 0,75 cm).
       - **Placeholder Gambar**: Wajib diletakkan lurus **sejajar dengan huruf pertama teks isi list** (posisi **3,29 cm**, perataan kiri *left-aligned*, bukan tengah *center*).
       - **Paragraf Penjelasan Teknis**: Paragraf pembahasan teknis di bawah gambar wajib diletakkan lurus **sejajar dengan huruf pertama teks isi list** (posisi **3,29 cm**, `first_line_indent = 0 cm`, perataan *Justified*), sehingga seluruh baris kalimat membungkus lurus rapi di batas 3,29 cm.
     - **Pola 2 (List Setelah Paragraf Pengantar)**:
       Jika terdapat paragraf pengantar naratif sebelum daftar poin list:
       - Paragraf pengantar: `left_indent = 1,27 cm`, `first_line_indent = 1,27 cm` (menjorok di 2,54 cm).
       - Nomor list (`1.`, `2.`, dst.) berada pada posisi **1,27 cm**.
       - Teks permulaan isi list berada pada posisi **2,02 cm** (1,27 cm + hanging 0,75 cm).
       - Placeholder gambar dan paragraf penjelasan: posisi **2,02 cm** (perataan kiri *left-aligned*).
5. **Hierarki Heading Native MS Word (Aturan Terusan Modul & Heading Bersyarat)**:
   - **Aturan Terusan Modul (Tanpa Heading 1 & Heading 2 pada Bab II, III, IV)**:
     Jika dokumen referensi/modul merupakan format terusan mingguan yang **tidak mencantumkan Heading 1 (`BAB II`, `BAB III`, `BAB IV`) dan Heading 2 (`2.1`, `3.1`, `4.1`)**:
     - **JANGAN BUAT** Heading 1 dan Heading 2 pada Bab II, Bab III, dan Bab IV.
     - Mulai bab tersebut **LANGSUNG DENGAN HEADING 3** (`\tx.1.N\t<Judul Modul>`).
     - **PENTING**: Heading 3 wajib diawali karakter tab (`\t`) dengan tab stop di 1,27 cm dan 2,54 cm, sehingga nomor `x.1.N` berada pada posisi **1,27 cm** (seakan-akan terusan dari modul sebelumnya di bawah parent), **JANGAN membuat Heading 3 rata kiri di margin 0 cm sejajar Heading 2**.
     - Khusus untuk **Bab V (Penutup)** dan **DAFTAR PUSTAKA**, Heading 1 (`BAB V \nPENUTUP`, `DAFTAR PUSTAKA`) dan Heading 2 (`5.1\tKesimpulan`) **TETAP WAJIB DIBUAT LENGKAP**.
   - **Daftar Heading Lengkap (Jika Modul Memiliki Parent Heading)**:
     - `Heading 1` (Center, Bold, Outline Level 0):
       - `BAB II \nLANDASAN TEORI` (Halaman 2 Baru)
       - `BAB III \nLANGKAH KERJA` (Halaman Baru)
       - `BAB IV \nHASIL DAN PEMBAHASAN` (Halaman Baru)
       - `BAB V \nPENUTUP` (Halaman Baru)
       - `DAFTAR PUSTAKA` (Halaman Baru)
     - `Heading 2` (Left, Bold, Outline Level 1, Tab Stop 1,27 cm):
       - `2.1\tLandasan Teori` (Bab II)
       - `3.1\tLangkah Kerja` (Bab III)
       - `4.1\tHasil dan Pembahasan` (Bab IV)
       - `5.1\tKesimpulan` (Bab V)
     - `Heading 3` (Left, Bold, Outline Level 2, Tab Stops 1,27 cm dan 2,54 cm):
       - `\t2.1.<NoModul>\t<Judul Modul>` (Bab II, diawali tab sehingga nomor `2.1.N` berada di 1,27 cm)
       - `\t3.1.<NoModul>\t<Judul Modul>` (Bab III, diawali tab sehingga nomor `3.1.N` berada di 1,27 cm)
       - `\t4.1.<NoModul>\t<Judul Modul>` (Bab IV, diawali tab sehingga nomor `4.1.N` berada di 1,27 cm)
       - `\t5.1.1` s.d. `\t5.1.N` (Bab V, diawali tab sehingga nomor `5.1.N` berada di 1,27 cm)
   *Hierarki ini menjamin Navigation Pane di Microsoft Office Word langsung menampilkan daftar isi otomatis berjenjang dengan presisi.*

---

## 4. Aturan Pemisahan Halaman Mutlak & Integritas Teks Modul

### [PENTING] Aturan Pemisahan Halaman Mutlak (*Page Break*)
> **Aturan Mutlak**: **TIAP BAB TIDAK BOLEH BERTEMU DI 1 HALAMAN YANG SAMA!**
> 1. **Halaman Sampul / Identitas**: Berdiri sendiri pada **Halaman 1**.
> 2. **Bab II (Landasan Teori)**: **WAJIB DIMULAI DI HALAMAN BARU (Halaman 2)** melalui *Page Break*. Jangan langsung digabung di halaman sampul!
> 3. **Bab III (Langkah Kerja)**: **WAJIB DI HALAMAN BARU** (*Page Break*).
> 4. **Bab IV (Hasil dan Pembahasan)**: **WAJIB DI HALAMAN BARU** (*Page Break*).
> 5. **Bab V (Penutup)**: **WAJIB DI HALAMAN BARU** (*Page Break*).
> 6. **DAFTAR PUSTAKA**: **WAJIB DI HALAMAN BARU** (*Page Break*).

### [PENTING] Aturan Integritas Teks Modul Asdos & Prinsip Full-Page Bab II
> **Aturan Mutlak**:
> 1. **Bab II (Landasan Teori - Teks Asdos Verbatim & Full-Page Rule)**:
>    - Teks materi yang diberikan asdos **JANGAN DIRUBAH KALIMATNYA**. Salin persis sesuai modul asdos.
>    - **Prinsip Halaman Penuh Mutlak (*Full-Page Rule*)**:
>      Bab II tidak harus dibatasi 1 halaman jika materinya banyak, tetapi **SETIAP HALAMAN YANG DITEMPATI BAB II WAJIB TERISI PENUH (FULL)**. Dilarang keras ada halaman terakhir Bab II yang "nanggung", menyisakan banyak ruang kosong, atau hanya terisi beberapa kalimat/setengah halaman sebelum *Page Break*.
>      - **Jika materi meluap sedikit (tumpah 1–6 baris nanggung ke halaman berikutnya)**: Wajib memotong / memparafrase kalimat pengayaan penutup agar pas dan padat di halaman sebelumnya (jangan membuat halaman baru hanya untuk sedikit kalimat).
>      - **Jika materi memang membutuhkan halaman baru**: Halaman baru tersebut **wajib diekspansi secara komprehensif** dengan materi teknis pendalaman hingga **terisi penuh 1 halaman utuh**, tidak boleh dibiarkan setengah kosong.
>    - **Aturan Sitasi Ilmiah Tambahan (Wajib Open-Access Free $\ge$ 2020)**:
>      - Teks materi pengayaan **WAJIB menyertakan sitasi ilmiah format APA 7th Edition**.
>      - **DILARANG MENGGUNAKAN BUKU BERBAYAR (*paid books*)** karena tidak dapat diakses bebas.
>      - **Wajib menggunakan artikel Jurnal Ilmiah Akses Terbuka (*Open-Access / Free*)** dengan tahun terbit **$\ge 2020$**.
>      - Sumber wajib divalidasi ketersediaannya melalui pencarian web (*web search*) dan memiliki DOI atau tautan repositori jurnal aktif.
>      - Format di teks: `(Penulis, Tahun)` dan wajib sinkron dengan entri di Daftar Pustaka.
> 2. **Bab III (Langkah Kerja)**: **JANGAN ADA PERUBAHAN KALIMAT LANGKAH KERJANYA**, biarkan kalimatnya persis sesuai modul asdos. Di bawah langkah yang membutuhkan dokumentasi, sematkan placeholder `[Sisipkan Gambar: <Deskripsi>]` yang **sejajar dengan huruf pertama teks langkah**. Semua foto/tangkapan layar asdos dihapus.

---

### Rincian Sistematika Bab:

### A. Halaman Sampul (Halaman 1 Khusus)
Terletak di halaman pertama secara mandiri, disusul **Page Break**:
```text
MODUL PRAKTIKUM <NO_MODUL_ROMAWI>
(<JUDUL MODUL PRAKTIKUM>)
Nama : MOH. YUSFI LAKHAFIDUN
NIM : F5512520089
Kelas : Informatika C
```

### B. Bab II (Landasan Teori - Halaman 2 Baru)
1. **Dimulai di Halaman Baru**: Setelah Halaman Sampul, disisipkan Page Break.
2. **Heading Terstruktur**:
   - Jika modul mandiri (ada parent heading): Heading 1 `BAB II \nLANDASAN TEORI`, Heading 2 `2.1\tLandasan Teori`, Heading 3 `\t2.1.<NoModul>\t<Judul Modul>`.
   - Jika modul terusan (tidak ada parent heading pada referensi): **Langsung mulai dengan Heading 3** `\t2.1.<NoModul>\t<Judul Modul>` (diawali tab, nomor berada pada posisi 1,27 cm, judul di 2,54 cm).
3. **Teks Asdos Verbatim**: Materi asli modul asdos disalin utuh tanpa mengubah kalimat aslinya.
4. **Format List**: Menggunakan Pola 1 (nomor di 2,54 cm, teks di 3,29 cm) jika langsung di bawah sub-judul, atau Pola 2 jika diawali paragraf pengantar. Sub-poin menggunakan huruf (`a.`, `b.`, `c.`), text indent 0,75 cm.
5. **Ekspansi Halaman Penuh + Sitasi Open-Access (Free $\ge$ 2020)**:
   - Pastikan halaman Bab II terisi penuh (*full-page*). Jika materi asdos menyisakan ruang di halaman, tambahkan kalimat pengayaan yang dipas-kan panjangnya agar halaman terisi penuh tanpa meluap nanggung ke halaman berikutnya.
   - Wajib menyertakan sitasi ilmiah open-access gratis $\ge 2020$ (terverifikasi web search).
6. **Page Break**: Di akhir Bab II disisipkan Page Break sebelum masuk ke Bab III.

### C. Bab III (Langkah Kerja - Halaman Baru)
1. **Dimulai di Halaman Baru**: Disisipkan Page Break.
2. **Heading Terstruktur**:
   - Jika modul mandiri: Heading 1 `BAB III \nLANGKAH KERJA`, Heading 2 `3.1\tLangkah Kerja`, Heading 3 `\t3.1.<NoModul>\t<Judul Modul>`.
   - Jika modul terusan: **Langsung mulai dengan Heading 3** `\t3.1.<NoModul>\t<Judul Modul>` (diawali tab, nomor berada pada posisi 1,27 cm, judul di 2,54 cm).
3. **Kalimat Langkah Kerja Sesuai Modul**: Seluruh butir langkah kerja disalin persis sesuai kalimat modul asdos tanpa diubah.
4. **Penomoran List (Pola 1 Standar)**: Menggunakan angka (`1.`, `2.`, `3.`, dst.) di posisi **2,54 cm** dengan teks langkah di posisi **3,29 cm** (hanging 0,75 cm).
5. **Placeholder Gambar**: Di bawah langkah disematkan `[Sisipkan Gambar: <Deskripsi>]` rata kiri sejajar huruf pertama isi langkah kerja (posisi **3,29 cm**).
6. **Page Break**: Di akhir Bab III disisipkan Page Break sebelum masuk ke Bab IV.

### D. Bab IV (Hasil dan Pembahasan - Halaman Baru)
1. **Dimulai di Halaman Baru**: Disisipkan Page Break.
2. **Heading Terstruktur**:
   - Jika modul mandiri: Heading 1 `BAB IV \nHASIL DAN PEMBAHASAN`, Heading 2 `4.1\tHasil dan Pembahasan`, Heading 3 `\t4.1.<NoModul>\t<Judul Modul>`.
   - Jika modul terusan: **Langsung mulai dengan Heading 3** `\t4.1.<NoModul>\t<Judul Modul>` (diawali tab, nomor berada pada posisi 1,27 cm, judul di 2,54 cm).
3. **Penomoran Sub-Hasil (Pola 1 Standar)**: Menggunakan angka (`1.`, `2.`, `3.`, dst.) di posisi **2,54 cm** dengan teks judul sub-hasil di posisi **3,29 cm** (hanging 0,75 cm).
4. **Placeholder Gambar**: Sematkan penanda `[Sisipkan Gambar: <Deskripsi Luaran>]` rata kiri sejajar huruf pertama judul sub-hasil (posisi **3,29 cm**).
5. **Pembahasan Komprehensif**: Pembahasan analisis teknis mendalam mengenai hasil uji coba diletakkan sejajar huruf pertama judul sub-hasil (posisi **3,29 cm**, `first_line_indent = 0`, Justified).
6. **Page Break**: Di akhir Bab IV disisipkan Page Break sebelum masuk ke Bab V.

### E. Bab V (Penutup - Halaman Baru)
1. **Dimulai di Halaman Baru**: Disisipkan Page Break.
2. **Heading Terstruktur**: Heading 1 `BAB V \nPENUTUP`, Heading 2 `5.1\tKesimpulan`.
3. **Kesimpulan Kumulatif**: Rangkuman kesimpulan dari Modul 1 hingga modul berjalan (`\t5.1.1` s.d. `\t5.1.N`).
4. **Pemindaian Otomatis**: Generator memindai kesimpulan sebelumnya dari berkas `.docx` terdahulu di folder praktikum.
5. **Penjajaran Sub-kesimpulan & Paragraf**:
   - Nomor sub-kesimpulan `5.1.N` diawali tab (`\t5.1.N\t<Judul>`) sehingga nomor `5.1.N` **lurus sejajar dengan huruf K pada parent sub-judul `5.1\tKesimpulan`** (posisi 1,27 cm).
   - Judul sub-kesimpulan berada di posisi tab berikutnya (posisi 2,54 cm).
   - **Paragraf Isi Kesimpulan**: Kata pertama pada baris pertama **lurus sejajar dengan huruf pertama judul sub-kesimpulan** (posisi 2,54 cm), dan **baris kalimat selanjutnya membungkus lurus sejajar dengan angka 5** (posisi 1,27 cm).
6. **Page Break**: Di akhir Bab V disisipkan Page Break sebelum masuk ke Daftar Pustaka.

### F. Daftar Pustaka (Halaman Baru)
1. **Dimulai di Halaman Baru**: Disisipkan Page Break dengan heading `DAFTAR PUSTAKA`.
2. **Format APA 7th Edition**: Hanging indent 1,27 cm, spasi 1,5, urut abjad.
3. Memuat semua sumber yang disitasi pada Bab II.

---

## 5. Aturan Bahasa & Cetak Miring (Non-KBBI)

> **Aturan Mutlak**: Seluruh kata, istilah teknis, atau frasa yang **bukan bahasa Indonesia resmi (tidak ada dalam KBBI)** WAJIB dicetak miring (*italic*).

- Contoh istilah yang harus miring:
  *Shapes*, *Image*, *Color Scheme*, *Fill*, *Linear Gradient*, *Radial Gradient*, *Angular Gradient*, *Diamond Gradient*, *Solid*, *Frame*, *Canvas*, *Layers*, *Group*, *Design*, *Desktop*, *Mobile*, *Device*, dsb.
- Diterapkan pada **seluruh bab** (Bab II, Bab III, Bab IV, Bab V).

---

## 6. Prosedur Pengeksekusian (Execution Workflow)

Saat membuat laporan baru:
1. **Periksa modul asdos**: Baca file modul PDF/Word asdos.
2. **Susun Konten**:
   - Halaman Sampul (Header Identitas).
   - Bab II: Teks asdos verbatim (jangan dirubah) + ekspansi sisa halaman hingga full page + sitasi APA 7th.
   - Bab III: Teks langkah kerja verbatim sesuai modul asdos (jangan dirubah kalimatnya) + placeholder gambar.
   - Bab IV: Luaran hasil + placeholder gambar + pembahasan teknis.
   - Bab V: Kesimpulan kumulatif (5.1.1 s.d. 5.1.N).
   - Daftar Pustaka: Format APA 7th Edition.
3. **Simpan Data Konten ke Berkas JSON**:
   Simpan ke scratch JSON (misal `<scratch>/report_data.json`).
4. **Jalankan Generator**:
   ```powershell
   uv run --with python-docx --with PySastrawi python "<skill_dir>/scripts/generate_report.py" --input "<scratch>/report_data.json" --output "<target_dir>/f5512520089_prak_<mata_kuliah>_<N>.docx" --scan-dir "<target_dir>"
   ```
   *(Catatan: `<skill_dir>` adalah path absolut atau relatif ke direktori root skill ini).*
5. **Verifikasi Output**: Pastikan setiap bab berada di halaman baru (Page Break mutlak) dan konfirmasikan hasilnya kepada pengguna.
