---
name: skripsi-filkom-ub
description: Membuat, mengedit, meneliti, mengaudit, dan merender skripsi atau proposal FILKOM UB berbahasa Indonesia dalam LaTeX dengan jejak bukti sumber dan pemeriksaan kepatuhan.
metadata:
  short-description: Skripsi FILKOM UB yang dapat diaudit
---

# Skripsi FILKOM UB

Gunakan skill ini untuk tugas skripsi/proposal/makalah turunan di Fakultas Ilmu Komputer Universitas Brawijaya (FILKOM UB), terutama bila luaran harus berbahasa Indonesia dan LaTeX. Hasilnya harus dapat ditelusuri: jangan menciptakan data, hasil eksperimen, sitasi, identitas, tanda tangan, persetujuan, atau status administratif.

## Batas otoritas dan sumber

`skripsi-filkom.md` adalah ekstraksi **Panduan Skripsi FILKOM UB v3.0 (2018)**. Perlakukan sebagai sumber normatif untuk aturan yang tertulis di dalamnya, tetapi jangan mengklaimnya sebagai aturan akademik terkini tanpa memeriksa kanal resmi FILKOM/UB. `puebi.md` adalah PUEBI edisi 2016. Untuk aturan ejaan atau administrasi yang berubah, cari dan catat sumber primer terkini.

Sebelum menghasilkan atau mengaudit dokumen, baca [source-authority.md](references/source-authority.md). Kemudian pilih jalur kerja:

| Permintaan | Baca dan lakukan |
| --- | --- |
| Merencanakan topik/proposal | [research-and-evidence.md](references/research-and-evidence.md), [filkom-requirements.md](references/filkom-requirements.md) |
| Menulis/revisi Bahasa Indonesia | [writing-and-puebi.md](references/writing-and-puebi.md) |
| Membuat/edit/render LaTeX | [latex-workflow.md](references/latex-workflow.md) dan template bila diminta |
| Audit naskah/siap semhas/ujian | [audit-protocol.md](references/audit-protocol.md) |
| Menilai kecukupan bidang | [filkom-requirements.md](references/filkom-requirements.md), [official-guide-index.md](references/official-guide-index.md), lalu buka bagian bidang yang relevan dari panduan lokal |

Jika dokumen belum menyediakan informasi yang menentukan (program studi, bidang, tipe/pendekatan penelitian, status proposal/akhir, template resmi, atau mesin LaTeX), inspeksi berkas yang ada dahulu dan tanyakan hanya informasi yang tidak bisa diperoleh dengan aman.

## Prinsip nonhalusinasi

1. Pisahkan secara eksplisit **fakta bersumber**, **data/hasil pengguna**, **rencana**, dan **inferensi**. Inferensi harus menyebutkan dasar dan keterbatasannya.
2. Untuk setiap klaim substantif, angka, definisi, metodologi, atau gambar pihak lain, buat entri di `research/claim-ledger.tsv`; jangan menulisnya sebagai fakta bila buktinya belum ada.
3. Ambil metadata bibliografi dari DOI, laman penerbit, Crossref/DataCite, atau sumber primer. Jangan mengisi DOI, halaman, tahun, penerbit, penulis, URL, maupun hasil yang tidak terverifikasi.
4. Parafrase setelah memahami sumber, sitasi dekat dengan klaim, dan gunakan kutipan langsung seperlunya dengan halaman/lokasi yang dapat diperiksa. Sitasi tidak membuat salinan tekstual berlebihan menjadi boleh.
5. Jangan membuat halaman pengesahan, tanda tangan, nilai, berita acara, sertifikat, atau pernyataan orisinalitas seolah-olah sudah benar/ditandatangani. Sediakan draf berlabel jelas dan minta pengguna mengganti fakta serta memperoleh persetujuan resmi.
6. Kompilasi tidak membuktikan kebenaran akademik; audit otomatis tidak membuktikan kepatuhan penuh. Nyatakan apa yang benar-benar diuji.

## Alur kerja inti

