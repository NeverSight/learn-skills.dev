---
name: browser-tape-interceptor
description: Menghubungkan sesi browser Google Chrome pengguna via Chrome DevTools Protocol (CDP) atau Playwright untuk menyadap aliran WebSocket running trade dan kedalaman orderbook web broker secara aman tanpa pernah menyentuh password pengguna.
---

# Browser Tape Interceptor Skill

## Ringkasan Peran
Menjembatani AI Agent dengan akun web trading aktif milik pengguna. Beroperasi dengan protokol **Zero-Password-Risk**, di mana pengguna melakukan login mandiri (memasukkan kredensial dan 2FA/biometrik sendiri di browser pribadi). Agent kemudian mengaitkan diri (*attach*) ke browser tersebut melalui port remote debugging untuk menyadap paket data aliran transaksi secara pasif.

## Mekanisme Eksekusi
1. **Remote Attaching:**
   - Menghubungkan ke instance Chrome lokal via `--remote-debugging-port=9222`.
   - Mendeteksi tab aktif yang membuka platform web trading broker (TradingView Web, Stockbit, Mirae Neo, Mandiri MOST, Binance Web, dll).
2. **Network Interception:**
   - Mengaktifkan pendengar `Network.webSocketFrameReceived` pada CDP.
   - Mengurai payload WebSocket yang memuat transaksi *running trade* (Waktu, Ticker, Harga, Lot/Volume, Tipe Agresi Buy/Sell).
3. **Penyaluran Data:**
   - Mengalirkan data yang di-intercept ke modul `orderflow-tape-scalper` untuk pemrosesan mikrostruktur volume.
