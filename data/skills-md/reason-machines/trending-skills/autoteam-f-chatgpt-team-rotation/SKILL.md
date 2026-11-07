---
name: autoteam-f-chatgpt-team-rotation
description: AutoTeam-F is a ChatGPT Team account rotation and authentication sync tool with batch free account generation, OAuth management, and a Web dashboard.
triggers:
  - set up AutoTeam-F for ChatGPT Team rotation
  - how do I batch generate free ChatGPT accounts
  - configure AutoTeam-F with Cloudflare temp email
  - rotate ChatGPT Team seats automatically
  - sync Codex OAuth tokens to CLIProxyAPI
  - deploy AutoTeam-F with Docker
  - fix 401 account_id error in AutoTeam
  - use AutoTeam-F web panel to manage accounts
---

# AutoTeam-F ChatGPT Team Rotation & Free Account Generation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

AutoTeam-F is a Python-based tool for automating ChatGPT Team account rotation, batch free Personal account generation, and Codex OAuth authentication sync to CLIProxyAPI (CPA). It uses Playwright for browser automation, FastAPI for the web backend, and Vue 3 for the dashboard.

**F = Fix + Free**: it fixes blocking bugs from the upstream [cnitlrt/AutoTeam](https://github.com/cnitlrt/AutoTeam) and adds batch free-account production.

---

## Installation

### Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) package manager
- A deployed [cloudflare_temp_email](https://github.com/dreamhunter2333/cloudflare_temp_email) instance (recommended mail backend)

### Linux
```bash
git clone https://github.com/ZRainbow1275/AutoTeam-F.git
cd AutoTeam-F
bash setup.sh
# setup.sh runs: uv sync && uv run playwright install chromium
```

### Windows / macOS
```bash
git clone https://github.com/ZRainbow1275/AutoTeam-F.git
cd AutoTeam-F
uv sync
uv run playwright install chromium
```

### Docker (recommended for production)
```bash
git clone https://github.com/ZRainbow1275/AutoTeam-F.git
cd AutoTeam-F
mkdir -p data && cp .env.example data/.env
# Edit data/.env with your configuration
docker compose up -d
```

---

## Configuration

Create a `.env` file (or `data/.env` for Docker). First-run wizard auto-generates it:

```bash
uv run autoteam api  # triggers guided setup on first run
```

### Key `.env` Variables

```dotenv
# Mail provider: cf_temp_email (default/recommended) or maillab
MAIL_PROVIDER=cf_temp_email
MAIL_BASE_URL=https://your-cf-temp-email.workers.dev

# If using maillab (upstream-compatible legacy)
# MAIL_PROVIDER=maillab
# MAIL_BASE_URL=https://your-cloudmail-instance.com

# OpenAI admin/master account
OPENAI_EMAIL=admin@example.com
OPENAI_PASSWORD=your_password

# CLIProxyAPI (CPA) sync target
CPA_BASE_URL=https://your-cpa-instance.com
CPA_API_KEY=$CPA_API_KEY

# AutoTeam-F API protection
API_KEY=$AUTOTEAM_API_KEY

# Team workspace settings
TEAM_WORKSPACE_ID=your_workspace_id
TARGET_MEMBER_COUNT=5

# Reconcile behavior
RECONCILE_KICK_ORPHAN=false
RECONCILE_KICK_GHOST=false
```

### Mail Provider Notes
- **`cf_temp_email`** (default): Cloudflare Workers-based, widely tested, good OpenAI domain allowlist compatibility
- **`maillab`**: Legacy `maillab/cloud-mail` backend; must be set explicitly — no longer the default
- On startup, AutoTeam-F fingerprint-sniffs the base URL and warns if provider/URL mismatch is detected (prevents silent "login success → create mailbox 401" failures)

---

## CLI Commands

```bash
# Start Web dashboard + API (port 8787)
uv run autoteam api

# Smart rotation — fill to N active accounts (default: 5)
uv run autoteam rotate [N]

# View account status
uv run autoteam status

# Check quotas (active accounts)
uv run autoteam check

# Check quotas including standby pool (rate-limited, 24h dedup)
uv run autoteam check --include-standby

# Add a new account via automated registration
uv run autoteam add

# Add account via manual OAuth paste
uv run autoteam manual-add

# Fill Team seats to target count
uv run autoteam fill [N]

# Clean up excess Team members
uv run autoteam cleanup [N]

# Sync local auth to CPA
uv run autoteam sync

# Pull auth from CPA to local
uv run autoteam pull-cpa

# Admin login (master account)
uv run autoteam admin-login

# Reconcile workspace vs local — find ghost/orphan/mismatched accounts
uv run autoteam reconcile
uv run autoteam reconcile --dry-run
```

---

## Web Dashboard

Access at `http://localhost:8787` after starting with `uv run autoteam api`.

| Page | Key Features |
|------|-------------|
| 📊 Dashboard | Account stats, status table, login/kick/delete/bulk-delete |
| 👥 Team Members | All workspace members including external |
| 🔁 Pool Operations | Rotate / Check / Fill / Add / **Generate Free Accounts** / Cleanup |
| 🔄 Sync Center | Sync accounts, push to CPA, pull from CPA |
| 🔐 OAuth Login | Generate auth links; auto localhost callback + manual paste fallback |
| 📜 Task History | Background task status + real-time stop button |
| 📋 Logs | Live log viewer |
| ⚙️ Settings | Admin login, master Codex sync, patrol config |

---

## REST API

All endpoints require `Authorization: Bearer $API_KEY` header.

### Account Management

```bash
# List all accounts
curl -H "Authorization: Bearer $API_KEY" http://localhost:8787/api/accounts

# Trigger rotation (fill to 5 active)
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": 5}' \
  http://localhost:8787/api/tasks/rotate

# Generate free Personal accounts (leave_workspace=true)
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": 3, "leave_workspace": true}' \
  http://localhost:8787/api/tasks/fill

# Check quotas including standby
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"include_standby": true}' \
  http://localhost:8787/api/tasks/check

# Sync to CPA
curl -X POST -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/tasks/sync

# Pull from CPA
curl -X POST -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/tasks/pull-cpa
```

### Diagnostics & Repair

```bash
# Diagnose 401 issues (checks 4 API endpoints)
curl -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/admin/diagnose | jq

# Hot-fix mismatched account_id without re-login
curl -X POST -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/admin/fix-account-id | jq

# Reconcile workspace vs local accounts (dry run)
curl -X POST -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8787/api/admin/reconcile?dry_run=1" | jq

# Stop a running task
curl -X POST -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/tasks/{task_id}/stop
```

### OAuth Flow

```bash
# Get OAuth URL for an account
curl -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/oauth/url

# Submit manually-obtained OAuth callback URL
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"callback_url": "http://localhost:..."}' \
  http://localhost:8787/api/oauth/manual
```

---

## Key Workflows

### 1. Batch Generate Free Personal Accounts

The "F" in AutoTeam-F's key feature: register accounts → master invites to Team → accounts leave workspace → Personal OAuth stored.

Via Web: Dashboard → "账号池操作" → "生成免费号" → set count → start.

Via API:
```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": 5, "leave_workspace": true}' \
  http://localhost:8787/api/tasks/fill
```

**Constraints**: `baseline + new_batch ≤ 4` (Team seat limit). AutoTeam-F auto-shrinks the batch if exceeded.

### 2. Smart Rotation

Accounts with exhausted Codex quota are moved to `standby`. When standby accounts recover quota, they're promoted back to `active` before registering new ones.

```bash
uv run autoteam rotate 5
# Equivalent API:
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": 5}' \
  http://localhost:8787/api/tasks/rotate
```

### 3. Fix 401 "Must be part of this workspace"

```bash
API_KEY="$(grep '^API_KEY' .env | cut -d= -f2)"

# Step 1: Diagnose
curl -s -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/admin/diagnose | jq

# Step 2: Hot-fix account_id (no re-login needed)
curl -s -X POST -H "Authorization: Bearer $API_KEY" \
  http://localhost:8787/api/admin/fix-account-id | jq
```

### 4. Reconcile Ghost/Orphan Accounts

Identifies: orphaned seats (workspace has seat, no local auth), mismatched accounts, exhausted-but-not-abandoned, ghost accounts.

```bash
# Safe dry run first
uv run autoteam reconcile --dry-run

# Apply fixes (behavior controlled by RECONCILE_KICK_ORPHAN / RECONCILE_KICK_GHOST in .env)
uv run autoteam reconcile
```

### 5. CPA Bidirectional Sync

```bash
# Push local active accounts → CPA
uv run autoteam sync

# Pull CPA accounts → local (import external auth)
uv run autoteam pull-cpa
```

---

## Account State Machine

```
registered → active → standby → (recover) → active
                   ↘ (exhausted, no recovery) → abandoned
                   
standby: quota exhausted, waiting for recovery
active: has valid Codex quota
auth_invalid: 401/403 on check → needs re-OAuth
network_error: transient DNS/timeout/5xx → retried next cycle (not marked invalid)
```

**Failure log**: Registration failures are persisted to `register_failures.json` with categories: `phone_required`, `duplicate`, `kick_failed`, `oauth_failed`.

---

## Python Integration Examples

### Check Account Status Programmatically

```python
import httpx
import os

API_KEY = os.environ["AUTOTEAM_API_KEY"]
BASE_URL = "http://localhost:8787"

headers = {"Authorization": f"Bearer {API_KEY}"}

with httpx.Client() as client:
    # Get all accounts
    accounts = client.get(f"{BASE_URL}/api/accounts", headers=headers).json()
    
    active = [a for a in accounts if a["status"] == "active"]
    standby = [a for a in accounts if a["status"] == "standby"]
    
    print(f"Active: {len(active)}, Standby: {len(standby)}")

    # Trigger rotation if below threshold
    if len(active) < 3:
        resp = client.post(
            f"{BASE_URL}/api/tasks/rotate",
            headers=headers,
            json={"target": 5}
        )
        task = resp.json()
        print(f"Rotation task started: {task['task_id']}")
```

### Poll Task Until Complete

```python
import httpx
import time
import os

API_KEY = os.environ["AUTOTEAM_API_KEY"]
BASE_URL = "http://localhost:8787"
headers = {"Authorization": f"Bearer {API_KEY}"}

def run_task_and_wait(endpoint: str, payload: dict, timeout: int = 600) -> dict:
    with httpx.Client(timeout=30) as client:
        resp = client.post(
            f"{BASE_URL}/api/tasks/{endpoint}",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
        task_id = resp.json()["task_id"]
        
        deadline = time.time() + timeout
        while time.time() < deadline:
            status = client.get(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers=headers
            ).json()
            
            if status["state"] in ("completed", "failed", "stopped"):
                return status
            
            time.sleep(5)
        
        raise TimeoutError(f"Task {task_id} did not complete in {timeout}s")

# Generate 3 free personal accounts
result = run_task_and_wait("fill", {"target": 3, "leave_workspace": True})
print(f"Task result: {result['state']}, accounts: {result.get('result')}")
```

### Export Codex CLI Auth

```python
import httpx
import json
import os

API_KEY = os.environ["AUTOTEAM_API_KEY"]
BASE_URL = "http://localhost:8787"
headers = {"Authorization": f"Bearer {API_KEY}"}

with httpx.Client() as client:
    resp = client.get(f"{BASE_URL}/api/auth/export", headers=headers)
    auth_data = resp.json()

# Write Codex CLI format
with open(os.path.expanduser("~/.codex/auth.json"), "w") as f:
    json.dump(auth_data, f, indent=2)

print("Auth exported to ~/.codex/auth.json")
```

---

## Docker Compose Reference

```yaml
# docker-compose.yml (from repo)
services:
  autoteam:
    build: .
    ports:
      - "8787:8787"
    volumes:
      - ./data:/app/data
    environment:
      - DATA_DIR=/app/data
    restart: unless-stopped
```

```bash
# Start
docker compose up -d

# View logs
docker compose logs -f autoteam

# Run CLI commands inside container
docker compose exec autoteam uv run autoteam status
docker compose exec autoteam uv run autoteam reconcile --dry-run

# Restart after config change
docker compose restart autoteam
```

**Linux host access**: If CPA or mail service runs on the host, use `host.docker.internal` (Docker Desktop) or the host's bridge IP (`172.17.0.1` typically) instead of `localhost` in `.env`.

---

## Troubleshooting

### 401 "Must be part of this workspace"
Most common cause: `account_id` stored locally doesn't match OpenAI's records.
```bash
API_KEY="$(grep '^API_KEY' data/.env | cut -d= -f2)"
curl -s -H "Authorization: Bearer $API_KEY" http://localhost:8787/api/admin/diagnose | jq
curl -s -X POST -H "Authorization: Bearer $API_KEY" http://localhost:8787/api/admin/fix-account-id | jq
```

### Mail provider mismatch warning on startup
```
WARNING: MAIL_PROVIDER=cf_temp_email but base_url fingerprint suggests maillab protocol
```
Fix: ensure `MAIL_PROVIDER` in `.env` matches your actual deployed mail service. `cf_temp_email` uses Cloudflare Workers API; `maillab` uses the cloud-mail REST API.

### Registration fails with `phone_required`
OpenAI began requiring phone verification for some IPs. Use a residential proxy. Check `register_failures.json` for categorized failure counts.

### Playwright times out during registration
```bash
# Increase timeout — edit .env
PLAYWRIGHT_TIMEOUT=120000  # ms, default 60000
```
Common on high-latency VPS. Consider residential proxy.

### Standby accounts never recover
AutoTeam-F uses 24h dedup for standby quota checks to avoid rate-limits. Force a check:
```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"include_standby": true}' \
  http://localhost:8787/api/tasks/check
```

### Personal accounts invalidated after master account ban
This is a known limitation — personal accounts derived from a banned master account (via Team invite → leave → personal OAuth) will also become invalid. The accounts must be regenerated from a new master account.

### Task stop is soft, not immediate
Clicking "Stop Task" completes the current account registration (~2 min) before exiting. This is by design to avoid half-registered accounts. The task will show `stopping` then `stopped`.

### `autoteam fill` batch auto-shrinks
Team seats are capped: `baseline + new_batch ≤ 4`. AutoTeam-F auto-reduces batch size. To generate more, run multiple fill cycles after previous accounts have left the workspace.

---

## Project Structure

```
AutoTeam-F/
├── autoteam/           # Core Python package
│   ├── api/            # FastAPI routes
│   ├── core/           # Account manager, rotation logic
│   ├── playwright_/    # Browser automation (register, OAuth, Codex)
│   ├── mail/           # cf_temp_email + maillab backends
│   └── cli.py          # CLI entry points
├── frontend/           # Vue 3 dashboard source
├── data/               # Runtime data (gitignored)
│   ├── accounts.json   # Account pool state
│   ├── register_failures.json  # Failure analytics
│   └── .env            # Configuration
├── docs/               # Extended documentation
├── docker-compose.yml
└── setup.sh
```

---

## Links

- [From-Zero Deploy Guide](docs/getting-started.md)
- [Configuration Reference](docs/configuration.md)
- [Docker Deployment](docs/docker.md)
- [API Reference](docs/api.md)
- [Architecture & State Machine](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Upstream: cnitlrt/AutoTeam](https://github.com/cnitlrt/AutoTeam)
- [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)
- [cloudflare_temp_email](https://github.com/dreamhunter2333/cloudflare_temp_email)
