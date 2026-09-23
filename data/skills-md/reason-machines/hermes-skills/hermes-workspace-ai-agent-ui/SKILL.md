---
name: hermes-workspace-ai-agent-ui
description: Native web workspace for Hermes Agent with chat, terminal, memory, skills, inspector, and multi-agent orchestration
triggers:
  - "set up hermes workspace"
  - "configure hermes agent ui"
  - "connect workspace to hermes gateway"
  - "enable swarm mode for multiple agents"
  - "customize hermes workspace theme"
  - "troubleshoot hermes workspace connection"
  - "deploy hermes workspace with docker"
  - "configure conductor missions"
---

# Hermes Workspace AI Agent UI

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Workspace is a native web interface for Hermes Agent that provides chat, terminal, memory browser, skills catalog, MCP integration, multi-agent orchestration, and a complete control plane for autonomous AI workflows. Unlike chat wrappers, it's a full workspace with file browsing, persistent sessions, role-based agent dispatch, and swarm mode for managing multiple Hermes Agent workers.

## What It Does

- **Chat Interface**: Real-time SSE streaming, tool call rendering, multi-session support, markdown + syntax highlighting
- **Memory Browser**: Search, edit, and manage agent memory with live markdown editor
- **Skills Catalog**: Browse 2,000+ skills with origin badges, filters, source paths
- **MCP Integration**: Full Model Context Protocol catalog, marketplace, and source management
- **Terminal & Files**: Monaco-powered file browser and cross-platform PTY terminal
- **Multi-Agent Dashboard**: Manage multiple Hermes Agent instances with profile presets (Sage/Trader/Builder/Scribe/Ops)
- **Swarm Mode**: Persistent tmux-backed agent workers with role-based dispatch and Kanban task board
- **Conductor**: Mission decomposition and dispatch with fallback to native swarm orchestration
- **PWA Support**: Install as native app, access over Tailscale

## Installation

### Docker Compose (Recommended for Self-Hosting)

```bash
# Clone repository
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace

# Start with docker-compose
docker-compose up -d

# Access at http://localhost:3000
```

### One-Line Install (macOS/Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/outsourc-e/hermes-workspace/main/install.sh | bash

# Terminal 1: Start Hermes Agent gateway
hermes gateway run

# Terminal 2: Start workspace
cd ~/hermes-workspace && pnpm dev
```

### Manual Installation

```bash
# Prerequisites: Node.js 22+, pnpm
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace

# Install dependencies
pnpm install

# Configure environment
cp .env.example .env

# Edit .env with your settings
echo 'HERMES_API_URL=http://127.0.0.1:8642' >> .env
echo 'HERMES_DASHBOARD_URL=http://127.0.0.1:9119' >> .env

# Start development server
pnpm dev
```

### Attach to Existing Hermes Agent

If you already have a Hermes Agent gateway running:

```bash
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace
pnpm install
cp .env.example .env

# Point to existing gateway
echo 'HERMES_API_URL=http://127.0.0.1:8642' >> .env
echo 'HERMES_DASHBOARD_URL=http://127.0.0.1:9119' >> .env

# If gateway requires auth
echo 'HERMES_API_TOKEN=your_api_server_key' >> .env

pnpm dev
```

## Configuration

### Environment Variables

```bash
# Required: OpenAI-compatible backend URL
HERMES_API_URL=http://127.0.0.1:8642

# Optional: Dashboard API for enhanced features
HERMES_DASHBOARD_URL=http://127.0.0.1:9119

# Optional: Gateway authentication token
HERMES_API_TOKEN=your_api_server_key

# Optional: UI password protection
HERMES_PASSWORD=your_password

# Optional: Provider API keys (only if using these providers)
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-v1-...
GOOGLE_API_KEY=AIza...
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Custom port
PORT=3000
```

### Gateway Requirements

For full functionality, the Hermes Agent gateway needs:

```bash
# In ~/.hermes/.env or gateway config
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0
API_SERVER_PORT=8642

