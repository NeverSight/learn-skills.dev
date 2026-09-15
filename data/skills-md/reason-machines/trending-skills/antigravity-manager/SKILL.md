---
name: antigravity-manager
description: AI coding agent skill for Antigravity Manager — a Tauri v2 + Rust desktop app and Docker service that manages multiple Google/Anthropic accounts and proxies them as standard OpenAI/Anthropic/Gemini API endpoints with intelligent account rotation.
triggers:
  - "set up antigravity manager"
  - "configure antigravity tools proxy"
  - "use antigravity for claude code"
  - "add accounts to antigravity manager"
  - "antigravity api proxy setup"
  - "rotate google accounts with antigravity"
  - "antigravity docker deployment"
  - "connect claude code to antigravity"
---

# Antigravity Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Antigravity Manager is a professional AI account manager and proxy gateway. It takes Google (Gemini) and Anthropic (Claude) web session tokens and exposes them as standard API endpoints (OpenAI-compatible, Anthropic-native, and Gemini-native formats) with intelligent multi-account rotation, quota tracking, and automatic failover.

**Key capabilities:**
- Multi-account management with real-time quota dashboards
- Protocol conversion: web sessions → OpenAI / Anthropic / Gemini API
- Auto-rotation on 429/401 errors (millisecond failover)
- Model routing and remapping
- Desktop app (Tauri v2 + React + Rust) or headless Docker/server mode

---

## Installation

### Option A: One-line script (Linux/macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/lbjlaq/Antigravity-Manager/v4.1.30/install.sh | bash
```

Install a specific version:
```bash
curl -fsSL https://raw.githubusercontent.com/lbjlaq/Antigravity-Manager/v4.1.30/install.sh | bash -s -- --version 4.1.30
```

Dry run (preview without installing):
```bash
curl -fsSL https://raw.githubusercontent.com/lbjlaq/Antigravity-Manager/v4.1.30/install.sh | bash -s -- --dry-run
```

### Option B: Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/lbjlaq/Antigravity-Manager/main/install.ps1 | iex
```

### Option C: Homebrew (macOS / Linuxbrew)

```bash
brew tap lbjlaq/antigravity-manager https://github.com/lbjlaq/Antigravity-Manager
brew install --cask antigravity-tools
```

### Option D: Docker (recommended for servers/NAS)

```bash
docker run -d --name antigravity-manager \
  -p 8045:8045 \
  -e API_KEY=$ANTIGRAVITY_API_KEY \
  -e WEB_PASSWORD=$ANTIGRAVITY_WEB_PASSWORD \
  -e ABV_MAX_BODY_SIZE=104857600 \
  -v ~/.antigravity_tools:/root/.antigravity_tools \
  lbjlaq/antigravity-manager:latest
```

Docker Compose:

```yaml
# docker-compose.yml
version: "3.8"
services:
  antigravity:
    image: lbjlaq/antigravity-manager:latest
    container_name: antigravity-manager
    restart: unless-stopped
    ports:
      - "8045:8045"
    environment:
      - API_KEY=${ANTIGRAVITY_API_KEY}
      - WEB_PASSWORD=${ANTIGRAVITY_WEB_PASSWORD}
      - ABV_MAX_BODY_SIZE=104857600
    volumes:
      - ~/.antigravity_tools:/root/.antigravity_tools
```

```bash
docker compose up -d
docker logs antigravity-manager          # view logs / recover forgotten keys
```

### Option E: Manual download

Download from [GitHub Releases](https://github.com/lbjlaq/Antigravity-Manager/releases):
- macOS: `.dmg` (Apple Silicon + Intel)
- Windows: `.msi` or portable `.zip`
- Linux: `.deb`, `.rpm`, or `.AppImage`

---

## Authentication / Security Model

Antigravity uses two separate credentials:

| Credential | Env var | Config key | Purpose |
|---|---|---|---|
| API Key | `API_KEY` | `api_key` | Authenticates AI API calls (`Authorization: Bearer ...`) |
| Web Password | `WEB_PASSWORD` | `admin_password` | Logs into the management web UI |

**Scenario A — only `API_KEY` set:**
- Web UI login: use `API_KEY`
- API calls: use `API_KEY`

**Scenario B — both set (recommended):**
- Web UI login: `WEB_PASSWORD` only (API Key rejected for login)
- API calls: `API_KEY` only

Recover credentials:
```bash
docker logs antigravity-manager
# or
grep -E '"api_key"|"admin_password"' ~/.antigravity_tools/gui_config.json
```

---

## API Endpoints

The proxy server runs on port **8045** by default.

### OpenAI-compatible (works with any OpenAI SDK)

```
POST http://localhost:8045/v1/chat/completions
Authorization: Bearer $ANTIGRAVITY_API_KEY
```

### Anthropic-native (Claude Code, etc.)

```
POST http://localhost:8045/v1/messages
Authorization: Bearer $ANTIGRAVITY_API_KEY
```

### Gemini-native

```
POST http://localhost:8045/v1/models/{model}:generateContent
Authorization: Bearer $ANTIGRAVITY_API_KEY
```

---

## Code Examples

### Python — OpenAI SDK (Gemini via Antigravity)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ANTIGRAVITY_API_KEY"],
    base_url="http://localhost:8045/v1",
)

response = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[
        {"role": "user", "content": "Explain quantum entanglement in simple terms."}
    ],
    stream=True,
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Python — Anthropic SDK (Claude via Antigravity)

```python
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ["ANTIGRAVITY_API_KEY"],
    base_url="http://localhost:8045",
)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a haiku about distributed systems."}
    ],
)
print(message.content[0].text)
```

### Python — Streaming with Anthropic

```python
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ["ANTIGRAVITY_API_KEY"],
    base_url="http://localhost:8045",
)

with client.messages.stream(
    model="claude-opus-4-5",
    max_tokens=2048,
    system="You are a helpful coding assistant.",
    messages=[{"role": "user", "content": "Implement a binary search in Rust."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### TypeScript / Node — OpenAI SDK

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.ANTIGRAVITY_API_KEY!,
  baseURL: "http://localhost:8045/v1",
});

async function chat(prompt: string): Promise<string> {
  const response = await client.chat.completions.create({
    model: "gemini-2.5-flash",
    messages: [{ role: "user", content: prompt }],
  });
  return response.choices[0].message.content ?? "";
}

// Image generation via Imagen 3
async function generateImage(prompt: string) {
  const response = await client.images.generate({
    model: "imagen-3.0-generate-002",
    prompt,
    size: "1024x1024",  // maps to Imagen 3 aspect ratio
    n: 1,
  });
  return response.data[0].url;
}
```

### cURL — quick test

```bash
# Test OpenAI-compatible endpoint
curl -s http://localhost:8045/v1/chat/completions \
  -H "Authorization: Bearer $ANTIGRAVITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-pro",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | jq '.choices[0].message.content'

# Test Anthropic endpoint
curl -s http://localhost:8045/v1/messages \
  -H "Authorization: Bearer $ANTIGRAVITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | jq '.content[0].text'
```

---

## Connecting Claude Code CLI

Claude Code uses the Anthropic protocol. Point it at Antigravity:

```bash
# Set environment variables before starting Claude Code
export ANTHROPIC_API_KEY=$ANTIGRAVITY_API_KEY
export ANTHROPIC_BASE_URL=http://localhost:8045

claude  # start Claude Code — it will use Antigravity as the backend
```

Or create a `.env` in your project root:

```bash
# .env
ANTHROPIC_API_KEY=your-antigravity-api-key
ANTHROPIC_BASE_URL=http://localhost:8045
```

---

## Connecting to Popular AI Clients

### Cherry Studio

1. Open Cherry Studio → Settings → API Provider
2. Select **OpenAI-compatible**
3. Base URL: `http://localhost:8045/v1`
4. API Key: your `ANTIGRAVITY_API_KEY`

### Cursor

In Cursor settings, set:
- OpenAI Base URL: `http://localhost:8045/v1`
- API Key: your `ANTIGRAVITY_API_KEY`

### Continue.dev

```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "Gemini Pro (Antigravity)",
      "provider": "openai",
      "model": "gemini-2.5-pro",
      "apiKey": "YOUR_ANTIGRAVITY_API_KEY",
      "apiBase": "http://localhost:8045/v1"
    },
    {
      "title": "Claude (Antigravity)",
      "provider": "anthropic",
      "model": "claude-sonnet-4-5",
      "apiKey": "YOUR_ANTIGRAVITY_API_KEY",
      "apiBase": "http://localhost:8045"
    }
  ]
}
```

---

## Configuration File

Config is stored at `~/.antigravity_tools/gui_config.json`:

```json
{
  "api_key": "sk-your-api-key",
  "admin_password": "your-web-ui-password",
  "proxy": {
    "port": 8045,
    "max_body_size": 104857600,
    "admin_password": "your-web-ui-password"
  },
  "model_routes": [
    {
      "pattern": "gpt-4.*",
      "target": "gemini-2.5-pro"
    },
    {
      "pattern": "gpt-3.5.*",
      "target": "gemini-2.5-flash"
    }
  ]
}
```

### Environment Variables (Docker / server mode)

| Variable | Description | Default |
|---|---|---|
| `API_KEY` | API key for authenticating proxy requests | required |
| `WEB_PASSWORD` | Web UI admin password | falls back to `API_KEY` |
| `ABV_MAX_BODY_SIZE` | Max request body in bytes (for image uploads) | `104857600` (100MB) |

---

## Model Routing

Antigravity's model router lets you remap incoming model names to actual upstream models. This is useful when clients hard-code model names like `gpt-4`.

Configuration via Web UI (API Proxy → Model Router) or `gui_config.json`:

```json
{
  "model_routes": [
    {
      "pattern": "gpt-4-turbo",
      "target": "gemini-2.5-pro"
    },
    {
      "pattern": "gpt-4o",
      "target": "gemini-2.5-pro"
    },
    {
      "pattern": "gpt-3\\.5.*",
      "target": "gemini-2.5-flash"
    },
    {
      "pattern": "claude-3-opus.*",
      "target": "claude-opus-4-5"
    }
  ]
}
```

