---
name: cftc-cot-tracker
description: Mengunduh dan menganalisis laporan mingguan resmi CFTC Commitment of Traders (COT). Melacak posisi bersih institusi hedge fund dan produser komoditas global, menghitung COT Index Oscillator, dan memetakan dampaknya ke saham emiten Indonesia (IDX).
---

# CFTC COT Institutional Tracker Skill

## Ringkasan Peran
Menyediakan intelijen institusional level makro berdasarkan laporan wajib mingguan U.S. Commodity Futures Trading Commission (CFTC). Membuka posisi riil dana miliaran dollar yang dipegang oleh *Commercials* (Smart Money) dan *Non-Commercials / Managed Money* (Hedge Funds).

## Metrik & Analisis
1. **COT Index Oscillator (0 - 100%):**
   - Menghitung normalisasi posisi bersih institusi dalam jendela waktu 1 hingga 3 tahun:
     $$\text{COT Index} = \frac{\text{Net Pos Terkini} - \text{Net Min}_{(N)}}{\text{Net Max}_{(N)} - \text{Net Min}_{(N)}} \times 100\%$$
   - Nilai > 90%: Peringatan rawan pembalikan arah (*overbought extreme*).
   - Nilai < 10%: Potensi pembalikan arah naik (*short squeeze / market bottoming*).
2. **Korelasi Komoditas ke Saham Emiten IDX:**
   - **Gold Futures (COMEX)** $\rightarrow$ Memvalidasi momentum saham tambang emas: `ANTM`, `MDKA`, `PSAB`, `ARCI`.
   - **Crude Oil (NYMEX)** $\rightarrow$ Memprediksi pendapatan emiten migas: `MEDC`, `ENRG`, `PGAS`.
   - **Copper & Metals** $\rightarrow$ Emiten nikel & timah: `TINS`, `INCO`, `HRUM`.
   - **US Dollar Index (DXY)** $\rightarrow$ Proyeksi arus dana asing (*foreign flow*) ke perbankan `BBCA`, `BBRI`, `BMRI`.
