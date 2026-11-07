---
name: masterhttprelayvpn-rust
description: Rust CLI + desktop UI for DPI bypass via Google Apps Script relay with TLS SNI concealment, supporting HTTP and SOCKS5 proxies
triggers:
  - set up MasterHttpRelayVPN rust
  - configure DPI bypass with Google Apps Script
  - run mhrv-rs proxy server
  - bypass censorship with SNI fronting
  - set up HTTP SOCKS5 proxy with TLS concealment
  - configure apps script relay proxy
  - help me use mhrv-rs
  - deploy Google Apps Script VPN relay
---

# MasterHttpRelayVPN-RUST

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Rust port of MasterHttpRelayVPN that routes traffic through a Google Apps Script relay, hiding the real destination from DPI/censorship systems. The ISP sees TLS SNI `www.google.com`; the actual request is proxied inside the encrypted tunnel through your own Google Apps Script deployment.

## How it works

```
Browser → HTTP(8085)/SOCKS5(8086) → mhrv-rs → TLS to Google IP (SNI: www.google.com)
       → Google edge → Apps Script relay → real destination
```

## Install

### Prebuilt binaries (recommended)

Download from [releases page](https://github.com/therealaleph/MasterHttpRelayVPN-RUST/releases):
- Linux: `mhrv-rs-linux-x86_64.tar.gz`
- macOS: `mhrv-rs-macos-aarch64.tar.gz` or `mhrv-rs-macos-x86_64.tar.gz`
- Windows: `mhrv-rs-windows-x86_64.zip`
- Android: `mhrv-rs-android-universal-v*.apk`

### Build from source

```bash
# CLI only
cargo build --release

# CLI + desktop UI (egui)
cargo build --release --features ui

# Binaries output to:
# target/release/mhrv-rs       (CLI)
# target/release/mhrv-rs-ui    (Desktop UI)
```

## First Run: Install MITM CA

Required for HTTPS interception. Run once with elevated privileges:

```bash
# macOS / Linux
sudo ./mhrv-rs --install-cert

# Windows (run as Administrator)
mhrv-rs.exe --install-cert

# Or use platform launchers (also starts the UI):
./run.command   # macOS
./run.sh        # Linux
run.bat         # Windows
```

The CA keypair is generated locally (`ca/ca.crt` + `ca/ca.key`) and never leaves your machine.

## Configuration

### Config file locations

- macOS: `~/Library/Application Support/mhrv-rs/config.json`
- Linux: `~/.config/mhrv-rs/config.json`
- Windows: `%APPDATA%\mhrv-rs\config.json`
- Fallback: `./config.json` (current directory)

### Minimal `config.json`

```json
{
  "mode": "apps_script",
  "script_id": "AKfycby...",
  "auth_key": "$AUTH_KEY_FROM_CODE_GS",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "http_port": 8085,
  "socks5_port": 8086
}
```

### Full `config.json` with all options

```json
{
  "mode": "apps_script",
  "script_id": "AKfycby...,AKfycbz...",
  "auth_key": "$YOUR_AUTH_KEY",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "http_port": 8085,
  "socks5_port": 8086,
  "hosts": {
    "example.com": "direct"
  },
  "upstream_socks5": null
}
```

**Key fields:**
- `mode`: `"apps_script"` (default) or `"google_only"` (no relay, Google domains only)
- `script_id`: Deployment ID from Google Apps Script. Comma-separate multiple for round-robin rotation
- `auth_key`: Secret matching `AUTH_KEY` in your `Code.gs`
- `google_ip`: Google edge IP — `216.239.38.120` is a reliable default
- `front_domain`: Keep as `www.google.com`
- `hosts`: Per-domain overrides — `"direct"` bypasses the relay entirely
- `upstream_socks5`: Forward through an external SOCKS5 (e.g. `"127.0.0.1:1080"`)

### Google-only mode (no Apps Script needed)

```json
{
  "mode": "google_only",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "http_port": 8085,
  "socks5_port": 8086
}
```

Use this to bootstrap — access `script.google.com` to deploy `Code.gs` when Google is blocked.

## CLI Commands

```bash
# Start proxy server (reads config.json)
mhrv-rs serve

# Start with explicit config file
mhrv-rs serve --config /path/to/config.json

# Test end-to-end relay connectivity
mhrv-rs test

# Test SNI fronting only (no config required beyond google_ip + front_domain)
mhrv-rs test-sni

# Scan for fastest Google IP from your network
mhrv-rs scan-ips

# Install MITM CA to system trust store
mhrv-rs --install-cert

# Show version
mhrv-rs --version

# Show help
mhrv-rs --help
```

## Deploy the Google Apps Script Relay

1. Go to https://script.google.com → **New project**
2. Replace default code with contents of [`Code.gs`](https://github.com/therealaleph/MasterHttpRelayVPN-RUST/blob/main/assets/apps_script/Code.gs)
3. Set your auth key:
   ```javascript
   const AUTH_KEY = "your-strong-secret-here";
   ```
4. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Copy the **Deployment ID** (looks like `AKfycby...`)
6. Paste it into `config.json` as `script_id`

## Common Patterns

### Proxy browser traffic (HTTP proxy)

Set browser proxy to `127.0.0.1:8085` (HTTP). Most browsers: Settings → Network → Manual proxy.

```bash
# Test with curl through the HTTP proxy
curl -x http://127.0.0.1:8085 https://example.com
```

### Proxy via SOCKS5

```bash
# curl via SOCKS5
curl --socks5 127.0.0.1:8086 https://example.com

# Use with any SOCKS5-aware application
export ALL_PROXY=socks5://127.0.0.1:8086
```

### Multiple script IDs for higher quota

```json
{
  "script_id": "AKfycby_first...,AKfycby_second...,AKfycby_third..."
}
```

Each Google Apps Script deployment has its own quota. Round-robin rotation spreads load.

### Per-domain direct routing

```json
{
  "hosts": {
    "internal.company.com": "direct",
    "192.168.1.0/24": "direct"
  }
}
```

### Use with xray/v2ray as upstream

```json
{
  "upstream_socks5": "127.0.0.1:10808"
}
```

### Headless server deployment

```bash
# Run CLI in background
nohup mhrv-rs serve > mhrv-rs.log 2>&1 &

# Or with systemd
cat > /etc/systemd/system/mhrv-rs.service << 'EOF'
[Unit]
Description=MasterHttpRelayVPN-RUST
After=network.target

[Service]
ExecStart=/usr/local/bin/mhrv-rs serve
Restart=on-failure
User=nobody
WorkingDirectory=/etc/mhrv-rs

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now mhrv-rs
```

## Desktop UI

```bash
# Launch UI directly
./mhrv-rs-ui        # Linux/macOS
mhrv-rs-ui.exe      # Windows
```

UI features:
- Config form with all settings
- **Start / Stop** proxy server
- **Test** button — sends one request through the relay end-to-end
- **Scan** button — finds fastest Google IP for your network
- Live traffic stats
- Log panel

## Android

1. Install `mhrv-rs-android-universal-v*.apk`
2. Follow [docs/android.md](https://github.com/therealaleph/MasterHttpRelayVPN-RUST/blob/main/docs/android.md)
3. The app uses TUN via `tun2proxy` to capture all device IP traffic

**Android HTTPS caveat:** From Android 7+, apps must opt in to trust user CAs. Chrome and Firefox work; Telegram, WhatsApp, Instagram, etc. do not. For those apps:
- Use SOCKS5 mode: point in-app proxy to `127.0.0.1:1081`
- Use `google_only` mode for Google services (no CA needed)
- Set `upstream_socks5` to an external VPS

## Troubleshooting

### "Connection refused" on proxy port

```bash
# Check if mhrv-rs is running
ps aux | grep mhrv-rs

# Check ports are listening
ss -tlnp | grep -E '8085|8086'   # Linux
netstat -an | grep -E '8085|8086' # macOS/Windows

# Try a different port if 8085 is taken
# Set http_port: 8181 in config.json
```

### HTTPS sites show certificate error

```bash
# CA not installed — run:
sudo mhrv-rs --install-cert

# Firefox: manually import ca/ca.crt
# Settings → Privacy & Security → Certificates → View Certificates → Authorities → Import
```

### Apps Script relay errors / quota exceeded

- Add more `script_id` entries (comma-separated) for rotation
- Check your Apps Script execution log at https://script.google.com
- Verify `AUTH_KEY` in `Code.gs` matches `auth_key` in `config.json`

### Find a working Google IP

```bash
mhrv-rs scan-ips
```

Update `google_ip` in config with the fastest result.

### Can't reach script.google.com to deploy Code.gs

Use `google_only` mode temporarily:

```bash
cp config.google-only.example.json config.json
mhrv-rs serve
# Set browser proxy to 127.0.0.1:8085
# Now open script.google.com in browser and deploy Code.gs
```

### Test SNI fronting without full config

```bash
mhrv-rs test-sni
```

### Verify relay is working end-to-end

```bash
mhrv-rs test
# Or via curl:
curl -v -x http://127.0.0.1:8085 https://httpbin.org/ip
```

## File Structure

```
mhrv-rs/                     # binary
mhrv-rs-ui/                  # desktop UI binary
config.json                  # your config
ca/
  ca.crt                     # MITM root cert (public, installed to system)
  ca.key                     # MITM root key (private, stays local)
assets/
  apps_script/
    Code.gs                  # Apps Script relay source to deploy to Google
```