**Tiered routing** (automatic): Antigravity prioritizes accounts by type (Ultra → Pro → Free) and quota reset frequency, consuming fast-reset accounts first.

**Background task demotion** (automatic): Requests detected as background tasks (e.g., Claude CLI title generation) are automatically redirected to Flash-tier models to preserve premium quota.

---

## Account Management

### Adding accounts via the UI

1. Open Antigravity Manager desktop app or web UI (`http://localhost:8045`)
2. Navigate to **Accounts**
3. Click **Add Account** — the app generates an OAuth 2.0 authorization URL
4. Complete authorization in any browser
5. The app captures the callback automatically; click "I've authorized, continue" if needed

### Batch import (JSON)

Export from another tool and import in the Accounts page:

```json
[
  {
    "token": "session-token-1",
    "type": "google",
    "label": "account-work"
  },
  {
    "token": "session-token-2",
    "type": "anthropic",
    "label": "account-personal"
  }
]
```

### Migration from v1

Antigravity auto-detects and migrates v1 database format on first launch — no manual steps needed.

---

## Quota Monitoring

The dashboard shows live quota across all accounts:

- **Gemini Pro** remaining calls (average across accounts)
- **Gemini Flash** remaining calls
- **Claude** remaining calls
- **Imagen 3** image generation quota

**Smart Recommendation**: The dashboard algorithmically selects the account with the most headroom and offers one-click switching.

**403 detection**: Accounts banned upstream are automatically flagged and skipped during rotation.

---

## Building from Source (Rust + Tauri v2)

### Prerequisites

```bash
# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Node.js (for frontend)
node --version  # requires v18+

# Tauri v2 CLI
cargo install tauri-cli --version "^2"

# System deps (Linux)
sudo apt install libwebkit2gtk-4.1-dev libayatana-appindicator3-dev librsvg2-dev
```

### Build & run

```bash
git clone https://github.com/lbjlaq/Antigravity-Manager.git
cd Antigravity-Manager

npm install          # install frontend deps
cargo tauri dev      # run in development mode
cargo tauri build    # build release binaries → src-tauri/target/release/bundle/
```

### Build headless server only (no GUI)

```bash
cd src-tauri
cargo build --release --features headless
./target/release/antigravity-manager --headless --port 8045
```

---

## Troubleshooting

### Port 8045 already in use

```bash
# Find and kill the process
lsof -ti:8045 | xargs kill -9
# or change port in gui_config.json:
# "proxy": { "port": 8046 }
```

### Forgotten API key or web password

```bash
# Docker
docker logs antigravity-manager | grep -E "api_key|password"

# Local install
cat ~/.antigravity_tools/gui_config.json | grep -E '"api_key"|"admin_password"'
```

### Account shows 403 / banned

The account has been flagged upstream. In the Accounts view it will be marked with a 403 badge and automatically skipped. Add a fresh account and remove/re-authorize the banned one.

### Requests failing with 429

Antigravity handles this automatically (rotates to next account within milliseconds). If all accounts are exhausted, add more accounts or wait for quota reset. Check the dashboard for per-account quota status.

### macOS Gatekeeper blocking the app

```bash
xattr -d com.apple.quarantine /Applications/Antigravity\ Tools.app
# or install with:
brew install --cask antigravity-tools --no-quarantine
```

### Docker container not persisting accounts after restart

Ensure the volume mount is correct:
```bash
docker run ... -v ~/.antigravity_tools:/root/.antigravity_tools ...
# Verify data is present:
ls ~/.antigravity_tools/
```

### Claude Code not connecting

```bash
# Verify the proxy is running
curl -s http://localhost:8045/v1/models \
  -H "Authorization: Bearer $ANTIGRAVITY_API_KEY"

# Check env vars are exported (not just set)
export ANTHROPIC_BASE_URL=http://localhost:8045
export ANTHROPIC_API_KEY=$ANTIGRAVITY_API_KEY
echo $ANTHROPIC_BASE_URL  # should print the URL
```

---

## Project Structure (for contributors)

```
Antigravity-Manager/
├── src/                    # React frontend (TypeScript)
│   ├── components/         # UI components (Dashboard, Accounts, etc.)
│   └── pages/
├── src-tauri/              # Rust backend
│   ├── src/
│   │   ├── main.rs         # Tauri app entry
│   │   ├── proxy/          # Axum HTTP proxy server
│   │   │   ├── router.rs   # Model routing logic
│   │   │   ├── dispatcher.rs # Account rotation
│   │   │   └── mapper.rs   # Protocol conversion
│   │   ├── accounts/       # Account storage & OAuth
│   │   └── quota/          # Quota tracking
│   └── Cargo.toml
├── docker/
│   └── Dockerfile
├── install.sh              # Linux/macOS installer
├── install.ps1             # Windows installer
└── docker-compose.yml
```
