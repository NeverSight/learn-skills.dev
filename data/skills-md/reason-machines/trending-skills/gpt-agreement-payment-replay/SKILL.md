---
name: gpt-agreement-payment-replay
description: End-to-end protocol replay toolkit for ChatGPT Plus/Team/Pro subscription with hCaptcha visual solver and anti-fraud empirical research
triggers:
  - "set up gpt agreement payment"
  - "run chatgpt subscription replay pipeline"
  - "configure hcaptcha solver"
  - "set up paypal billing agreement replay"
  - "run daemon mode for subscription pipeline"
  - "configure stripe checkout replay"
  - "debug pipeline replay errors"
  - "extend hcaptcha solver with new challenge type"
---

# Gpt-Agreement-Payment Replay Toolkit

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

End-to-end protocol replay toolkit that automates the `Stripe Checkout → PayPal billing agreement → ChatGPT manual-approval → Codex OAuth + PKCE` chain. Includes a from-scratch hCaptcha visual solver (~4000 lines), empirical anti-fraud research data, and a 12-path self-healing daemon.

---

## Installation

### System Requirements

- Linux (Ubuntu 22.04+ recommended), ~5 GB disk, ~2 GB RAM
- Python 3.11+
- Xvfb for headless browser automation

```bash
# System dependencies
sudo apt-get install -y xvfb xauth gost

# Clone
git clone https://github.com/DanOps-1/Gpt-Agreement-Payment
cd Gpt-Agreement-Payment

# Core Python dependencies
pip install requests curl_cffi playwright camoufox browserforge mitmproxy pybase64

# Install browser engines
playwright install firefox
camoufox fetch
```

### ML Dependencies for hCaptcha Solver (optional, ~4 GB)

```bash
python -m venv ~/.venvs/ctfml
~/.venvs/ctfml/bin/pip install torch transformers opencv-python pillow numpy
```

### WebUI (recommended for first-time setup)

```bash
pip install -r webui/requirements.txt
cd webui/frontend && pnpm i && pnpm build && cd ../..
python -m webui.server
# Open http://127.0.0.1:8765 — runs 14-step wizard, generates configs
```

---

## Prerequisites Checklist

Before running, you need:

| Requirement | Notes |
|---|---|
| PayPal account (EU) | Must be EU-based (IE, DE, FR, etc.); first run needs manual OTP 2FA |
| EU/US proxy | PayPal is region-locked; Stripe is country-locked |
| Cloudflare zone | For catch-all subdomain email registration |
| Linux with Camoufox + Playwright | ~5 GB disk + 2 GB RAM |
| VLM API key (optional) | OpenAI-compatible endpoint for hCaptcha solving |
| CAPTCHA platform API key (optional) | createTask/getTaskResult protocol, fallback for passive captcha |

---

## Configuration

### Copy and Edit Config Templates

```bash
cp CTF-pay/config.paypal.example.json     CTF-pay/config.paypal.json
cp CTF-reg/config.paypal-proxy.example.json   CTF-reg/config.paypal-proxy.json
```

### config.paypal.json — Key Fields

```json
{
  "proxy": {
    "host": "your-proxy-host",
    "port": 1080,
    "username": "PROXY_USER",
    "password": "PROXY_PASS",
    "protocol": "socks5"
  },
  "paypal": {
    "email": "your-paypal-email@example.com",
    "password": "PAYPAL_PASS",
    "totp_secret": "PAYPAL_TOTP_SECRET"
  },
  "cloudflare": {
    "api_token": "CF_API_TOKEN",
    "zone_id": "CF_ZONE_ID",
    "domain": "yourdomain.com"
  },
  "webshare": {
    "api_key": "WEBSHARE_API_KEY"
  },
  "vlm": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "VLM_API_KEY",
    "model": "gpt-4o"
  },
  "captcha_platform": {
    "api_key": "CAPTCHA_PLATFORM_KEY",
    "base_url": "https://api.2captcha.com"
  },
  "subscription_type": "team",
  "output_path": "output/results.jsonl"
}
```

### Environment Variables (alternative to config file)

```bash
export PROXY_HOST="your-proxy-host"
export PROXY_PORT="1080"
export PAYPAL_EMAIL="your@email.com"
export PAYPAL_PASS="yourpassword"
export CF_API_TOKEN="your-cloudflare-token"
export CF_ZONE_ID="your-zone-id"
export VLM_API_KEY="your-vlm-key"
export WEBSHARE_API_KEY="your-webshare-key"
```

---

## Running the Pipeline

### Single Run (full flow)

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal
```

Output: `output/results.jsonl` containing `refresh_token` on success.

### Daemon Mode (continuous pool maintenance)

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal \
  --daemon
```

### Batch Mode

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal \
  --batch \
  --count 10
```

### Self-Dealer Mode

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal \
  --self-dealer
```

---

