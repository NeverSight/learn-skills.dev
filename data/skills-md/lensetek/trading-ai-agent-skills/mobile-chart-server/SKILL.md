---
name: mobile-chart-server
description: Server dashboard web mandiri berbasis FastAPI dan TradingView Lightweight Charts dengan desain responsif Mobile-View First. Menampilkan candlestick interaktif, overlay proyeksi TimesFM, dan tombol persetujuan tiket transaksi.
---

# Mobile Chart Server Skill

## Ringkasan Peran
Menyediakan antarmuka visual mandiri (*local web dashboard*) yang ringan dan cepat. Mengedepankan filosofi **Mobile-View First**, sehingga nyaman dan intuitif dibuka dari layar smartphone saat pengguna sedang bepergian.

## Fitur Antarmuka
1. **TradingView Lightweight Charts:**
   - Visualisasi candlestick cepat tanpa beban berat.
   - Menggambar garis dinamis Trailing Stop yang naik seiring kenaikan harga.
   - Menampilkan area proyeksi probabilitas Google TimesFM (Fan Chart P10 - P90) di masa depan.
2. **Tri-Channel Approval Gate:**
   - Mendukung otorisasi transaksi melalui antarmuka tombol Web, Terminal CLI, atau Bot Telegram.
3. **Keamanan Tanpa Kebocoran (Zero-Client-Side Leak):**
   - Frontend hanya menerima JSON data visual grafik. Token API broker atau variabel `.env` sama sekali tidak pernah dikirimkan ke browser.