# Optional: Enable authentication
API_SERVER_KEY=your_secret_key
```

Start gateway and dashboard:

```bash
hermes gateway run        # Port 8642
hermes dashboard          # Port 9119
```

### Remote Access (Tailscale/VPN)

For access from remote devices:

```bash
# Use Tailscale/LAN IP instead of localhost
echo 'HERMES_API_URL=http://100.x.y.z:8642' >> .env
echo 'HERMES_DASHBOARD_URL=http://100.x.y.z:9119' >> .env

# Gateway must bind to 0.0.0.0
echo 'API_SERVER_HOST=0.0.0.0' >> ~/.hermes/.env
```

## Usage Patterns

### Connecting to Local Models

#### Ollama

```bash
# Start Ollama with CORS enabled
OLLAMA_ORIGINS=* ollama serve

# Start workspace pointing to Ollama
HERMES_API_URL=http://127.0.0.1:11434 pnpm dev
```

#### LM Studio

```bash
# Start LM Studio server on port 1234
# In workspace:
HERMES_API_URL=http://127.0.0.1:1234/v1 pnpm dev
```

#### Atomic Chat

```bash
# Start Atomic Chat desktop app
# In workspace:
HERMES_API_URL=http://127.0.0.1:1337/v1 pnpm dev
```

### Swarm Mode Setup

Enable multi-agent orchestration:

```bash
# Start multiple agent workers
cd ~/hermes-workspace
pnpm swarm:start

# View swarm docs
cat docs/swarm/README.md

# Configure roles in workspace UI:
# Settings → Swarm → Configure Roles
# - builder: Code implementation
# - reviewer: PR review and validation
# - docs: Documentation
# - research: Investigation
# - ops: Operations and deployment
# - triage: Issue classification
# - qa: Quality assurance
# - lab: Experiments
```

### API Integration

For programmatic access:

```typescript
// Next.js API route example
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { message, sessionId } = await req.json();
  
  const response = await fetch(`${process.env.HERMES_API_URL}/v1/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.HERMES_API_TOKEN || ''}`
    },
    body: JSON.stringify({
      model: 'hermes-3',
      messages: [{ role: 'user', content: message }],
      stream: true
    })
  });
  
  return new NextResponse(response.body);
}
```

### Custom Theme Configuration

Create or modify themes in `src/styles/themes`:

```typescript
// src/styles/themes/custom.ts
export const customTheme = {
  name: 'custom',
  colors: {
    background: '#0a0a0a',
    foreground: '#ffffff',
    primary: '#6366f1',
    secondary: '#8b5cf6',
    accent: '#ec4899',
    muted: '#374151',
    border: '#1f2937'
  },
  fonts: {
    sans: 'Inter, system-ui, sans-serif',
    mono: 'JetBrains Mono, monospace'
  }
};
```

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  hermes-workspace:
    build: .
    ports:
      - "3000:3000"
    environment:
      - HERMES_API_URL=http://hermes-gateway:8642
      - HERMES_DASHBOARD_URL=http://hermes-gateway:9119
      - HERMES_API_TOKEN=${HERMES_API_TOKEN}
    depends_on:
      - hermes-gateway
    volumes:
      - ./data:/app/data

  hermes-gateway:
    image: nousresearch/hermes-agent:latest
    ports:
      - "8642:8642"
      - "9119:9119"
    environment:
      - API_SERVER_ENABLED=true
      - API_SERVER_HOST=0.0.0.0
      - API_SERVER_KEY=${HERMES_API_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./hermes-data:/root/.hermes
```

### Conductor Mission Dispatch

```typescript
// Dispatching a mission programmatically
const dispatchMission = async (mission: string) => {
  const response = await fetch('/api/conductor/dispatch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mission,
      mode: 'auto', // or 'native-swarm'
      decompose: true
    })
  });
  
  const result = await response.json();
  return result;
};

// Example usage
await dispatchMission('Review and merge PR #42, update docs');
```

## Key Commands

### Development

```bash
# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run tests
pnpm test

# Lint code
pnpm lint

# Type check
pnpm type-check
```

### Swarm Management

```bash
# Start swarm workers
pnpm swarm:start

# Stop swarm workers
pnpm swarm:stop

# View swarm status
pnpm swarm:status

# Attach to worker terminal
pnpm swarm:attach <worker-name>
```

### Docker

