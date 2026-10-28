---
name: mhr-cfw-domain-fronting-relay
description: Expert skill for setting up and using MHR-CFW, a domain-fronting relay that routes traffic through Google Apps Script and Cloudflare Workers to bypass DPI filtering.
triggers:
  - set up domain fronting relay
  - bypass DPI with Google Apps Script
  - configure mhr-cfw proxy
  - route traffic through cloudflare worker
  - set up MasterHttpRelay
  - domain fronting proxy python
  - google apps script relay setup
  - bypass deep packet inspection proxy
---

# MHR-CFW Domain-Fronting Relay

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

MHR-CFW (MasterHttpRelay + Cloudflare Worker) is a Python-based domain-fronting relay that routes HTTP/SOCKS5 proxy traffic through Google Apps Script (GAS) and Cloudflare Workers. Network DPI filters see only traffic to `www.google.com`, while the actual destination is hidden inside the relay chain.

## Traffic Flow

```
Client → Local Proxy (127.0.0.1:8085)
           ↓
       Google IP (216.239.38.120) — DPI sees www.google.com
           ↓
       Google Apps Script Web App (Relay)
           ↓
       Cloudflare Worker
           ↓
       Target Website
```

---

## Installation

```bash
git clone https://github.com/denuitt1/mhr-cfw.git
cd mhr-cfw
pip install -r requirements.txt
```

If PyPI is blocked:
```bash
pip install -r requirements.txt \
  -i https://mirror-pypi.runflare.com/simple/ \
  --trusted-host mirror-pypi.runflare.com
```

---

## Full Setup Guide

### Step 1: Deploy the Cloudflare Worker

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **Compute > Workers & Pages**
3. Click **Create Application** → **Start with Hello World** → **Deploy**
4. Click **Edit code**, delete all default code
5. Paste the contents of `script/worker.js` from the repo
6. Edit the worker URL constant:
   ```javascript
   const WORKER_URL = "your-worker-name.workers.dev";
   ```
7. Click **Deploy** — note your worker URL (e.g., `your-worker-name.workers.dev`)

### Step 2: Deploy the Google Apps Script Relay

1. Go to [script.google.com](https://script.google.com) and create a **New project**
2. Delete all default code
3. Paste the contents of `script/Code.gs` from the repo
4. Edit these two constants at the top:
   ```javascript
   const AUTH_KEY = "your-secret-password-here";   // choose a strong password
   const WORKER_URL = "https://your-worker-name.workers.dev";
   ```
5. Click **Deploy** → **New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
6. Click **Deploy** and **copy the Deployment ID** (long random string like `AKfycb...`)

### Step 3: Configure `config.json`

```bash
cp config.example.json config.json
```

Edit `config.json`:
```json
{
  "mode": "apps_script",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "script_id": "AKfycbXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "auth_key": "your-secret-password-here",
  "listen_host": "127.0.0.1",
  "listen_port": 8085,
  "socks5_enabled": true,
  "socks5_port": 1080,
  "log_level": "INFO",
  "verify_ssl": true
}
```

| Field | Description |
|---|---|
| `mode` | Always `"apps_script"` for GAS relay |
| `google_ip` | IP of Google's infrastructure for fronting |
| `front_domain` | Domain shown to DPI (`www.google.com`) |
| `script_id` | Your GAS Deployment ID from Step 2 |
| `auth_key` | Must match `AUTH_KEY` in `Code.gs` |
| `listen_host` | Local bind address (keep `127.0.0.1`) |
| `listen_port` | HTTP proxy port (default `8085`) |
| `socks5_enabled` | Enable SOCKS5 proxy on `socks5_port` |
| `socks5_port` | SOCKS5 proxy port (default `1080`) |
| `log_level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `verify_ssl` | Verify SSL certs; set `false` to skip |

### Step 4: Run the Proxy

**Linux/macOS:**
```bash
bash start.sh
# or
python3 main.py
```

**Windows:**
```
start.bat
```

Expected output:
```
[INFO] HTTP proxy running on 127.0.0.1:8085
[INFO] SOCKS5 proxy running on 127.0.0.1:1080
```

---

## Using the Proxy

### Browser via FoxyProxy

Install [FoxyProxy](https://getfoxyproxy.org/):
- **Chrome:** [Chrome Web Store](https://chromewebstore.google.com/detail/foxyproxy/gcknhkkoolaabfmlnjonogaaifnjlfnp)
- **Firefox:** [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/)

Configure FoxyProxy:
- Proxy Type: `HTTP` or `SOCKS5`
- Host: `127.0.0.1`
- Port: `8085` (HTTP) or `1080` (SOCKS5)

### curl (HTTP proxy)

```bash
curl -x http://127.0.0.1:8085 https://ipleak.net/json/
```

### curl (SOCKS5 proxy)

```bash
curl --socks5 127.0.0.1:1080 https://ipleak.net/json/
```

### Python requests

```python
import requests

proxies = {
    "http": "http://127.0.0.1:8085",
    "https": "http://127.0.0.1:8085",
}

response = requests.get("https://ipleak.net/json/", proxies=proxies)
print(response.json())
```

### Python with SOCKS5

```python
import requests

proxies = {
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080",
}

response = requests.get("https://ipleak.net/json/", proxies=proxies)
print(response.json())
```

---

## Configuration Patterns

### Minimal config (HTTP only, no SOCKS5)

```json
{
  "mode": "apps_script",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "script_id": "YOUR_DEPLOYMENT_ID",
  "auth_key": "YOUR_AUTH_KEY",
  "listen_host": "127.0.0.1",
  "listen_port": 8085,
  "socks5_enabled": false,
  "log_level": "INFO",
  "verify_ssl": true
}
```

### Debug config (verbose logging, skip SSL verification)

```json
{
  "mode": "apps_script",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "script_id": "YOUR_DEPLOYMENT_ID",
  "auth_key": "YOUR_AUTH_KEY",
  "listen_host": "127.0.0.1",
  "listen_port": 8085,
  "socks5_enabled": true,
  "socks5_port": 1080,
  "log_level": "DEBUG",
  "verify_ssl": false
}
```

### Listen on all interfaces (for LAN sharing)

```json
{
  "listen_host": "0.0.0.0",
  "listen_port": 8085
}
```

> ⚠️ Only use `0.0.0.0` on trusted networks. Anyone on the LAN can use your proxy.

---

## Cloudflare Worker (`script/worker.js`) — Key Structure

```javascript
// The worker receives proxied requests and forwards them to the target
const WORKER_URL = "your-worker-name.workers.dev"; // set this to your own worker

addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request));
});
```

The worker:
- Receives requests from GAS relay
- Extracts the target URL from the request
- Fetches the target on behalf of the client
- Returns the response back through the chain

---

## Google Apps Script (`script/Code.gs`) — Key Structure

```javascript
const AUTH_KEY = "your-secret-password-here";      // must match config.json auth_key
const WORKER_URL = "https://your-worker.workers.dev";

