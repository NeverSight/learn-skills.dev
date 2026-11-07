---
name: masterhttprelayvpn-proxy
description: Domain-fronted HTTP/SOCKS5 proxy tunneling traffic through Google Apps Script with MITM TLS interception and DPI evasion
triggers:
  - set up MasterHttpRelayVPN
  - configure Google Apps Script proxy tunnel
  - domain fronting proxy python
  - bypass DPI with Google fronting
  - MITM TLS proxy with Google relay
  - HTTP SOCKS5 proxy tunnel setup
  - MasterHttpRelayVPN configuration
  - install Google relay VPN proxy
---

# MasterHttpRelayVPN Proxy

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

MasterHttpRelayVPN is a domain-fronted HTTP/SOCKS5 proxy that tunnels traffic through Google Apps Script. It disguises requests as Google traffic to evade DPI/firewalls, performs local MITM TLS interception to re-encrypt traffic, and requires only a free Google account — no VPS needed.

**Traffic flow:**
```
Browser → Local Proxy (127.0.0.1:8085) → Google IP (front_domain) → Apps Script Relay → Target Website
```

---

## Installation

```bash
git clone https://github.com/masterking32/MasterHttpRelayVPN.git
cd MasterHttpRelayVPN
pip install -r requirements.txt
```

**Behind a firewall (PyPI mirror):**
```bash
pip install -r requirements.txt -i https://mirror-pypi.runflare.com/simple/ --trusted-host mirror-pypi.runflare.com
```

**Quick start scripts (handles venv + deps automatically):**
```bash
# Linux/macOS
chmod +x start.sh && ./start.sh

# Windows
start.bat
```

---

## Step 1: Deploy the Google Apps Script Relay