1. **Intake.** Identifikasi deliverable, status, bidang, tipe penelitian, pembimbing/template, batasan, dan berkas yang sudah ada. Pertahankan template institusi apa adanya bila tersedia.
2. **Matriks kepatuhan.** Buat daftar persyaratan dengan asal, status (`terbukti`, `belum terbukti`, `tidak berlaku`, atau `perlu verifikasi terkini`), bukti/berkas, dan tindakan.
3. **Riset.** Susun pertanyaan pencarian, pakai sumber primer/terbitan bereputasi, verifikasi metadata, dan catat klaim. Jangan menyamakan relevansi dengan bukti kausal.
4. **Struktur dan penulisan.** Selaraskan masalah → tujuan/pertanyaan → metode → data → hasil → pembahasan → kesimpulan. Untuk skripsi akhir gunakan struktur yang cocok dengan pendekatan, bukan bab seragam yang kosong. Proposal memuat Bab 1--3 dan jadwal penelitian.
5. **LaTeX.** Pertahankan kelas/mesin/back-end bibliography dari template. Bila belum ada template resmi, gunakan `assets/latex-skeleton` sebagai titik awal, LuaLaTeX/XeLaTeX untuk Calibri, dan beri status *draf* sampai halaman institusional diverifikasi.
6. **Validasi.** Jalankan pemeriksaan statis, verifikasi referensi, build multi-pass, baca log, dan periksa PDF secara visual. Perbaiki akar masalah lalu ulangi.
7. **Laporan.** Berikan perubahan, perintah build yang dijalankan, hasil aktual, temuan berprioritas, dan item yang tetap memerlukan verifikasi manusia/FILKOM.

## Ketentuan FILKOM v3.0 yang harus diperlakukan sebagai baseline

Gunakan [filkom-requirements.md](references/filkom-requirements.md) sebagai indeks operasional, bukan pengganti panduan asli. Baseline yang sering relevan mencakup: Bahasa Indonesia baku; daftar referensi gaya nama--tahun adaptasi Harvard-Anglia; bagian awal/utama/akhir; halaman awal Romawi kecil dan bagian utama Arab di tengah bawah; A4 satu sisi; margin kiri 4 cm serta atas/kanan/bawah 3 cm; Calibri dengan badan 12 pt; spasi tunggal; tabel di atas dan gambar di bawah, keduanya bernomor per bab serta dirujuk di teks.

Aturan bidang dan prosedur administrasi sangat spesifik serta dapat berubah. Jangan menggeneralisasi indikator RPL ke KBJ, SI, atau bidang lain. Jangan menyimpulkan kelayakan/kelulusan hanya dari pemeriksaan ini.

## Operasi LaTeX

Untuk proyek baru yang tidak diberi template, salin kerangka aset, lalu edit metadata dan bab. Untuk proyek yang ada, jangan mengganti kelas, margin, font, gaya sitasi, atau mesin hanya karena preferensi.

```bash
cp -R assets/latex-skeleton ./skripsi
cd skripsi
latexmk -lualatex -interaction=nonstopmode -file-line-error main.tex
python3 ../../scripts/audit_skripsi.py .
python3 ../../scripts/verify_sources.py research/references.json
```

`latexmk` dapat dipanggil dengan `-xelatex` bila Calibri hanya tersedia pada XeLaTeX. Jika font atau compiler tidak tersedia, jangan menyatakan PDF berhasil dibuat; laporkan prasyarat yang hilang. Jangan aktifkan `--shell-escape` kecuali pengguna mengetahui alasan dan sumber TeX tepercaya.

## Pemeriksaan wajib sebelum menyerahkan

- Semua sitasi memiliki entri referensi dan metadata yang dapat diverifikasi.
- Semua klaim hasil berasal dari data/analisis pengguna yang dapat ditelusuri.
- Rumusan masalah, tujuan, metode, hasil, dan kesimpulan saling menjawab.
- Gambar/tabel/persamaan diberi label, dirujuk dari teks, dan sumbernya dicatat bila bukan karya sendiri.
- Bahasa, kapitalisasi, kata depan, istilah asing, singkatan, angka, dan tanda baca telah ditinjau menurut PUEBI/KBBI.
- Tidak ada data mentah, kode berlebihan, atau detail yang seharusnya menjadi lampiran di badan utama tanpa alasan.
- Log build bebas dari error serta referensi/sitasi tak terdefinisi; PDF diperiksa untuk margin, nomor halaman, float, overflow, dan placeholder.
- Ketentuan administratif terkini, template, tanda tangan, dan tenggat telah dikonfirmasi pada kanal resmi.
