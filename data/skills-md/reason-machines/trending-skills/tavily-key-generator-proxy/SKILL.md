---
name: tavily-key-generator-proxy
description: Auto batch-register Tavily API keys via browser automation and pool them behind a unified proxy gateway with web console
triggers:
  - tavily api key generator
  - batch register tavily accounts
  - tavily key pool proxy
  - automate tavily registration
  - tavily api proxy gateway
  - rotate tavily api keys
  - tavily capsolver automation
  - bulk tavily api keys
---

# Tavily Key Generator + API Proxy

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

Automates bulk Tavily account registration using Playwright + CapSolver (Cloudflare Turnstile), then pools the resulting API keys behind a unified proxy gateway with round-robin rotation, usage tracking, token management, and a web console.

---

## What It Does

| Component | Location | Purpose |
|-----------|----------|---------|
| **Key Generator** | root `/` | Playwright-driven headless Firefox registers Tavily accounts, solves Turnstile CAPTCHAs, verifies email, extracts API key |
| **API Proxy** | `proxy/` | FastAPI service that round-robins requests across pooled keys, exposes `/api/search` and `/api/extract`, serves web console at `/console` |

Each free Tavily account yields **1,000 API calls/month**. The proxy aggregates quota: 10 keys = 10,000 calls/month via one endpoint.

---

## Installation

### Key Generator

```bash
git clone https://github.com/skernelx/tavily-key-generator.git
cd tavily-key-generator
pip install -r requirements.txt
playwright install firefox
cp config.example.py config.py
# Edit config.py with your CapSolver key and email backend
python main.py
```

### API Proxy (Docker — recommended)

```bash
cd proxy/
cp .env.example .env
# Set ADMIN_PASSWORD in .env
docker compose up -d
# Console at http://localhost:9874/console
```

---

## Configuration (`config.py`)

### CAPTCHA Solver (required)

```python
# CapSolver — recommended (~$0.001/solve, high success rate)
CAPTCHA_SOLVER = "capsolver"
CAPSOLVER_API_KEY = "CAP-..."   # from capsolver.com

# Browser click fallback — free but low success rate
CAPTCHA_SOLVER = "browser"
```

### Email Backend (required — pick one)

**Option A: Cloudflare Email Worker (self-hosted, free)**

```python
EMAIL_BACKEND = "cloudflare"
EMAIL_DOMAIN = "mail.yourdomain.com"
EMAIL_API_URL = "https://mail.yourdomain.com"
EMAIL_API_TOKEN = "your-worker-token"
```

**Option B: DuckMail (third-party temporary email)**

```python
EMAIL_BACKEND = "duckmail"
DUCKMAIL_API_BASE = "https://api.duckmail.sbs"
DUCKMAIL_BEARER = "dk_..."
DUCKMAIL_DOMAIN = "duckmail.sbs"
```

If both backends are configured, the CLI prompts you to choose at runtime.

### Registration Throttle (anti-ban)

```python
THREADS = 2                  # Max 3 — more = higher ban risk
COOLDOWN_BASE = 45           # Seconds between registrations
COOLDOWN_JITTER = 15         # Random additional seconds
BATCH_LIMIT = 20             # Pause after this many registrations
```

### Auto-upload to Proxy (optional)

```python
PROXY_AUTO_UPLOAD = True
PROXY_URL = "http://localhost:9874"
PROXY_ADMIN_PASSWORD = "your-admin-password"
```

---

## Running the Key Generator

```bash
python main.py
# Prompts: how many keys to generate, which email backend
# Output: api_keys.md with all generated keys
# If PROXY_AUTO_UPLOAD=True, keys are pushed to proxy automatically
```

Generated `api_keys.md` format (used for bulk import into proxy):

```
tvly-abc123...
tvly-def456...
tvly-ghi789...
```

---

## API Proxy Usage

### Calling the Proxy (drop-in Tavily replacement)

```bash
# Search — replace base URL only
curl -X POST http://your-server:9874/api/search \
  -H "Authorization: Bearer tvly-YOUR_PROXY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "latest AI news", "search_depth": "basic"}'

# Extract
curl -X POST http://your-server:9874/api/extract \
  -H "Authorization: Bearer tvly-YOUR_PROXY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/article"]}'
```

Token can also be passed in the request body as `api_key` (Tavily SDK compatible):

```python
import requests

response = requests.post(
    "http://your-server:9874/api/search",
    json={
        "query": "Python web scraping",
        "api_key": "tvly-YOUR_PROXY_TOKEN"
    }
)
print(response.json())
```

### Python SDK Integration

```python
from tavily import TavilyClient

# Point SDK at your proxy — no other changes needed
client = TavilyClient(
    api_key="tvly-YOUR_PROXY_TOKEN",
    base_url="http://your-server:9874"
)

results = client.search("machine learning trends 2025")
```

