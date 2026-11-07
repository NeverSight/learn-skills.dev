---
name: holyclaude-ai-workstation
description: Deploy a full AI coding workstation with Claude Code, web UI, headless browser, and 5 AI CLIs in a single Docker container
triggers:
  - set up HolyClaude
  - run Claude Code in Docker
  - AI coding workstation container
  - Claude Code web UI setup
  - deploy HolyClaude with docker compose
  - configure HolyClaude environment
  - headless browser with Claude Code
  - HolyClaude troubleshooting
---

# HolyClaude AI Workstation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

HolyClaude is a containerized AI development workstation that bundles Claude Code CLI, a CloudCLI web UI, Chromium headless browser with Playwright, 5 AI CLIs (Claude, Gemini, OpenAI Codex, Cursor, TaskMaster AI), and 50+ dev tools into a single Docker image. One `docker compose up` replaces hours of manual setup.

---

## Installation

### Prerequisites
- Docker + Docker Compose installed
- Existing Anthropic account (Max/Pro subscription or API key)

### Quick Start

```bash
mkdir holyclaude && cd holyclaude
```

Create `docker-compose.yaml`:

```yaml
services:
  holyclaude:
    image: CoderLuii/HolyClaude:latest
    container_name: holyclaude
    hostname: holyclaude
    restart: unless-stopped
    shm_size: 2g
    ports:
      - "3001:3001"
    volumes:
      - ./data/claude:/root/.claude
      - ./data/config:/root/.config
      - ./projects:/workspace
    environment:
      - PUID=1000
      - PGID=1000
```

```bash
docker compose up -d
# Open http://localhost:3001
```

### Image Variants

```bash
# Full image — all tools pre-installed (recommended)
docker pull CoderLuii/HolyClaude:latest

# Slim image — smaller download, tools installed on demand
docker pull CoderLuii/HolyClaude:slim

# Pinned version for production stability
docker pull CoderLuii/HolyClaude:1.2.3
docker pull CoderLuii/HolyClaude:1.2.3-slim
```

---

## Full Docker Compose Configuration

```yaml
services:
  holyclaude:
    image: CoderLuii/HolyClaude:latest
    container_name: holyclaude
    hostname: holyclaude
    restart: unless-stopped
    shm_size: 2g                          # Required for Chromium
    ports:
      - "3001:3001"                       # CloudCLI web UI
    volumes:
      - ./data/claude:/root/.claude       # Claude credentials & config (persisted)
      - ./data/config:/root/.config       # App config (persisted)
      - ./projects:/workspace             # Your project files
    environment:
      # User/group IDs (match host user to avoid permission issues)
      - PUID=1000
      - PGID=1000

      # AI provider API keys (optional — can also set via web UI)
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - CURSOR_API_KEY=${CURSOR_API_KEY}

      # NAS/SMB mount polling (enable if using Synology/QNAP)
      - CHOKIDAR_USEPOLLING=true

      # Notification webhooks (optional)
      - DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL}
      - SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
    security_opt:
      - seccomp:unconfined               # Required for Chromium sandbox
```

### Environment Variable Reference

| Variable | Required | Description |
|---|---|---|
| `PUID` | Recommended | Host user ID (run `id -u` to find yours) |
| `PGID` | Recommended | Host group ID (run `id -g` to find yours) |
| `ANTHROPIC_API_KEY` | Optional | Anthropic API key (alternative to OAuth login) |
| `GEMINI_API_KEY` | Optional | Google AI API key for Gemini CLI |
| `OPENAI_API_KEY` | Optional | OpenAI API key for Codex CLI |
| `CURSOR_API_KEY` | Optional | Cursor API key |
| `CHOKIDAR_USEPOLLING` | NAS only | Set `true` for SMB/NFS mounts |
| `DISCORD_WEBHOOK_URL` | Optional | Discord notifications |
| `SLACK_WEBHOOK_URL` | Optional | Slack notifications |

---

## Authentication

### Method 1: OAuth (Claude Max/Pro Subscription)
1. Open `http://localhost:3001`
2. Create a CloudCLI account (10 seconds)
3. Sign in with your Anthropic account via OAuth
4. No API key needed — uses your existing subscription

### Method 2: API Key
```yaml
environment:
  - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```
