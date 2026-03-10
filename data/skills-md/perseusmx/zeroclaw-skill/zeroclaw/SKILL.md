---
name: zeroclaw
description: Configure and operate ZeroClaw autonomous AI infrastructure. Use when user mentions zeroclaw CLI, needs to setup/configure zeroclaw, asks about 'zeroclaw providers', 'zeroclaw channels', 'autonomous AI agent', or wants to run LLMs on low-cost hardware (Raspberry Pi, ESP32, Arduino).
license: MIT
---

# ZeroClaw Quick Reference

ZeroClaw is a fast, small (<5MB RAM), fully autonomous AI assistant infrastructure built in Rust.

**Core Characteristics:**
- Single binary (~8.8MB release), no runtime dependencies
- <10ms cold start, 16+ communication channels
- Runs on $10 hardware (ARM, x86, RISC-V)
- Config: `~/.zeroclaw/config.toml`
- Workspace: `~/.zeroclaw/workspace/`
- Auth profiles: `~/.zeroclaw/auth-profiles.json` (encrypted)

---

# Installation

## Install

```bash
# Homebrew (macOS/Linux)
brew install zeroclaw

# Clone + bootstrap (recommended — inspect before running)
git clone https://github.com/zeroclaw-labs/zeroclaw.git
cd zeroclaw && ./bootstrap.sh

# Bootstrap options: --prefer-prebuilt, --prebuilt-only, --docker, --onboard
```

## Update

```bash
git clone https://github.com/zeroclaw-labs/zeroclaw.git /tmp/zeroclaw-update
cd /tmp/zeroclaw-update && bash scripts/bootstrap.sh --prefer-prebuilt
rm -rf /tmp/zeroclaw-update
zeroclaw --version
```

## Onboarding

```bash
ZEROCLAW_API_KEY="..." zeroclaw onboard --provider openrouter
zeroclaw onboard --interactive    # Full wizard
zeroclaw onboard --channels-only  # Reconfigure channels only
```

---

# Essential Commands

## Daily Use

- `zeroclaw agent` - Interactive AI chat
- `zeroclaw agent -m "message"` - Single message
- `zeroclaw daemon` - Full autonomous runtime

## Diagnostics

- `zeroclaw status` - Check system status
- `zeroclaw doctor` - Run full diagnostics
- `zeroclaw channel doctor` - Check channel health

## Providers & Models

- `zeroclaw providers` - List all providers
- `zeroclaw models refresh` - Refresh model catalogs
- `zeroclaw models refresh --provider <ID>` - Refresh specific provider

## Channels

- `zeroclaw channel list` - List all channels
- `zeroclaw channel start` - Start channels
- `zeroclaw channel start <channel>` - Start specific channel

## Service

- `zeroclaw service install` - Install as system service
- `zeroclaw service start/stop/restart` - Control service

## Other

- `zeroclaw completions bash|zsh` - Generate shell completions
- `zeroclaw migrate openclaw [--dry-run]` - Import from OpenClaw
- `zeroclaw gateway [--port 0]` - Start webhook gateway (port 0 = random)

---

# Providers Overview

ZeroClaw supports 10+ built-in providers plus custom endpoints.

**Built-in providers:**
- `openrouter` - OpenRouter (default, multi-provider aggregation)
- `anthropic` - Anthropic Claude models
- `openai` / `openai-codex` - OpenAI (API key / OAuth)
- `groq`, `xai`, `together`, `deepseek` - Cloud providers
- `ollama`, `lmstudio`, `llamacpp`, `vllm`, `osaurus` - Local servers
- `custom:<URL>` / `anthropic-custom:<URL>` - Any compatible endpoint

**See complete catalog:** [PROVIDERS.md](references/PROVIDERS.md)

**Quick custom provider setup:**

```toml
# ~/.zeroclaw/config.toml
default_provider = "custom:https://your-api.example.com"
# api_key resolved from $ZEROCLAW_API_KEY env var (recommended) or set here
default_model = "your-model"
```

---

# Channels Overview

ZeroClaw supports 16+ communication channels.