1. Go to [https://script.google.com/](https://script.google.com/) and create a **New project**
2. Delete default code, paste the contents of `apps_script/Code.gs`
3. Set a strong password on this line:
   ```javascript
   const AUTH_KEY = "your-secret-password-here";
   ```
4. Click **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Copy the **Deployment ID** (long random string)

---

## Step 2: Configure

### Option A — Interactive wizard (recommended)
```bash
python setup.py
```
Prompts for Deployment ID, generates a random `auth_key`, writes `config.json`.

### Option B — Manual config

```bash
cp config.example.json config.json
```

Edit `config.json`:
```json
{
  "mode": "apps_script",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "script_id": "AKfycb...",
  "auth_key": "your-secret-password-here",
  "listen_host": "127.0.0.1",
  "listen_port": 8085,
  "socks5_enabled": true,
  "socks5_port": 1080,
  "log_level": "INFO",
  "verify_ssl": true
}
```

> `auth_key` in `config.json` **must match** `AUTH_KEY` in `Code.gs`.

---

## Step 3: Run

```bash
python3 main.py
```

Install CA certificate (run once, or re-run anytime):
```bash
python main.py --install-cert
```

---

## Configuration Reference

### Main Settings

| Key | Description |
|-----|-------------|
| `mode` | Always `"apps_script"` |
| `script_id` | Google Apps Script Deployment ID |
| `auth_key` | Shared secret between proxy and relay |
| `listen_host` | `"127.0.0.1"` (local only) or `"0.0.0.0"` (LAN) |
| `listen_port` | HTTP proxy port (default: `8085`) |
| `socks5_enabled` | Enable SOCKS5 listener |
| `socks5_port` | SOCKS5 port (default: `1080`) |
| `log_level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### Advanced Settings

| Key | Default | Description |
|-----|---------|-------------|
| `google_ip` | `"216.239.38.120"` | Google IP to connect through |
| `front_domain` | `"www.google.com"` | Domain shown to firewall |
| `verify_ssl` | `true` | Verify upstream TLS certs |
| `script_ids` | `[]` | Multiple deployment IDs for load balancing |
| `lan_sharing` | `false` | Allow LAN devices to use proxy |
| `block_hosts` | `[]` | Hosts that return HTTP 403 (e.g. `".doubleclick.net"`) |
| `bypass_hosts` | `["localhost", ".local", ".lan", ".home.arpa"]` | Hosts that go direct (no MITM/relay) |

### Full config example with all advanced options

```json
{
  "mode": "apps_script",
  "google_ip": "216.239.38.120",
  "front_domain": "www.google.com",
  "script_ids": [
    "AKfycbDEPLOYMENT_ID_1",
    "AKfycbDEPLOYMENT_ID_2"
  ],
  "auth_key": "super-strong-random-password",
  "listen_host": "0.0.0.0",
  "listen_port": 8085,
  "socks5_enabled": true,
  "socks5_port": 1080,
  "lan_sharing": true,
  "log_level": "INFO",
  "verify_ssl": true,
  "block_hosts": [
    ".doubleclick.net",
    "ads.example.com"
  ],
  "bypass_hosts": [
    "localhost",
    ".local",
    ".lan",
    "192.168.1.1"
  ]
}
```

---

## CA Certificate Installation (Required for HTTPS)

The proxy performs MITM TLS interception. A local CA is generated at `ca/ca.crt` on first run. Install it once per machine/browser.

### Linux (Ubuntu/Debian)
```bash
sudo cp ca/ca.crt /usr/local/share/ca-certificates/masterhttp-relay.crt
sudo update-ca-certificates
```

### macOS
```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca/ca.crt
```

### Windows (PowerShell as Admin)
```powershell
certutil -addstore -f "ROOT" ca\ca.crt
```

### Firefox (all platforms)
Settings → Privacy & Security → Certificates → View Certificates → Authorities → Import → select `ca/ca.crt` → check "Trust this CA to identify websites"

> ⚠️ Never share the `ca/` folder. Delete it to regenerate a fresh CA.

---

## Browser Proxy Configuration

**HTTP Proxy:** `127.0.0.1:8085`  
**SOCKS5 Proxy:** `127.0.0.1:1080`

### Firefox
Settings → General → Network Settings → Manual proxy configuration:
- HTTP Proxy: `127.0.0.1`, Port: `8085`
- Check: "Also use this proxy for HTTPS"

### Chrome/Edge (Windows system proxy)
Settings → Network → Proxy → Manual proxy setup → `127.0.0.1:8085`

### Using curl for testing
```bash
curl -x http://127.0.0.1:8085 https://example.com
# or SOCKS5
curl --socks5 127.0.0.1:1080 https://example.com
```

### Using requests in Python
```python
import requests

proxies = {
    "http": "http://127.0.0.1:8085",
    "https": "http://127.0.0.1:8085",
}
response = requests.get("https://example.com", proxies=proxies)
print(response.status_code)
```

---

## LAN Sharing Setup

Allow other devices on your network to use the proxy:

```json
{
  "lan_sharing": true,
  "listen_host": "0.0.0.0",
  "listen_port": 8085
}
```

On startup, the proxy logs your LAN IP addresses. Configure other devices to use `<YOUR_LAN_IP>:8085`.

---

## Load Balancing with Multiple Relays

Deploy multiple Google Apps Script projects and list all Deployment IDs:

```json
{
  "script_ids": [
    "AKfycbFIRST_DEPLOYMENT_ID",
    "AKfycbSECOND_DEPLOYMENT_ID",
    "AKfycbTHIRD_DEPLOYMENT_ID"
  ],
  "auth_key": "same-password-in-all-scripts"
}
```

> All Apps Script deployments must have the same `AUTH_KEY` value.

---

## Common Patterns

### Blocking ads/trackers
```json
{
  "block_hosts": [
    ".doubleclick.net",
    ".googlesyndication.com",
    ".googleadservices.com",
    "ads.example.com"
  ]
}
```

### Bypassing local/LAN resources (no MITM)
```json
{
  "bypass_hosts": [
    "localhost",
    "127.0.0.1",
    ".local",
    ".lan",
    ".home.arpa",
    "192.168.1.0/24"
  ]
}
```

### Running with debug logging
```bash
# In config.json
{ "log_level": "DEBUG" }

# Or temporarily
python3 main.py
```

### Scripted config generation
```python
import json
import secrets

config = {
    "mode": "apps_script",
    "google_ip": "216.239.38.120",
    "front_domain": "www.google.com",
    "script_id": "PASTE_DEPLOYMENT_ID_HERE",
    "auth_key": secrets.token_urlsafe(32),
    "listen_host": "127.0.0.1",
    "listen_port": 8085,
    "socks5_enabled": True,
    "socks5_port": 1080,
    "log_level": "INFO",
    "verify_ssl": True
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

print(f"Generated auth_key: {config['auth_key']}")
print("Remember to set this same value as AUTH_KEY in Code.gs")
```

---

## Troubleshooting

### "Security warning" on every website
→ CA certificate not installed. Run `python main.py --install-cert` or follow the manual install steps above.

### Connection refused on port 8085
→ Check `listen_host` and `listen_port` in `config.json`. Make sure `python3 main.py` is running.

### "403 Forbidden" from relay
→ `auth_key` in `config.json` does not match `AUTH_KEY` in deployed `Code.gs`. Redeploy the script after fixing.

### Google Apps Script quota exceeded
→ Free tier has daily quotas. Add more `script_ids` in `config.json` for load balancing across multiple deployments.

### `verify_ssl` errors
```json
{ "verify_ssl": false }
```
Use only for testing; not recommended for production.

### Regenerate CA certificate
```bash
rm -rf ca/
python3 main.py  # generates new ca/ca.crt on startup
# Then reinstall the certificate in OS/browser
```

### Can't install Python packages (behind firewall)
```bash
pip install -r requirements.txt \
  -i https://mirror-pypi.runflare.com/simple/ \
  --trusted-host mirror-pypi.runflare.com
```

### Test the proxy is working
```bash
# Should return your external IP routed through Google
curl -x http://127.0.0.1:8085 https://api.ipify.org
```

---

## Project Structure

```
MasterHttpRelayVPN/
├── main.py              # Entry point, starts HTTP + SOCKS5 listeners
├── setup.py             # Interactive config wizard
├── config.json          # Your configuration (gitignored)
├── config.example.json  # Template
├── requirements.txt     # Python dependencies
├── apps_script/
│   └── Code.gs          # Google Apps Script relay code
├── ca/
│   ├── ca.crt           # Generated CA certificate (install this)
│   └── ca.key           # CA private key (keep secret)
├── start.sh             # Linux/macOS quick start
└── start.bat            # Windows quick start
```