Or paste the key directly in the CloudCLI web UI settings.

### Credential Persistence
Credentials are stored in the bind-mounted volume:
```
./data/claude/     →  /root/.claude/
./data/config/     →  /root/.config/
```
Credentials survive container restarts, updates, and recreation.

---

## Platform-Specific Configuration

### Linux (amd64/arm64) — Default
```yaml
# No extra config needed
shm_size: 2g
```

### macOS (Docker Desktop)
```yaml
# Works out of the box with Docker Desktop
shm_size: 2g
```

### Windows (WSL2 + Docker Desktop)
```yaml
# Requires WSL2 backend enabled in Docker Desktop
shm_size: 2g
```

### Synology / QNAP NAS
```yaml
environment:
  - CHOKIDAR_USEPOLLING=true    # Fixes file watching on SMB mounts
volumes:
  - /volume1/docker/holyclaude/data/claude:/root/.claude
  - /volume1/docker/holyclaude/projects:/workspace
```

### Kubernetes (ARM64 / Oracle Cloud Graviton)
```yaml
# arm64 image is published alongside amd64
image: CoderLuii/HolyClaude:latest   # multi-arch manifest auto-selects correct arch
```

---

## What's Inside the Container

### AI CLIs

| CLI | Invocation | Key Provider |
|---|---|---|
| Claude Code | `claude` | Anthropic (`ANTHROPIC_API_KEY` or OAuth) |
| Gemini CLI | `gemini` | Google (`GEMINI_API_KEY`) |
| OpenAI Codex | `codex` | OpenAI (`OPENAI_API_KEY`) |
| Cursor | `cursor` | Cursor (`CURSOR_API_KEY`) |
| TaskMaster AI | `task-master` | Uses configured AI provider keys |

### Headless Browser Stack
- **Chromium** — pre-installed and configured
- **Xvfb** — virtual display on `:99`
- **Playwright** — configured and ready
- **Shared memory** — `shm_size: 2g` pre-configured (fixes the 64MB Docker default)

### Dev Tools (50+)
- **Languages**: Node.js, Python 3, TypeScript, Bun, Deno
- **Package managers**: npm, yarn, pnpm, pip, cargo
- **Database clients**: PostgreSQL, MySQL, SQLite, Redis CLI
- **Cloud CLIs**: AWS CLI, Google Cloud SDK, Azure CLI
- **Dev tools**: GitHub CLI (`gh`), Git, curl, jq, ripgrep, fd
- **Process manager**: s6-overlay (auto-restart, graceful shutdown)

---

## Working with Projects

### Mount your project directory
```yaml
volumes:
  - ./projects:/workspace
  # Or mount a specific project:
  - /path/to/my-app:/workspace/my-app
```

### Inside the container
```bash
# Access the container shell
docker exec -it holyclaude bash

# Navigate to workspace
cd /workspace

# Run Claude Code directly
claude

# Run other AI CLIs
gemini
codex
```

---

## Playwright / Headless Browser Usage

Playwright is pre-configured. Use it from Claude Code tasks or directly:

```typescript
// playwright.config.ts — already works inside the container
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    // Chromium is pre-installed, no download needed
    browserName: 'chromium',
    launchOptions: {
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',  // Use /tmp instead of /dev/shm
      ],
    },
  },
});
```

```typescript
// Direct Playwright usage inside container
import { chromium } from 'playwright';

const browser = await chromium.launch({
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
  ],
});
const page = await browser.newPage();
await page.goto('https://example.com');
const screenshot = await page.screenshot({ path: '/workspace/screenshot.png' });
await browser.close();
```

```bash
# Run Playwright tests inside container
docker exec -it holyclaude bash -c "cd /workspace && npx playwright test"

# Run with headed mode via Xvfb
docker exec -it holyclaude bash -c "DISPLAY=:99 npx playwright test --headed"
```

---

## Updating HolyClaude

```bash
# Pull latest image
docker compose pull

# Recreate container with new image (zero data loss — data is in bind mounts)
docker compose up -d

# Or explicit recreation
docker compose down && docker compose up -d
```

### Pinned Version Strategy
```yaml
# For production: pin to a specific version
image: CoderLuii/HolyClaude:1.2.3

# Update by changing the tag and running:
docker compose up -d
```

