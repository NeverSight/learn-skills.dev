---
name: market-data-collector
description: Pengunduh dan penyedia data pasar multi-market mandiri. Mengambil harga historis OHLCV, data intraday, dan orderbook untuk Saham Indonesia (IDX), Crypto (CCXT), Valuta Asing (Forex), dan Komoditas.
---

# Market Data Collector Skill

## Ringkasan Peran
Bertugas sebagai jembatan data finansial tanpa biaya (free-first) yang secara otonom mencari, mengunduh, dan membersihkan data harga historis maupun real-time untuk dianalisis oleh modul teknikal dan model AI time-series.

## Sumber Data yang Didukung
- **Saham IDX (Indonesia):** Pengambilan data emiten IHSG via Yahoo Finance API (`.JK` suffix, misal: `BBCA.JK`, `ANTM.JK`, `BBRI.JK`, `ADRO.JK`) serta scraper data keterbukaan informasi.
- **Crypto:** Integrasi pustaka CCXT yang mencakup Binance, Bybit, Indodax, dan OKX untuk spot & futures.
- **Forex & Komoditas:** Pasangan mata uang mayor (EUR/USD, USD/JPY, GBP/USD, USD/IDR) dan komoditas global (Gold XAU/USD, WTI Crude Oil, Silver, Natural Gas).

## Output Standar
Mengembalikan dataframe bertipe terstandarisasi: `Date/Time`, `Open`, `High`, `Low`, `Close`, `Volume` dengan format numerik yang siap dikonsumsi oleh `timesfm-forecaster` dan `technical-analyst`.