| Channel | Access Control | Quick Setup |
|---|---|---|
| CLI | n/a | Built-in |
| Telegram | `allowed_users` | `zeroclaw onboard` |
| Discord | `allowed_users` | `zeroclaw onboard` |
| Slack | `allowed_users` | `zeroclaw onboard` |
| Mattermost | `allowed_users` | Manual config |
| WhatsApp | `allowed_numbers` | `zeroclaw onboard` (Web + Cloud API) |
| Signal | `allowed_from` | Manual config |
| iMessage | `allowed_contacts` | macOS only |
| Matrix | `allowed_users` | Manual config |
| Email | `allowed_senders` | Manual config |
| IRC | `allowed_users` | `zeroclaw onboard` |
| Lark | `allowed_users` | Manual config |
| DingTalk | `allowed_users` | `zeroclaw onboard` |
| QQ | `allowed_users` | Manual config |
| Linq | `allowed_senders` | Manual config |
| Nostr | `allowed_pubkeys` | Manual config |
| Webhook | `secret` | Manual/onboard |

**See detailed channel-by-channel setup:** [CHANNELS.md](references/CHANNELS.md)

<security-warning>
**⚠️ SECURITY**: All channels use deny-by-default. Empty arrays deny all access, `["*"]` allows all. Only allow trusted users/contacts to prevent unauthorized access.
</security-warning>

---

# Configuration Overview

ZeroClaw uses `~/.zeroclaw/config.toml` for all settings.

**Basic provider setup:**

```toml
default_provider = "openrouter"
# api_key resolved from $ZEROCLAW_API_KEY env var (recommended) or set here (encrypted at rest)
default_model = "anthropic/claude-sonnet-4.5"
default_temperature = 0.7
```

**Autonomy levels:**

| Level | Description |
|---|---|
| `readonly` | Can read files only, no modifications |
| `supervised` | Requires approval for file writes, shell commands, network requests |
| `full` | No approval required (use only on trusted machines) |

```toml
[autonomy]
level = "supervised"
workspace_only = true
allowed_commands = ["git", "npm", "cargo", "ls", "cat"]
max_actions_per_hour = 20
max_cost_per_day_cents = 500
```

<security-warning>
**⚠️ HIGH RISK**: Setting `level = "full"` removes all guardrails. Only use on trusted, personal machines. The AI can execute any command without approval.
</security-warning>

**Common security settings:**

```toml
# Restrict to workspace only (recommended)
[autonomy]
workspace_only = true
allowed_paths = ["/path/to/project"]

# Set cost limits
[autonomy]
max_cost_per_day_cents = 500
max_actions_per_hour = 20

# Block dangerous commands
[autonomy]
blocked_commands = ["rm -rf", "dd", "mkfs"]
```

**See complete config reference:** [CONFIG.md](references/CONFIG.md)
**See security best practices:** [SECURITY.md](references/SECURITY.md)

---

# Troubleshooting

## Quick Diagnostics

```bash
zeroclaw --version
zeroclaw status
zeroclaw doctor
zeroclaw channel doctor
```

## Common Issues

| Problem | Solution |
|---|---|
| `cargo` not found | Run `./bootstrap.sh --install-rust` |
| `zeroclaw` command not found | Add to PATH: `export PATH="$HOME/.cargo/bin:$PATH"` |
| Gateway unreachable | Check `gateway.host`/`port` in config.toml |
| Telegram "terminated by other getUpdates" | Stop extra daemons (only one per bot token) |
| Channel unhealthy | Run `zeroclaw channel doctor`, verify credentials and permissions |
| Config world-readable warning | Run `chmod 600 ~/.zeroclaw/config.toml` |
| API authentication failed | Verify API key in config or environment variables |
| Model not found | Run `zeroclaw models refresh` to update catalog |
| High memory usage | Check autonomy settings, limit concurrent actions |

## Logs

- macOS/Windows: `~/.zeroclaw/logs/daemon.stdout.log`
- Linux systemd: `journalctl --user -u zeroclaw.service -f`

## Getting Help

1. Run `zeroclaw doctor` for automated diagnostics
2. Check logs for error messages
3. Review config: `cat ~/.zeroclaw/config.toml`
4. Full documentation: https://github.com/zeroclaw-labs/zeroclaw