---

## Admin API Reference

All admin endpoints require header: `X-Admin-Password: your-password`

### Keys Management

```bash
# List all keys
curl http://localhost:9874/api/keys \
  -H "X-Admin-Password: secret"

# Add a single key
curl -X POST http://localhost:9874/api/keys \
  -H "X-Admin-Password: secret" \
  -H "Content-Type: application/json" \
  -d '{"key": "tvly-abc123..."}'

# Bulk import from api_keys.md text
curl -X POST http://localhost:9874/api/keys \
  -H "X-Admin-Password: secret" \
  -H "Content-Type: application/json" \
  -d '{"bulk": "tvly-abc...\ntvly-def...\ntvly-ghi..."}'

# Toggle key enabled/disabled
curl -X PUT http://localhost:9874/api/keys/{id}/toggle \
  -H "X-Admin-Password: secret"

# Delete key
curl -X DELETE http://localhost:9874/api/keys/{id} \
  -H "X-Admin-Password: secret"
```

### Token Management

```bash
# Create access token
curl -X POST http://localhost:9874/api/tokens \
  -H "X-Admin-Password: secret" \
  -H "Content-Type: application/json" \
  -d '{"label": "my-app"}'
# Returns: {"token": "tvly-...", "id": "..."}

# List tokens
curl http://localhost:9874/api/tokens \
  -H "X-Admin-Password: secret"

# Delete token
curl -X DELETE http://localhost:9874/api/tokens/{id} \
  -H "X-Admin-Password: secret"
```

### Stats

```bash
curl http://localhost:9874/api/stats \
  -H "X-Admin-Password: secret"
# Returns: total_quota, used, remaining, active_keys, disabled_keys
```

### Change Admin Password

```bash
curl -X PUT http://localhost:9874/api/password \
  -H "X-Admin-Password: current-password" \
  -H "Content-Type: application/json" \
  -d '{"new_password": "new-secure-password"}'
```

---

## Proxy Behavior

- **Round-robin**: requests distributed evenly across active keys
- **Auto-disable**: key disabled after 3 consecutive failures
- **Quota tracking**: total = active_keys × 1,000/month; updates automatically on add/delete/toggle
- **Token format**: proxy tokens use `tvly-` prefix, indistinguishable from real Tavily keys to clients

---

## Proxy `.env` Configuration

```env
ADMIN_PASSWORD=change-this-immediately
PORT=9874
# Optional: restrict CORS origins
CORS_ORIGINS=https://myapp.com,https://app2.com
```

---

## Nginx Reverse Proxy + HTTPS

```nginx
server {
    listen 443 ssl;
    server_name tavily-proxy.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:9874;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Integration Pattern: Auto-replenish Pool

```python
# replenish.py — run on cron when quota runs low
import requests

PROXY_URL = "http://localhost:9874"
ADMIN_PASSWORD = "your-password"
MIN_ACTIVE_KEYS = 10

def get_stats():
    r = requests.get(f"{PROXY_URL}/api/stats",
                     headers={"X-Admin-Password": ADMIN_PASSWORD})
    return r.json()

def trigger_registration(count: int):
    """Call your key generator as subprocess or import directly"""
    import subprocess
    subprocess.run(["python", "main.py", "--count", str(count)], check=True)

stats = get_stats()
active = stats["active_keys"]
if active < MIN_ACTIVE_KEYS:
    needed = MIN_ACTIVE_KEYS - active
    print(f"Pool low ({active} keys), registering {needed} more...")
    trigger_registration(needed)
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| CAPTCHA solve failures | Tavily elevated bot detection | Pause several hours, reduce `THREADS` to 1 |
| Email verification timeout | Slow email delivery | Increase poll timeout in config |
| Keys immediately disabled in proxy | Tavily account flagged/suspended | Register from different IP |
| `playwright install firefox` fails | Missing system deps | Run `playwright install-deps firefox` first |
| Docker compose port conflict | 9874 in use | Change `PORT` in `.env` and `docker-compose.yml` |
| `X-Admin-Password` 401 | Wrong password | Check `.env`, restart container after changes |
| IP ban during registration | Too many registrations | Use `BATCH_LIMIT=10`, wait hours between batches |

### Rate Limit Safe Settings

```python
# Conservative — minimizes ban risk
THREADS = 1
COOLDOWN_BASE = 60
COOLDOWN_JITTER = 30
BATCH_LIMIT = 10
```

---

## Security Checklist

- [ ] Change `ADMIN_PASSWORD` from default immediately after deploy
- [ ] Add `config.py` to `.gitignore` (already included, verify before push)
- [ ] Deploy behind HTTPS in production
- [ ] Rotate proxy tokens periodically
- [ ] Never commit `api_keys.md` to public repositories