function doPost(e) {
  // Validates AUTH_KEY, extracts target URL, forwards via WORKER_URL
}
```

The GAS relay:
- Exposes a public HTTPS endpoint (`/exec`) that acts as the domain-fronted relay
- Validates `AUTH_KEY` on every request
- Forwards validated requests to your Cloudflare Worker

---

## Verifying It Works

After starting the proxy and configuring your browser:

1. Visit [ipleak.net](https://ipleak.net) — your IP should show as a Cloudflare IP
2. Visit [whoer.net](https://whoer.net) — should reflect Cloudflare's location
3. Via curl:
   ```bash
   curl -x http://127.0.0.1:8085 https://ipleak.net/json/ | python3 -m json.tool
   ```
   Look for `"ip"` showing a Cloudflare address range.

---

## Troubleshooting

### Proxy starts but no traffic gets through

- Verify `script_id` in `config.json` is the **Deployment ID**, not the Script ID
- Re-check that `auth_key` in `config.json` exactly matches `AUTH_KEY` in `Code.gs`
- In GAS, confirm deployment is set to **Execute as: Me** and **Who has access: Anyone**
- Try redeploying the GAS app — old deployments sometimes break

### SSL errors

```json
"verify_ssl": false
```
Set to `false` temporarily to diagnose. Re-enable for production use.

### `pip install` fails (PyPI blocked)

```bash
pip install -r requirements.txt \
  -i https://mirror-pypi.runflare.com/simple/ \
  --trusted-host mirror-pypi.runflare.com
```

### GAS quota exceeded

Google Apps Script has daily quotas (~20,000 URL fetch calls/day for free accounts). If the relay stops working mid-day:
- Use a different Google account for a fresh GAS deployment
- Deploy multiple GAS relays and alternate `script_id` values

### Port already in use

```json
{
  "listen_port": 8086,
  "socks5_port": 1081
}
```
Change ports in `config.json` and update your browser/FoxyProxy settings.

### Cloudflare Worker errors (5xx)

- Check the worker is deployed and the `WORKER_URL` in `Code.gs` matches exactly
- Visit `https://your-worker.workers.dev` directly in browser — should respond (even with an error page) rather than timeout
- Check Cloudflare Worker logs in the dashboard under **Workers & Pages > your worker > Logs**

### Debug logging

```json
"log_level": "DEBUG"
```
Restart `main.py` — you'll see each relay hop logged to stdout.

---

## Environment Variable Pattern for Automation

When scripting deployment or CI, avoid hardcoding secrets. Use environment variables and generate config dynamically:

```python
import json
import os

config = {
    "mode": "apps_script",
    "google_ip": "216.239.38.120",
    "front_domain": "www.google.com",
    "script_id": os.environ["GAS_DEPLOYMENT_ID"],
    "auth_key": os.environ["MHR_AUTH_KEY"],
    "listen_host": "127.0.0.1",
    "listen_port": int(os.environ.get("MHR_PORT", "8085")),
    "socks5_enabled": True,
    "socks5_port": 1080,
    "log_level": os.environ.get("MHR_LOG_LEVEL", "INFO"),
    "verify_ssl": True
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

print("config.json written")
```

Then run:
```bash
export GAS_DEPLOYMENT_ID="AKfycbXXXXXXXXXXXXXX"
export MHR_AUTH_KEY="$(openssl rand -hex 32)"
python3 write_config.py
python3 main.py
```

---

## Project File Reference

| File | Purpose |
|---|---|
| `main.py` | Entry point — starts HTTP and SOCKS5 proxy listeners |
| `config.json` | Runtime configuration (copy from `config.example.json`) |
| `config.example.json` | Template configuration with placeholder values |
| `script/worker.js` | Cloudflare Worker source — deploy to Cloudflare |
| `script/Code.gs` | Google Apps Script relay source — deploy to GAS |
| `start.bat` | Windows launcher |
| `start.sh` | Linux/macOS launcher |
| `requirements.txt` | Python dependencies |
