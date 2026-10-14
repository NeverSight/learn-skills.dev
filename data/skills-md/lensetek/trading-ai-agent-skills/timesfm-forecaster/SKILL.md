---
name: timesfm-forecaster
description: Menjalankan model AI Time Series Foundation Model dari Google Research (TimesFM) untuk memprediksi lintasan harga masa depan secara zero-shot probabilistik lengkap dengan rentang ketidakpastian matematis (Quantile P10, P50, P90).
---

# Google Research TimesFM Forecaster Skill

## Ringkasan Peran
Menyediakan lapisan proyeksi harga prediktif menggunakan model mutakhir Google Research TimesFM (berbasis Transformer decoder-only yang dilatih pada miliaran data deret waktu). Menggantikan tebakan subjektif dengan interval statistik matematis yang terukur.

## Kemampuan Kuantitatif
1. **Zero-Shot Forecasting:**
   - Menerima rentang 128 - 512 candle terakhir (OHLCV) dan memproyeksikan 16 - 32 horizon candle ke depan tanpa perlu pelatihan model ulang (*fine-tuning from scratch*).
2. **Dynamic Trailing Stop via Quantile P10:**
   - Menghitung estimasi batas bawah pesimis (*Quantile 10th percentile*).
   - Dijadikan patokan *Trailing Stop Loss Dinamis* yang bergerak naik mengikuti deviasi normalitas statistik.
3. **Target Profit Realistis via P50 & P90:**
   - Garis median (P50) berfungsi sebagai estimasi target harga paling rasional.
   - Garis optimis (P90) berfungsi sebagai target take-profit parsial untuk mengamankan keuntungan puncak.
4. **Hardware-Adaptive Inference:**
   - Berjalan pada akselerasi GPU NVIDIA (PyTorch CUDA) bila tersedia, atau otomatis fallback ke mode CPU hemat memori.