```bash
# Build image
docker build -t hermes-workspace .

# Run container
docker run -p 3000:3000 \
  -e HERMES_API_URL=http://gateway:8642 \
  -e HERMES_DASHBOARD_URL=http://gateway:9119 \
  hermes-workspace

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## Troubleshooting

### Connection Issues

```bash
# Verify gateway is running
curl http://127.0.0.1:8642/health
# Expected: {"status":"ok"}

# Verify dashboard is running
curl http://127.0.0.1:9119/api/status
# Expected: dashboard metadata JSON

# Check gateway logs
hermes gateway run --verbose

# Check workspace logs
pnpm dev
# Look for connection probe results
```

### Authentication Failures

```bash
# Ensure API_SERVER_KEY matches HERMES_API_TOKEN
# In gateway config (~/.hermes/.env):
API_SERVER_KEY=your_secret

# In workspace .env:
HERMES_API_TOKEN=your_secret

# Or disable auth entirely:
# Remove API_SERVER_KEY from gateway
# Remove HERMES_API_TOKEN from workspace
```

### Features Not Appearing

```bash
# Check capability detection in browser console:
# Settings → Connection → Test Connection

# Verify dashboard is running for enhanced features:
ps aux | grep "hermes dashboard"

# Check HERMES_DASHBOARD_URL is set correctly:
echo $HERMES_DASHBOARD_URL

# Restart both services:
pkill -f "hermes gateway"
pkill -f "hermes dashboard"
hermes gateway run &
hermes dashboard &
```

### Swarm Workers Not Starting

```bash
# Check tmux sessions
tmux ls

# Verify worker processes
ps aux | grep hermes

# Check worker logs
tail -f ~/.hermes/logs/worker-*.log

# Reset swarm state
pnpm swarm:stop
rm -rf ~/.hermes/swarm-state
pnpm swarm:start
```

### Memory/Performance Issues

```bash
# Increase Node.js memory
NODE_OPTIONS="--max-old-space-size=4096" pnpm dev

# Clear workspace cache
rm -rf .next
pnpm build

# Check Docker resource limits
docker stats
# Increase in Docker Desktop settings if needed
```

### Remote Access Not Working

```bash
# Verify gateway binds to 0.0.0.0
grep API_SERVER_HOST ~/.hermes/.env
# Should be: API_SERVER_HOST=0.0.0.0

# Test from remote device
curl http://<tailscale-ip>:8642/health

# Check firewall rules
sudo ufw status
sudo ufw allow 8642/tcp
sudo ufw allow 9119/tcp

# Verify Tailscale connectivity
tailscale status
ping <tailscale-ip>
```

### Build Errors

```bash
# Clear all caches and reinstall
rm -rf node_modules .next pnpm-lock.yaml
pnpm install
pnpm build

# Verify Node.js version
node --version
# Must be 22.0.0 or higher

# Check for TypeScript errors
pnpm type-check
```

## Advanced Configuration

### Custom Skills Integration

```bash
# Add custom skills directory
export HERMES_SKILLS_PATH=/path/to/custom/skills

# Skills should follow format:
# /custom/skills/
#   ├── skill-name/
#   │   ├── SKILL.md
#   │   └── metadata.json
```

### Persistent Sessions

```bash
# Sessions stored in ~/.hermes/sessions/
# Backup sessions:
tar -czf sessions-backup.tar.gz ~/.hermes/sessions/

# Restore sessions:
tar -xzf sessions-backup.tar.gz -C ~/
```

### Custom API Routes

```typescript
// app/api/custom/route.ts
import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  // Custom endpoint logic
  const data = await req.json();
  
  // Forward to gateway with custom headers
  const response = await fetch(`${process.env.HERMES_API_URL}/custom`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Custom-Header': 'value'
    },
    body: JSON.stringify(data)
  });
  
  return response;
}
```

## Resources

- GitHub: https://github.com/outsourc-e/hermes-workspace
- Documentation: https://hermes-workspace.com
- Hermes Agent: https://github.com/NousResearch/hermes-agent
- Swarm Docs: `docs/swarm/README.md` in repository
- Issues: https://github.com/outsourc-e/hermes-workspace/issues
