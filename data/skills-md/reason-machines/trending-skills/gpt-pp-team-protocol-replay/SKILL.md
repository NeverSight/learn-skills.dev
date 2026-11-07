---
name: gpt-pp-team-protocol-replay
description: End-to-end protocol replay toolkit for ChatGPT Team subscription with hCaptcha solver and anti-fraud research tools
triggers:
  - replay ChatGPT Team subscription protocol
  - solve hCaptcha automatically with VLM
  - run pipeline for ChatGPT account automation
  - configure PayPal billing with Stripe replay
  - set up daemon mode for account pool maintenance
  - debug anti-fraud mechanisms for ChatGPT
  - use gpt-pp-team for bug bounty research
  - configure hcaptcha solver with OpenAI VLM
---

# gpt-pp-team Protocol Replay Toolkit

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

End-to-end protocol replay toolkit for ChatGPT Team subscription covering `Stripe Checkout → PayPal billing agreement → ChatGPT manual-approval → Codex OAuth + PKCE`. Includes a from-scratch hCaptcha visual solver (12 challenge types) and empirical anti-fraud research data.

> ⚠️ **For authorized security research, CTF, and bug bounty in-scope assets only.** Read `NOTICE` before use.

---

## Installation

```bash
git clone https://github.com/DanOps-1/gpt-pp-team
cd gpt-pp-team
pip install requests curl_cffi playwright camoufox browserforge mitmproxy pybase64
playwright install firefox
camoufox fetch
```

### ML dependencies for hCaptcha solver (separate venv, ~4 GB)

```bash
python -m venv ~/.venvs/ctfml
~/.venvs/ctfml/bin/pip install torch transformers opencv-python pillow numpy
```

### System requirements

- Linux with Xvfb (for headless browser automation)
- ~5 GB disk, ~2 GB RAM minimum
- EU/US proxy (PayPal region-locked, Stripe country-locked)
- Cloudflare zone for catch-all subdomain email registration

---

## Architecture Overview

```
pipeline.py
  └─> CTF-reg/browser_register.py   (Camoufox + Turnstile)
  └─> CTF-pay/card.py               (Stripe Checkout replay, 8000 lines)
  └─> Stripe confirm + ChatGPT /approve
  └─> Camoufox PayPal billing agreement
  └─> Stripe poll state=succeeded
  └─> Camoufox second login Codex OAuth + PKCE
  └─> output/results.jsonl          (refresh_token)
```

Key files:
| File | Purpose |
|------|---------|
| `pipeline.py` | Orchestrator, daemon loop, 12-self-healing branches |
| `CTF-pay/card.py` | Stripe protocol replay (single file, 8000 lines) |
| `CTF-pay/hcaptcha_auto_solver.py` | hCaptcha VLM solver (~4000 lines, standalone) |
| `CTF-reg/browser_register.py` | Account registration with Camoufox |
| `webui/server.py` | 14-step setup wizard + SSE log controller |

---

## Configuration

### Copy templates

```bash
cp CTF-pay/config.paypal.example.json     CTF-pay/config.paypal.json
cp CTF-reg/config.paypal-proxy.example.json   CTF-reg/config.paypal-proxy.json
```

### Core config fields (`CTF-pay/config.paypal.json`)

```json
{
  "proxy": {
    "host": "your-proxy-host",
    "port": 1080,
    "username": "$PROXY_USER",
    "password": "$PROXY_PASS",
    "protocol": "socks5"
  },
  "paypal": {
    "email": "$PAYPAL_EMAIL",
    "password": "$PAYPAL_PASSWORD",
    "country": "IE"
  },
  "cloudflare": {
    "api_token": "$CF_API_TOKEN",
    "zone_id": "$CF_ZONE_ID",
    "domain": "yourdomain.com"
  },
  "vlm": {
    "api_key": "$VLM_API_KEY",
    "base_url": "$VLM_BASE_URL",
    "model": "gpt-4o"
  },
  "captcha_platform": {
    "api_key": "$CAPTCHA_API_KEY",
    "provider": "2captcha"
  },
  "webshare": {
    "api_key": "$WEBSHARE_API_KEY"
  }
}
```

### Environment variables

```bash
export PROXY_USER="your_proxy_username"
export PROXY_PASS="your_proxy_password"
export PAYPAL_EMAIL="your@paypal.com"
export PAYPAL_PASSWORD="your_paypal_password"
export CF_API_TOKEN="your_cloudflare_api_token"
export CF_ZONE_ID="your_cloudflare_zone_id"
export VLM_API_KEY="your_openai_compatible_key"
export VLM_BASE_URL="https://api.openai.com/v1"
export WEBSHARE_API_KEY="your_webshare_key"
export CAPTCHA_API_KEY="your_2captcha_key"
```

---

## WebUI Setup Wizard (Recommended for First-Time Setup)