## Pipeline Architecture

```
pipeline.py
  └─ CTF-reg/browser_register.py   # Camoufox + Cloudflare Turnstile
  └─ CTF-pay/card.py               # Stripe Checkout replay (8000 lines)
       └─ Stripe confirm
       └─ ChatGPT /approve
       └─ Camoufox PayPal billing agreement
       └─ Stripe poll state=succeeded
       └─ Camoufox second login → Codex OAuth + PKCE
  └─ output/results.jsonl          # Final refresh_token
```

---

## hCaptcha Solver

### Standalone Usage

```python
import sys
sys.path.insert(0, '/path/to/Gpt-Agreement-Payment')

# Activate ML venv first if using VLM/CLIP paths
from CTF_pay.hcaptcha_auto_solver import HCaptchaSolver

solver = HCaptchaSolver(
    vlm_base_url="https://api.openai.com/v1",
    vlm_api_key="VLM_API_KEY",
    vlm_model="gpt-4o",
    use_clip_fallback=True,
    use_opencv_fallback=True,
)

# With a Playwright page that has an hCaptcha iframe
async def solve_on_page(page):
    result = await solver.solve(page)
    return result  # True if solved, False if failed
```

### Three-Layer Decision Flow

```
1. VLM primary path     — sends challenge image to VLM, parses coordinate response
2. CLIP heuristic       — cosine similarity between challenge prompt and image tiles
3. OpenCV fallback      — contour/template matching for known visual patterns
```

### Supported Challenge Types (12)

| Type | Description |
|---|---|
| `select-image` | Select all images matching description |
| `bounding-box` | Draw bounding box around object |
| `image-label` | Label images as matching/not-matching |
| `click-point` | Click specific point on image |
| `drag-drop` | Drag element to target |
| `3d-rotate` | Rotate 3D object to match |
| `object-count` | Count objects in image |
| `text-in-image` | Identify text shown in image |
| `shape-match` | Match shapes by property |
| `spatial-relation` | Identify spatial relationships |
| `color-match` | Match by color |
| `pattern-complete` | Complete a visual pattern |

### Adding a New Challenge Type

```python
# In CTF-pay/hcaptcha_auto_solver.py, extend the solver class:

class HCaptchaSolver:
    # ... existing code ...

    async def _solve_my_new_type(self, challenge_data: dict) -> list[tuple[int, int]]:
        """
        Solver for 'my-new-type' challenge.
        challenge_data keys: 'prompt', 'images', 'type'
        Returns list of (x, y) click coordinates.
        """
        prompt = challenge_data['prompt']
        images = challenge_data['images']  # list of PIL.Image or base64 strings

        # Option A: VLM path
        coords = await self._vlm_solve(prompt, images)

        # Option B: CLIP heuristic
        scores = self._clip_score(prompt, images)
        coords = [(img['x'], img['y']) for img, s in zip(images, scores) if s > 0.25]

        return coords

    # Register it:
    CHALLENGE_HANDLERS = {
        # ... existing handlers ...
        'my-new-type': '_solve_my_new_type',
    }
```

---

## Daemon Mode — 12 Self-Healing Paths

The `daemon()` function in `pipeline.py` handles these failure modes automatically:

| Trigger | Recovery Action |
|---|---|
| IP flagged / rate-limited | Webshare API auto-rotate IP |
| Cloudflare DNS quota exceeded | CF DNS quota cleanup |
| tmpfs orphan processes | Orphan process reap |
| gost relay down | gost relay watchdog restart |
| DataDome slider challenge | Auto-drag slider synthesis |
| Stripe fingerprint drift | Runtime re-alignment |
| PayPal session expired | Re-authentication flow |
| hCaptcha solve failure | VLM → CLIP → platform fallback |
| Account batch-association ban | Delay + fresh identity |
| Codex OAuth token expired | PKCE refresh flow |
| Browser crash / hang | Camoufox process restart |
| Output file lock | Tmpfs rotation + re-open |

### Daemon Status Monitoring

```python
# pipeline.py exposes a status endpoint when --daemon is active
import requests

status = requests.get("http://localhost:8766/daemon/status").json()
# {
#   "active_workers": 3,
#   "completed_today": 12,
#   "alive_rate_24h": 0.02,
#   "current_ip": "x.x.x.x",
#   "last_success": "2026-04-30T12:00:00Z",
#   "healing_events": [...]
# }
```

---

## Reading Output

```python
import json

results = []
with open("output/results.jsonl") as f:
    for line in f:
        results.append(json.loads(line))

# Each result:
# {
#   "email": "user@subdomain.yourdomain.com",
#   "refresh_token": "...",
#   "subscription_type": "team",
#   "created_at": "2026-04-30T...",
#   "proxy_ip": "x.x.x.x",
#   "success": true
# }

successful = [r for r in results if r.get("success")]
print(f"Success rate: {len(successful)}/{len(results)}")
```

