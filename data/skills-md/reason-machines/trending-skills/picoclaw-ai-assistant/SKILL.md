---
name: picoclaw-ai-assistant
description: Ultra-lightweight AI assistant in Go that runs on $10 hardware with <10MB RAM, supporting multiple LLM providers, tools, and single-binary deployment across RISC-V, ARM, MIPS, and x86.
triggers:
  - "set up picoclaw on my device"
  - "configure picoclaw with my API key"
  - "deploy picoclaw on raspberry pi"
  - "build picoclaw from source"
  - "add a new LLM provider to picoclaw"
  - "run picoclaw in docker"
  - "picoclaw web search tool setup"
  - "picoclaw memory and workspace configuration"
---

# PicoClaw AI Assistant

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

PicoClaw is an ultra-lightweight personal AI assistant written in Go. It runs on $10 hardware with under 10MB RAM and boots in under 1 second. It supports multiple LLM providers (OpenAI-compatible, Anthropic, Volcengine), optional web search tools, and deploys as a single self-contained binary on x86_64, ARM64, MIPS, and RISC-V Linux devices.

---

## Installation

### Precompiled Binary

Download from the [releases page](https://github.com/sipeed/picoclaw/releases):

```bash
# Linux ARM64 (Raspberry Pi, LicheeRV-Nano, etc.)
wget https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-arm64
chmod +x picoclaw-linux-arm64
./picoclaw-linux-arm64 onboard
```

### Build from Source

```bash
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw

# Install dependencies
make deps

# Build for current platform
make build

# Build for all platforms
make build-all

# Raspberry Pi Zero 2 W — 32-bit
make build-linux-arm      # → build/picoclaw-linux-arm

# Raspberry Pi Zero 2 W — 64-bit
make build-linux-arm64    # → build/picoclaw-linux-arm64

# Build both Pi Zero variants
make build-pi-zero

# Build and install to system PATH
make install
```

### Docker Compose

```bash
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw

# First run — generates docker/data/config.json then exits
docker compose -f docker/docker-compose.yml --profile gateway up

# Edit config
vim docker/data/config.json

# Start in background
docker compose -f docker/docker-compose.yml --profile gateway up -d

# View logs
docker compose -f docker/docker-compose.yml logs -f picoclaw-gateway

# Stop
docker compose -f docker/docker-compose.yml --profile gateway down
```

#### Docker: Web Console (Launcher Mode)

```bash
docker compose -f docker/docker-compose.yml --profile launcher up -d
# Open http://localhost:18800
```

#### Docker: One-shot Agent Mode

```bash
# Single question
docker compose -f docker/docker-compose.yml run --rm picoclaw-agent -m "What is 2+2?"

# Interactive session
docker compose -f docker/docker-compose.yml run --rm picoclaw-agent
```

#### Docker: Expose Gateway to Host

If the gateway needs to be reachable from the host, set:

```bash
PICOCLAW_GATEWAY_HOST=0.0.0.0 docker compose -f docker/docker-compose.yml --profile gateway up -d
```

Or set `PICOCLAW_GATEWAY_HOST=0.0.0.0` in `docker/data/config.json`.

### Termux (Android)

```bash
pkg install wget proot
wget https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-arm64
chmod +x picoclaw-linux-arm64
termux-chroot ./picoclaw-linux-arm64 onboard
```

---

## Quick Start

### 1. Initialize

```bash
picoclaw onboard
```

This creates `~/.picoclaw/config.json` with a starter configuration.

### 2. Configure `~/.picoclaw/config.json`

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.picoclaw/workspace",
      "model_name": "gpt-4o",
      "max_tokens": 8192,
      "temperature": 0.7,
      "max_tool_iterations": 20
    }
  },
  "model_list": [
    {
      "model_name": "gpt-4o",
      "model": "openai/gpt-4o",
      "api_key": "$OPENAI_API_KEY",
      "request_timeout": 300
    },
    {
      "model_name": "claude-sonnet",
      "model": "anthropic/claude-sonnet-4-5",
      "api_key": "$ANTHROPIC_API_KEY"
    },
    {
      "model_name": "ark-code",
      "model": "volcengine/ark-code-latest",
      "api_key": "$VOLCENGINE_API_KEY",
      "api_base": "https://ark.cn-beijing.volces.com/api/coding/v3"
    }
  ],
  "tools": {
    "web": {
      "brave": {
        "enabled": false,
        "api_key": "$BRAVE_API_KEY"
      },
      "tavily": {
        "enabled": false,
        "api_key": "$TAVILY_API_KEY"
      }
    }
  }
}
```

> Never hard-code API keys. Reference environment variables using `$VAR_NAME` notation in config, or set them in your shell environment before launch.

### 3. Run

```bash
# Interactive chat
picoclaw

# Single message
picoclaw -m "Summarize the latest Go release notes"