---

## Data & Persistence

```
holyclaude/
├── docker-compose.yaml
├── data/
│   ├── claude/          # Claude credentials, .claude.json, history
│   └── config/          # CloudCLI and app configuration
└── projects/            # Your workspace (mount your code here)
```

**All credentials and config survive:**
- Container restarts
- `docker compose down && up`
- Image updates via `docker compose pull`
- Container recreation

---

## Common Patterns

### Pattern: Multiple Projects
```yaml
volumes:
  - ./data/claude:/root/.claude
  - ./data/config:/root/.config
  - ~/code/project-a:/workspace/project-a
  - ~/code/project-b:/workspace/project-b
  - ~/code/project-c:/workspace/project-c
```

### Pattern: Read-only API Keys via .env file
```bash
# .env (never commit this)
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
OPENAI_API_KEY=sk-...
```

```yaml
# docker-compose.yaml
services:
  holyclaude:
    env_file: .env
```

### Pattern: Custom Port
```yaml
ports:
  - "8080:3001"    # Access via http://localhost:8080
```

### Pattern: Remote Server Access
```yaml
ports:
  - "0.0.0.0:3001:3001"    # Accessible from network
# Then access via http://your-server-ip:3001
# Recommend putting behind nginx/Caddy with HTTPS for production
```

### Pattern: Nginx Reverse Proxy
```yaml
services:
  holyclaude:
    image: CoderLuii/HolyClaude:latest
    # Don't expose ports directly — nginx handles it
    expose:
      - "3001"
    networks:
      - web

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certs:/etc/nginx/certs
    networks:
      - web

networks:
  web:
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs holyclaude

# Check if port 3001 is already in use
lsof -i :3001
```

### Chromium crashes / headless browser fails
```yaml
# Ensure shm_size is set (CRITICAL)
shm_size: 2g

# Ensure seccomp is unconfined
security_opt:
  - seccomp:unconfined
```

```bash
# Verify display is available inside container
docker exec holyclaude bash -c "echo $DISPLAY"
# Should output: :99
```

### Permission denied errors on bind mounts
```yaml
environment:
  - PUID=1000    # Must match your host user: `id -u`
  - PGID=1000    # Must match your host group: `id -g`
```

```bash
# Fix existing permissions on host
sudo chown -R 1000:1000 ./data ./projects
```

### File watching broken on NAS / SMB mounts
```yaml
environment:
  - CHOKIDAR_USEPOLLING=true
```

### Claude Code installer hangs
This is pre-solved in HolyClaude — the container sets the correct WORKDIR ownership. If you're building a custom image on top:
```dockerfile
# Ensure WORKDIR is not root-owned before running Claude Code installer
RUN chown -R node:node /app
WORKDIR /app
```

### SQLite locks on NAS mount
```yaml
volumes:
  # Move SQLite databases to a local volume, not NAS mount
  - holyclaude-db:/root/.local/share/holyclaude
  - /nas/mount:/workspace    # NAS mount only for project files

volumes:
  holyclaude-db:
```

### Claude Code authentication lost after restart
```yaml
# Ensure this volume is mounted (credentials live here)
volumes:
  - ./data/claude:/root/.claude
```

### Process keeps dying / not restarting
HolyClaude uses s6-overlay for process supervision. Check service status:
```bash
docker exec holyclaude s6-svstat /run/service/cloudcli
docker exec holyclaude s6-svstat /run/service/xvfb
```

---

## Building Locally

```bash
git clone https://github.com/CoderLuii/HolyClaude.git
cd HolyClaude

# Build full image
docker build -t holyclaude:local .

# Build slim image
docker build -t holyclaude:local-slim --target slim .

# Build for specific platform
docker buildx build --platform linux/arm64 -t holyclaude:arm64 .

# Run your local build
docker run -d \
  --name holyclaude \
  --shm-size=2g \
  -p 3001:3001 \
  -v $(pwd)/data/claude:/root/.claude \
  holyclaude:local
```

---

## Quick Reference

```bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs (live)
docker compose logs -f holyclaude

# Shell access
docker exec -it holyclaude bash

# Update to latest
docker compose pull && docker compose up -d

# Restart only the container
docker compose restart holyclaude

# Check resource usage
docker stats holyclaude
```
