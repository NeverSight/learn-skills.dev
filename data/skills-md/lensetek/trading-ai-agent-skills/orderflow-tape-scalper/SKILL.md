---
name: orderflow-tape-scalper
description: Algoritma tape reading dan analisis mikrostruktur order flow. Mendeteksi agresi volume Hajar Kanan (Haka), Hajar Kiri (Haki), akumulasi/distribusi senyap (Iceberg Orders), manipulasi Fake Bid/Ask, dan Broker Summary (Bandarmologi).
---

# Orderflow & Tape Scalper Skill

## Ringkasan Peran
Spesialis mikrostruktur transaksi jangka pendek (scalping dan tape reading). Menerima aliran data live dari `browser-tape-interceptor` dan menghitung metrik ketidakseimbangan order (*orderbook imbalance*) secara matematis.

## Fitur Deteksi
1. **Haka / Haki Aggressor Sweeps:**
   - Menghitung rasio volume beli agresif di sisi Offer/Ask (*Haka*) vs volume jual agresif di sisi Bid (*Haki*).
   - Memunculkan sinyal momentum saat lonjakan volume melebihi 3x rata-rata moving volume 5 menit terakhir.
2. **Iceberg Order Detection:**
   - Mendeteksi transaksi berulang di satu titik harga yang menyerap lot raksasa tanpa menggeser harga turun (*absorption*).
3. **Bandarmologi & Broker Summary (Khusus Saham IDX):**
   - Menganalisis konsentrasi transaksi broker institusi/asing (misal: kode broker ZP, CS, BK, RX, AK) untuk mengidentifikasi apakah saham sedang diakumulasi bandar atau didistribusikan ke ritel.
