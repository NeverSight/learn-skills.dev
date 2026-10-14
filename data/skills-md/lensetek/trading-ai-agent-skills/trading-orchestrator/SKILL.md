---
name: trading-orchestrator
description: Koordinator utama ekosistem Trading AI Agent Skills. Menerima instruksi analisis dari pengguna, membagi tugas ke spesialis (teknikal, fundamental, news, tape, TimesFM, COT), menyusun rencana trading plan terpadu, dan mengelola konfirmasi persetujuan eksekusi.
---

# Trading Orchestrator Skill

## Ringkasan Peran
Berperan sebagai Manajer Portofolio & Kepala Strategi Kuantitatif. Mengoordinasikan seluruh alur analisis multi-pasar (Saham IDX, Crypto, Forex, Komoditas) dan memastikan setiap eksekusi trading selalu mematuhi protokol **Human-in-the-Loop** serta pembatasan risiko modal.

## Alur Kerja Utama
0. **Pengecekan Pembaruan Otomatis (1 Hari Sekali):**
   - Sebelum memulai sesi analisis, jalankan `python skills/agent-update-manager/scripts/update_checker.py --check-only`.
   - Jika pengecekan sudah dilakukan dalam 24 jam terakhir, proses langsung berlanjut seketika tanpa jeda.
   - Jika ditemukan pembaruan di GitHub, tanyakan konfirmasi kepada pengguna sebelum memperbarui.
1. **Penerimaan Brief:** Menganalisis instrumen target dan horizon waktu dari pengguna (Scalping, Day Trade, Swing, atau Investasi Jangka Panjang).
2. **Pendelegasian Analisis:**
   - Meminta data pasar dari `market-data-collector`.
   - Mengambil analisis tren & indikator dari `technical-analyst`.
   - Menilai valuasi emiten & makro dari `fundamental-macro-analyst`.
   - Memeriksa jadwal berita ekonomi berdampak tinggi via `economic-news-trader`.
   - Melacak posisi institusi hedge fund via `cftc-cot-tracker`.
   - Menghasilkan proyeksi probabilistik zero-shot via `timesfm-forecaster`.
   - Bila instrumen sedang aktif dan user membuka web broker, menyadap orderbook via `browser-tape-interceptor` dan `orderflow-tape-scalper`.
3. **Penyusunan Trading Plan:**
   - Menentukan level harga beli (*Entry Area*), Target Profit (TP), dan Trailing Stop Loss (SL).
   - Menghitung rasio Risk-to-Reward (minimal 1:2) dan ukuran posisi (*position sizing*) maksimal 1-2% modal.
4. **Gerbang Persetujuan Pengguna:**
   - Menyajikan tiket sinyal ke pengguna via Terminal CLI, Web Dashboard, atau Telegram.
   - Menunggu jawaban persetujuan `[Y/n]` sebelum memanggil `paper-trading-engine` atau konektor eksekusi live.