Reduces ~3 hour manual config to ~15 minutes. Generates both config files automatically.

```bash
# Install backend deps
pip install -r webui/requirements.txt

# Build frontend (one-time)
cd webui/frontend && pnpm i && pnpm build && cd ../..

# Start wizard
python -m webui.server
# Open http://127.0.0.1:8765 — redirects to /setup on first visit
```

Features:
- 14-step configuration wizard
- Real-time preflight self-checks
- SSE log streaming for live pipeline monitoring
- Generates `CTF-pay/config.auto.json` + `CTF-reg/config.paypal-proxy.json`

For public access via nginx reverse proxy, see `webui/README.md`.

---

## Running the Pipeline

### Single run

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal
```

### Daemon mode (continuous pool maintenance)

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal \
  --daemon
```

### Batch mode

```bash
xvfb-run -a python pipeline.py \
  --config CTF-pay/config.paypal.json \
  --paypal \
  --batch 10
```

### Output

Results written to `output/results.jsonl`:
```json
{"email": "user@subdomain.yourdomain.com", "refresh_token": "...", "timestamp": "2026-04-29T00:00:00Z", "status": "success"}
```

---

## hCaptcha Solver — Standalone Usage

The solver (`CTF-pay/hcaptcha_auto_solver.py`) is independently usable with a 3-layer decision architecture:

1. **VLM primary path** — OpenAI-compatible vision model identifies challenge targets
2. **CLIP/OpenCV heuristic fallback** — local model, no API needed
3. **Human action synthesis** — Playwright realistic mouse movement

### Basic usage

```python
import asyncio
from CTF-pay.hcaptcha_auto_solver import HCaptchaSolver

async def solve_captcha(page):
    solver = HCaptchaSolver(
        page=page,
        vlm_api_key=os.environ["VLM_API_KEY"],
        vlm_base_url=os.environ["VLM_BASE_URL"],
        vlm_model="gpt-4o",
        clip_venv_path=os.path.expanduser("~/.venvs/ctfml"),
        debug=True
    )
    result = await solver.solve()
    return result  # True if solved, False if failed

asyncio.run(solve_captcha(page))
```

### With Playwright + Camoufox

```python
import asyncio
from camoufox.async_api import AsyncCamoufox
from CTF_pay.hcaptcha_auto_solver import HCaptchaSolver

async def main():
    async with AsyncCamoufox(headless=True, humanize=True) as browser:
        page = await browser.new_page()
        await page.goto("https://example.com/page-with-hcaptcha")
        
        solver = HCaptchaSolver(
            page=page,
            vlm_api_key=os.environ["VLM_API_KEY"],
            vlm_base_url=os.environ.get("VLM_BASE_URL", "https://api.openai.com/v1"),
            vlm_model="gpt-4o",
        )
        
        success = await solver.solve()
        if success:
            print("hCaptcha solved successfully")
        else:
            print("Solver failed, check logs")

asyncio.run(main())
```

### Supported challenge types (12)

- Image classification (single/multi-select)
- Bounding box / area selection
- Drag-and-drop alignment
- 3D object rotation
- Text-in-image matching
- Spatial relationship challenges
- Count-based selection
- Sequential ordering
- Color/pattern matching
- Object pair matching
- Scene classification
- Entity attribute verification

### CLIP-only mode (no VLM API)

```python
solver = HCaptchaSolver(
    page=page,
    vlm_api_key=None,          # Disables VLM primary path
    clip_venv_path=os.path.expanduser("~/.venvs/ctfml"),
    fallback_only=True
)
```

---

## Daemon Mode — 12-Self-Healing Branches

`pipeline.py::daemon()` handles these failure conditions automatically:

| Branch | Trigger | Recovery |
|--------|---------|----------|
| IP rotation | Ban detected / probe fail | Webshare API fetch new IP |
| CF DNS quota | Zone record limit hit | Clean stale catch-all records |
| tmpfs orphan | Crashed browser profile left | Reclaim tmpfs mounts |
| gost relay | Relay process died | Restart watchdog |
| DataDome slider | Slider CAPTCHA on registration | Auto-drag synthesis |
| PayPal 2FA | Session expired | Re-authenticate flow |
| Stripe fingerprint | `runtime.version` drift | Re-align JS checksum |
| Batch correlation | Mass ban detected | Pause + stagger restart |
| DNS propagation | New subdomain not resolving | Poll + retry with backoff |
| OAuth PKCE | Token exchange failure | Regenerate challenge |
| Account approval | Manual approval queue | Poll `/approve` endpoint |
| Memory pressure | Browser OOM | Graceful restart with GC |

---

## Anti-Fraud Research Data

Key empirical findings from `docs/anti-fraud-research.md`:

- **24-hour survival rate**: ~2% across 45 test accounts
- **Mechanism**: Batch correlation — accounts registered in same IP/time window get delayed mass ban
- **Probe vs ban layer separation**: Initial probe passes, ban fires 6–18 hours later
- **IP fingerprinting**: String-level exact match, not subnet-level

```python
# Access research data programmatically
import json

with open("docs/anti-fraud-research.md") as f:
    # Raw markdown with embedded JSON samples
    content = f.read()

# Survival curve model (from research):
# P(survival at t hours) ≈ 0.85 * exp(-0.31 * t) for batch size > 5
# P(survival at t hours) ≈ 0.60 * exp(-0.08 * t) for batch size == 1
```

---

## Protocol Chain — Key Endpoints

Documented from packet capture (`mitmproxy` intercept):

```
POST https://checkout.stripe.com/pay/{session_id}
  → Stripe payment intent confirm

POST https://api.openai.com/dashboard/billing/stripe/confirm
  → ChatGPT billing linkage

GET  https://api.openai.com/dashboard/billing/subscription/approve?token={t}
  → Manual approval poll

POST https://www.paypal.com/agreements/approve
  → PayPal billing agreement

GET  https://auth.openai.com/authorize
  → Codex OAuth + PKCE initiation

POST https://auth.openai.com/oauth/token
  → refresh_token exchange
```

---

## Stripe Runtime Fingerprint Maintenance

`card.py` embeds Stripe JS runtime fingerprints that drift every few weeks:

```python
# In CTF-pay/card.py — fields to re-align after Stripe updates:
STRIPE_RUNTIME = {
    "runtime_version": "5.104.0",   # Check stripe.js version
    "js_checksum": "sha256-...",     # Recompute from live stripe.js
    "rv_timestamp": 1714000000,      # Update to current epoch
}

# To re-capture current values:
# 1. Open browser devtools on any Stripe Checkout page
# 2. Network tab → filter "stripe" → find runtime init request
# 3. Extract from request payload or JS source
```

---

## Debugging

### Common failures

**`PayPal OTP loop`** — First run requires manual 2FA:
```bash
# Run without --daemon first, complete OTP manually
xvfb-run -a python pipeline.py --config CTF-pay/config.paypal.json --paypal --interactive
```

**`hCaptcha VLM timeout`** — VLM API unreachable:
```bash
# Test VLM connectivity
python -c "
import openai, os
client = openai.OpenAI(api_key=os.environ['VLM_API_KEY'], base_url=os.environ.get('VLM_BASE_URL'))
print(client.models.list())
"
```

**`Stripe fingerprint mismatch`** — Protocol drift:
```bash
# Check card.py STRIPE_RUNTIME block, compare to live stripe.js
# Use mitmproxy to capture fresh values:
mitmproxy --mode upstream:http://your-proxy:1080 -s CTF-pay/capture_stripe.py
```

**`CF DNS quota exceeded`**:
```bash
# Manual cleanup
python -c "
import requests, os
headers = {'Authorization': f'Bearer {os.environ[\"CF_API_TOKEN\"]}'}
r = requests.get(f'https://api.cloudflare.com/client/v4/zones/{os.environ[\"CF_ZONE_ID\"]}/dns_records?per_page=100', headers=headers)
print(f'Record count: {len(r.json()[\"result\"])}')
"
```

**`Camoufox not found`**:
```bash
camoufox fetch
python -c "from camoufox.async_api import AsyncCamoufox; print('OK')"
```

### Artifact paths

```
output/results.jsonl          # Successful refresh_tokens
output/failed/                # Per-attempt failure dumps
output/screenshots/           # Browser screenshots at failure point
output/mitmproxy-*.har        # Protocol capture (if enabled)
/tmp/ctf-*/                   # tmpfs browser profiles (cleaned by daemon)
```

### Enable verbose logging

```bash
export CTF_DEBUG=1
export CTF_SCREENSHOT_ON_ERROR=1
xvfb-run -a python pipeline.py --config CTF-pay/config.paypal.json --paypal --verbose
```

---

## Contributing

Priority contributions (by impact):
1. New hCaptcha challenge type solvers — provide `round.json` with challenge data + solution
2. Protocol adaptations when Stripe/PayPal/OpenAI break — include packet capture diff
3. New daemon self-healing branches — include trigger log + recovery log
4. Anti-fraud empirical data — follow anonymization pattern in existing research doc

PR requirements (no evidence = auto-close):
- Solver PRs: `round.json` with challenge rounds
- Protocol PRs: packet capture before/after comparison
- Daemon PRs: trigger log + successful recovery log

---

## Legal Boundary

**Permitted:** Systems you own, legitimate CTF competitions, authorized bug bounty in-scope assets, security research with platform permission.

**Prohibited:** Fraud, payment circumvention, bulk account resale, ToS violations, unauthorized targets.

Full terms: `NOTICE` file in repo root. MIT license applies to code; `NOTICE` governs usage rights.