# Use a specific model
picoclaw -model claude-sonnet -m "Refactor this function for clarity"
```

---

## Key CLI Commands

| Command | Description |
|---|---|
| `picoclaw onboard` | Initialize config and workspace |
| `picoclaw` | Start interactive chat session |
| `picoclaw -m "..."` | Send a single message and exit |
| `picoclaw -model <name>` | Override the default model |
| `picoclaw -config <path>` | Use a custom config file |

---

## Configuration Reference

### Model Entry Fields

```json
{
  "model_name": "my-model",        // Alias used in -model flag and agent defaults
  "model": "provider/model-id",    // Provider-prefixed model identifier
  "api_key": "$ENV_VAR",           // API key — use env var reference
  "api_base": "https://...",       // Optional: override base URL (for self-hosted or regional endpoints)
  "request_timeout": 300           // Optional: seconds before timeout
}
```

### Supported Provider Prefixes

| Prefix | Provider |
|---|---|
| `openai/` | OpenAI and OpenAI-compatible APIs |
| `anthropic/` | Anthropic Claude |
| `volcengine/` | Volcengine (Ark) |

### Agent Defaults

```json
"agents": {
  "defaults": {
    "workspace": "~/.picoclaw/workspace",  // Working directory for file operations
    "model_name": "gpt-4o",                // Default model alias
    "max_tokens": 8192,                    // Max response tokens
    "temperature": 0.7,                    // Sampling temperature
    "max_tool_iterations": 20              // Max agentic tool-call loop iterations
  }
}
```

### Web Search Tools

Get free API keys:
- **Tavily**: https://tavily.com — 1,000 free queries/month
- **Brave Search**: https://brave.com/search/api — 2,000 free queries/month

```json
"tools": {
  "web": {
    "tavily": {
      "enabled": true,
      "api_key": "$TAVILY_API_KEY"
    },
    "brave": {
      "enabled": false,
      "api_key": "$BRAVE_API_KEY"
    }
  }
}
```

Only enable one search provider at a time unless you want fallback behavior.

---

## Common Patterns

### Pattern: Minimal $10 Device Setup

For a LicheeRV-Nano or similar ultra-low-resource board:

```bash
# Download the RISC-V or ARM binary from releases
wget https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-riscv64
chmod +x picoclaw-linux-riscv64

# Initialize
./picoclaw-linux-riscv64 onboard

# Edit config — use a lightweight model, low max_tokens
cat > ~/.picoclaw/config.json << 'EOF'
{
  "agents": {
    "defaults": {
      "workspace": "~/.picoclaw/workspace",
      "model_name": "gpt-4o-mini",
      "max_tokens": 2048,
      "temperature": 0.5,
      "max_tool_iterations": 10
    }
  },
  "model_list": [
    {
      "model_name": "gpt-4o-mini",
      "model": "openai/gpt-4o-mini",
      "api_key": "$OPENAI_API_KEY",
      "request_timeout": 120
    }
  ]
}
EOF

./picoclaw-linux-riscv64
```

### Pattern: Full-Stack Dev Assistant with Web Search

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/projects",
      "model_name": "claude-sonnet",
      "max_tokens": 8192,
      "temperature": 0.3,
      "max_tool_iterations": 30
    }
  },
  "model_list": [
    {
      "model_name": "claude-sonnet",
      "model": "anthropic/claude-sonnet-4-5",
      "api_key": "$ANTHROPIC_API_KEY",
      "request_timeout": 600
    }
  ],
  "tools": {
    "web": {
      "tavily": {
        "enabled": true,
        "api_key": "$TAVILY_API_KEY"
      }
    }
  }
}
```

### Pattern: Docker with Environment Variables

```yaml
# docker/docker-compose.override.yml
services:
  picoclaw-gateway:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - PICOCLAW_GATEWAY_HOST=0.0.0.0
```

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml --profile gateway up -d
```

### Pattern: Build for a Specific Target in Go

```bash
# Cross-compile for MIPS (OpenWRT routers)
GOOS=linux GOARCH=mips GOMIPS=softfloat go build -o build/picoclaw-linux-mips ./cmd/picoclaw

# Cross-compile for 32-bit ARM (older Raspberry Pi)
GOOS=linux GOARCH=arm GOARM=7 go build -o build/picoclaw-linux-arm ./cmd/picoclaw

# Cross-compile for RISC-V 64-bit
GOOS=linux GOARCH=riscv64 go build -o build/picoclaw-linux-riscv64 ./cmd/picoclaw
```

---

## Troubleshooting

### Binary won't execute on device

```bash
# Verify the binary matches the device architecture
file picoclaw-linux-arm64
uname -m   # Should match: aarch64 = arm64, x86_64 = amd64

# Ensure executable permission
chmod +x picoclaw-linux-arm64
```

### "Permission denied" on Termux

Termux requires `proot` for some system calls:

```bash
pkg install proot
termux-chroot ./picoclaw-linux-arm64 onboard
```

### API key not recognized

- Do not use `"api_key": "sk-..."` literals in config — set env vars and reference them as `"$OPENAI_API_KEY"`.
- Verify the env var is exported in your current shell: `echo $OPENAI_API_KEY`.

### Docker gateway not reachable from host

Set `PICOCLAW_GATEWAY_HOST=0.0.0.0` in the environment or in `config.json` before starting the container.

### High memory usage in recent versions

The project notes that recent PRs may push RAM usage to 10–20MB. If this is a concern on ultra-low-memory devices, pin to an earlier release tag:

```bash
git checkout v0.1.1
make build
```

### Config file location

Default: `~/.picoclaw/config.json`

Override at runtime:

```bash
picoclaw -config /path/to/custom-config.json
```

### Rebuild after dependency changes

```bash
cd picoclaw
make deps
make build
```

---

## Hardware Targets Quick Reference

| Device | Price | Binary |
|---|---|---|
| LicheeRV-Nano (E/W) | ~$10 | `picoclaw-linux-riscv64` |
| NanoKVM | ~$30–50 | `picoclaw-linux-riscv64` |
| MaixCAM / MaixCAM2 | ~$50–100 | `picoclaw-linux-arm64` |
| Raspberry Pi Zero 2 W (32-bit OS) | ~$15 | `picoclaw-linux-arm` |
| Raspberry Pi Zero 2 W (64-bit OS) | ~$15 | `picoclaw-linux-arm64` |
| Android via Termux | — | `picoclaw-linux-arm64` |
| Standard Linux x86_64 | — | `picoclaw-linux-amd64` |