---

## WebUI API (when server is running)

```python
import requests

BASE = "http://127.0.0.1:8765"

# Check preflight / system health
health = requests.get(f"{BASE}/api/preflight").json()

# Start a single run via API
run = requests.post(f"{BASE}/api/run", json={
    "mode": "single",
    "subscription_type": "team"
}).json()
run_id = run["run_id"]

# Stream logs via SSE
import sseclient
response = requests.get(f"{BASE}/api/run/{run_id}/logs", stream=True)
client = sseclient.SSEClient(response)
for event in client.events():
    print(event.data)

# Stop a run
requests.post(f"{BASE}/api/run/{run_id}/stop")
```

---

## Troubleshooting

### Pipeline Hangs at PayPal OTP

```
# First run requires manual 2FA completion
# Run WITHOUT xvfb-run to see the browser:
python pipeline.py --config CTF-pay/config.paypal.json --paypal --no-headless
# Complete OTP manually; subsequent runs use saved session
```

### Stripe Fingerprint Drift

```bash
# Symptoms: Stripe returns 400 or challenge page unexpectedly
# CTF-pay/card.py contains runtime.version / js_checksum / rv_timestamp
# These drift every few weeks — check docs/debugging.md for realignment procedure

# Quick check: compare your values against a fresh mitmproxy capture
mitmproxy --mode transparent -p 8080 --set console_eventlog_verbosity=debug
```

### hCaptcha Solver Falling Back Constantly

```bash
# Check VLM endpoint is reachable
curl -H "Authorization: Bearer $VLM_API_KEY" \
     "$VLM_BASE_URL/models" | python -m json.tool

# Check CLIP venv is active when running
~/.venvs/ctfml/bin/python pipeline.py --config ...

# Enable verbose solver logging
export HCAPTCHA_DEBUG=1
```

### Low Survival Rate (~2%)

This is expected per the anti-fraud research. Key findings from `docs/anti-fraud-research.md`:

- **Batch-association delayed banning**: Accounts registered in the same batch are banned together ~12–24 hours after creation
- **IP-string-level fingerprinting**: Exact IP (not just subnet) is tracked
- **Probe layer vs ban layer separation**: Initial probe passes, ban fires later

Mitigation strategies documented in `docs/anti-fraud-research.md`:
- Use residential IPs, not datacenter
- Introduce timing jitter between registrations (daemon does this automatically)
- Avoid reusing Cloudflare subdomains across batches

### Free Account Path Broken

```
# Known limitation — OpenAI redirects free accounts to /add-phone
# No workaround without a real phone number
# Codex API audience mismatch with ChatGPT-Web access_token
# Only Plus/Team/Pro subscription paths are currently functional
```

### Common Error Messages

| Error | Cause | Fix |
|---|---|---|
| `PayPal region rejected` | Non-EU proxy | Switch to EU/IE proxy |
| `Turnstile solve timeout` | Browser fingerprint detected | Update Camoufox: `camoufox fetch` |
| `Stripe 3DS required` | Card requires 3DS auth | Use a non-3DS card config |
| `CF DNS quota exceeded` | Too many subdomain creates | Daemon auto-cleans; manual: see `docs/debugging.md` |
| `gost relay not responding` | gost process crashed | Daemon restarts; manual: `systemctl restart gost` |
| `Codex PKCE state mismatch` | Clock skew | `ntpdate -u pool.ntp.org` |

---

## Project Structure

```
Gpt-Agreement-Payment/
├── pipeline.py                    # Main entry point, daemon orchestrator
├── CTF-pay/
│   ├── card.py                    # Stripe Checkout replay (~8000 lines)
│   ├── hcaptcha_auto_solver.py    # hCaptcha visual solver (~4000 lines)
│   ├── config.paypal.example.json
│   └── config.auto.json           # Generated by webui wizard
├── CTF-reg/
│   ├── browser_register.py        # Camoufox + Turnstile registration
│   └── config.paypal-proxy.example.json
├── webui/
│   ├── server.py                  # FastAPI backend
│   ├── frontend/                  # React/pnpm frontend
│   └── README.md
├── output/
│   └── results.jsonl              # refresh_token output
└── docs/
    ├── anti-fraud-research.md     # Empirical data, 45-account 24h study
    ├── architecture.md
    ├── configuration.md
    ├── daemon-mode.md
    ├── debugging.md
    ├── hcaptcha-solver.md
    ├── installation.md
    └── operating-modes.md
```

---

## Key Timing Expectations

| Phase | Typical Duration |
|---|---|
| First-time config + PayPal 2FA | 1–3 hours |
| Single pipeline run (after setup) | ~5 minutes |
| WebUI wizard setup | ~15 minutes |
| Daemon stabilization | 30–60 minutes |
| Account survival window | 12–24 hours (2% survive 24h) |
