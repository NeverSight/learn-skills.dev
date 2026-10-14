---
name: economic-news-trader
description: Memantau kalender ekonomi berdampak tinggi (NFP, CPI AS, FOMC Rate, BI-Rate). Menerapkan strategi Pre-News Shield, kalkulasi deviasi surprise Actual vs Forecast, dan pelindung anti-slippage dari pelebaran spread broker.
---

# Economic News & NFP Trader Skill

## Ringkasan Peran
Mengelola risiko dan peluang dari rilis berita makroekonomi berdampak tinggi (*Red Folder / Bintang Tiga*). Menghindari bahaya spekulasi tebak angka sebelum rilis, dan fokus pada eksekusi berbasis deviasi matematis serta perlindungan posisi aktif.

## Tiga Mode Taktis
1. **Pre-News Shield:**
   - Mendeteksi agenda berita 30 menit sebelum jadwal rilis.
   - Mengirim peringatan untuk memperketat trailing stop atau mengamankan posisi swing ke titik impas (Breakeven) guna menghindari stop-hunting akibat lonjakan spread.
2. **Post-Release Momentum Scalping:**
   - Menghitung deviasi $\Delta = \text{Actual} - \text{Forecast}$ dalam 10 detik pasca-rilis.
   - Mengambil posisi searah kejutan fundamental hanya jika orderbook menunjukkan aliran volume konfirmatif.
3. **Anti-Slippage & Spread Widening Guard:**
   - Memeriksa selisih bid-ask terkini sebelum mengirim order.
   - Bila spread melebar melampaui toleransi maksimum (misal > 5 pips pada XAU atau valas), order otomatis diblokir demi melindungi modal pengguna.
