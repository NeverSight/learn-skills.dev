---
name: paper-trading-engine
description: Simulator portofolio trading offline mandiri berbasis SQLite lokal. Memodelkan komisi fee dan slippage likuiditas realistis, memantau trailing stop otomatis, dan mengekspor jurnal trading terformat profesional ke Excel (.xlsx).
---

# Paper Trading Engine Skill

## Ringkasan Peran
Menyediakan lingkungan pengujian bebas risiko modal (*forward testing sandbox*) yang mencerminkan kondisi bursa sesungguhnya. Memastikan pengguna dapat memvalidasi strategi trading tanpa mempertaruhkan uang riil.

## Kemampuan Kunci
1. **Model Slippage & Fee Nyata:**
   - Menghitung fee beli (~0.15%) dan jual (~0.25% termasuk PPh final) untuk Saham IDX.
   - Menghitung maker/taker fees untuk Crypto dan spread pips untuk Forex.
   - Memperhitungkan antrean volume bid/ask sehingga order berukuran besar tidak langsung terisi secara magis di harga terbaik.
2. **Database Lokal (Zero-Cloud Leak):**
   - Riwayat posisi terbuka, log transaksi, dan saldo tersimpan rapi di SQLite lokal (`data/trading_platform.db`).
3. **Ekspor Jurnal Excel (.xlsx) Otomatis:**
   - Membuat file spreadsheet Excel profesional berisikan Sheet KPI Portofolio (Win Rate, Sharpe, Max Drawdown), Sheet Posisi Terbuka, Sheet Log Transaksi, dan grafik Kurva Ekuitas (*Equity Curve*).
