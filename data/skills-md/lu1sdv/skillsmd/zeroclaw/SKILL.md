---
name: zeroclaw
description: This skill should be used when building, configuring, deploying, or troubleshooting ZeroClaw AI agent infrastructure — including provider setup, channel binding, memory backends, config.toml authoring, CLI usage, Docker/native runtime, and migration from other agent frameworks
---

# ZeroClaw

Rust-based autonomous AI assistant infrastructure. Runtime OS for agentic workflows — deploy anywhere, swap anything. Runs on <5MB RAM, <10ms startup, ~8.8MB binary.

- Repo: https://github.com/zeroclaw-labs/zeroclaw
- Docs: https://github.com/zeroclaw-labs/zeroclaw/blob/main/docs/README.md

## Quick Reference

| Command | Purpose |
|---------|---------|
| `zeroclaw onboard --interactive` | First-time setup wizard |
| `zeroclaw agent -m "msg"` | Single message |
| `zeroclaw agent` | Interactive REPL |
| `zeroclaw daemon` | Full autonomous runtime + channels |
| `zeroclaw gateway` | Webhook server (default :42617) |
| `zeroclaw status` | Check daemon & config |
| `zeroclaw doctor` | System diagnostics |
| `zeroclaw channel doctor` | Channel health check |
| `zeroclaw channel bind-telegram <id>` | Bind Telegram chat |
| `zeroclaw providers` | List available providers |
| `zeroclaw auth login --provider <p> --device-code` | OAuth login |
| `zeroclaw auth setup-token --provider <p>` | Token auth |
| `zeroclaw service install` | Install as system service |
| `zeroclaw migrate openclaw --dry-run` | Preview migration |
| `zeroclaw completions <shell>` | Shell completions |

## Installation

```bash
# Homebrew
brew install zeroclaw

# Bootstrap (local clone)
git clone https://github.com/zeroclaw-labs/zeroclaw.git && cd zeroclaw && ./bootstrap.sh

# Remote bootstrap
curl -fsSL https://raw.githubusercontent.com/zeroclaw-labs/zeroclaw/main/scripts/bootstrap.sh | bash

# From source
cargo build --release --locked && cargo install --path . --force --locked

# Pre-built binaries: GitHub Releases (Linux x86_64/aarch64/armv7, macOS, Windows)
# Bootstrap flags: --prefer-prebuilt, --prebuilt-only, --docker
```

**Build requirements:** 2GB+ RAM+swap, 6GB+ disk. Runtime: <5MB.

## Configuration

Edit `~/.zeroclaw/config.toml`. Core sections:

```toml
[providers]
# OpenAI, Anthropic, OpenRouter, Google, Mistral, xAI, DeepSeek, 70+ more
# Set via env: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.

[memory]
backend = "sqlite"  # "postgres", "markdown", "lucid", "none"
# Built-in vector search (BLOBs + cosine similarity) + FTS5 keyword search
# No external vector DB needed — hybrid merge of vector + BM25

[runtime]
kind = "native"  # "docker" for sandboxed execution

[channels]
# CLI, Telegram, Discord, Slack, Matrix, Signal, IRC, Email, iMessage,
# WhatsApp, Mattermost, Lark, DingTalk, QQ, Linq, Nostr, Webhook

[security]
# allowlists, pairing, rate_limits, filesystem_scoping

[autonomy]
level = "full"                          # "supervised" (default) or "full"
max_actions_per_hour = 999999           # ⚠️ MUST be > 0 or daemon silently fails
max_cost_per_day_cents = 999999         # same
require_approval_for_medium_risk = false
block_high_risk_commands = false
```


## Architecture

**Trait-driven — every subsystem is swappable:**

| Layer | Swappable Options |
|-------|-------------------|
| **Providers** | OpenAI, Anthropic, OpenRouter, Google, custom endpoints |
| **Channels** | 18+ (CLI, Telegram, Discord, Slack, Matrix, etc.) |
| **Memory** | SQLite (default), PostgreSQL, Markdown, Lucid, none |
| **Tools** | Shell, file ops, Git, HTTP, screenshots, browser |
| **Runtime** | Native, Docker sandbox |

## Authentication

```bash
OPENAI_API_KEY=sk-... zeroclaw agent                              # env var
zeroclaw auth login --provider openai-codex --device-code         # OAuth device flow
zeroclaw auth paste-token --provider anthropic --profile default  # token paste
```

Profiles stored encrypted at `~/.zeroclaw/auth-profiles.json` (key: `~/.zeroclaw/.secret_key`). Manage with `auth use`, `auth status`, `auth refresh` (see Quick Reference).

**WARNING (Feb 2026):** Claude Code OAuth tokens (Free/Pro/Max) are restricted to Claude Code/Claude.ai only. Do NOT use them via ZeroClaw — violates Anthropic ToS.

## Memory System

Built-in full-stack search engine (no external vector DB):

- **Vector**: Embeddings as BLOBs in SQLite, cosine similarity
- **Keyword**: FTS5 virtual tables, BM25 scoring
- **Hybrid**: Weighted merge of vector + keyword results
- **Embeddings**: OpenAI, custom URL, or noop
- **Chunking**: Line-based markdown with heading preservation
- **Cache**: SQLite LRU embedding cache
- **Reindex**: Atomic FTS5 rebuild + missing vector re-embedding

The agent manages memory automatically via built-in tools.

## Common Patterns

### Deploy as daemon with Telegram
```bash
zeroclaw onboard --interactive          # configure provider + channel
zeroclaw channel bind-telegram 123456   # bind chat ID
zeroclaw daemon                         # start autonomous runtime
```

### Webhook gateway
```bash
zeroclaw gateway --port 8080            # or --port 0 for random
```

### Docker sandbox
```toml
# config.toml
[runtime]
kind = "docker"
```

### Migration from OpenClaw
```bash
zeroclaw migrate openclaw --dry-run     # preview changes
zeroclaw migrate openclaw               # execute migration
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build OOM | Use `--prefer-prebuilt` or add swap (need 2GB+) |
| Channel not responding | `zeroclaw channel doctor` |
| Auth expired | `zeroclaw auth refresh --provider <p>` |
| Config issues | `zeroclaw doctor` |
| Gateway unreachable | Check port binding, firewall, pairing config |
| Memory search poor | Check embedding provider config, run reindex |
| Config schema JSON parse fails | `zeroclaw config schema` mixes INFO log lines with JSON — save to file and strip the log line first |
| Config changes not applied | `zeroclaw service restart` (or `zeroclaw service stop && zeroclaw service start`) then `zeroclaw doctor` |

## Security

Supports gateway pairing, Docker sandboxing, allowlists (tools/files/channels), rate limiting, filesystem scoping, and encrypted secrets at rest.
