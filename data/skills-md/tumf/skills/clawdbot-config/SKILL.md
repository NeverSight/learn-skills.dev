---
name: clawdbot-config
description: Comprehensive Clawdbot configuration and skills system management. Use when working with Clawdbot setup, configuration files, creating/modifying AgentSkills-compatible skills with YAML frontmatter, troubleshooting agent behavior, managing channels, workspace, sandbox, or multi-agent routing.
---

# Clawdbot Configuration Expert

Expert guidance for Clawdbot's configuration system, skills management, and agent setup.

## When to Use This Skill

Use this skill when you need to:

- **Configure Clawdbot**: Set up `~/.clawdbot/clawdbot.json` with agents, channels, gateway, or tools
- **Create Skills**: Build AgentSkills-compatible `SKILL.md` with proper YAML frontmatter and metadata
- **Manage Skills**: Configure skill loading, gating, environment injection, or installation
- **Troubleshoot**: Diagnose configuration issues, skill loading problems, or agent behavior
- **Understand System**: Learn about workspace structure, bootstrap files, or session management
- **Deep Dive**: Access complete documentation archive (370+ files) for channels, automation, webhooks, cron jobs, gateway protocols, platform-specific guides, and advanced features

## Quick Decision Tree

```
Need to configure Clawdbot?
├─ Setting up for first time? → See "Quick Start Guide"
├─ Managing skills? → See "Skills Management"
├─ Configuring channels? → See "Channel Configuration"
├─ Setting up remote access? → See "Remote Gateway Setup"
└─ Creating a skill? → See "Creating Skills"

Need examples?
└─ See references/config-examples.md for common patterns

Need deep documentation?
├─ Channel-specific setup? → See references/repomix-output.xml (channels/)
├─ Automation (cron, webhooks)? → See references/repomix-output.xml (automation/)
├─ Gateway protocols? → See references/repomix-output.xml (gateway/)
├─ Platform guides? → See references/repomix-output.xml (platforms/)
└─ CLI reference? → See references/repomix-output.xml (cli/)
```

## Quick Start Guide

### Initial Setup

1. **Create minimal config** (`~/.clawdbot/clawdbot.json`):

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Projects/my-agent-workspace"
    }
  },
  "channels": {
    "whatsapp": {
      "allowFrom": ["+1555555YOUR_NUMBER"]
    }
  }
}
```

2. **Initialize workspace**:

```bash
clawdbot setup
```

This creates bootstrap files:
- `AGENTS.md` - Operating instructions
- `SOUL.md` - Persona and boundaries
- `TOOLS.md` - Tool usage notes
- `IDENTITY.md` - Agent identity
- `USER.md` - User profile

3. **Pair WhatsApp**:

```bash
clawdbot channels login
```

4. **Start gateway**:

```bash
clawdbot gateway
```

### Configuration File Location

- **Primary**: `~/.clawdbot/clawdbot.json`
- **Override**: `CLAWDBOT_CONFIG_PATH` environment variable
- **Format**: JSONC (JSON with Comments)

## Core Configuration Areas

### 1. Agents Configuration

Controls the embedded agent runtime.

**Minimal**:
```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Projects/my-workspace",
      "model": "anthropic/claude-sonnet-4"
    }
  }
}
```

**With sandbox**:
```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Projects/my-workspace",
      "sandbox": {
        "enabled": true,
        "docker": {
          "image": "clawdbot/sandbox:latest",
          "setupCommand": "apt-get update && apt-get install -y python3-pip",
          "env": {
            "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
          }
        }
      }
    }
  }
}
```

**Key fields**:
- `workspace` (required): Agent's working directory
- `model`: Primary model (format: `provider/model`)
- `sandbox`: Docker isolation configuration
- `blockStreamingDefault`: Streaming behavior (`"on"` | `"off"`)

See [references/config-schema.md](./references/config-schema.md#agents-configuration) for complete options.

### 2. Skills Configuration

Manage skill loading, filtering, and configuration.

**Basic**:
```jsonc
{
  "skills": {
    "allowBundled": ["gemini", "browser"],
    "entries": {
      "gemini": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

**Advanced**:
```jsonc
{
  "skills": {
    "load": {
      "extraDirs": ["~/Projects/custom-skills/skills"],
      "watch": true,
      "watchDebounceMs": 250
    },
    "install": {
      "preferBrew": true,
      "nodeManager": "pnpm"
    },
    "entries": {
      "nano-banana-pro": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}",
        "config": {
          "model": "gemini-3-pro-image"
        }
      }
    }
  }
}
```

**Skill precedence** (highest to lowest):
1. `<workspace>/skills`
2. `~/.clawdbot/skills`
3. `skills.load.extraDirs`
4. Bundled skills

See [references/skills-system.md](./references/skills-system.md) for complete skills documentation.

### 3. Channels Configuration

Configure WhatsApp, Telegram, Discord, iMessage, and other channels.

**WhatsApp**:
```jsonc
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"],
      "groups": {
        "*": { "requireMention": true }
      }
    }
  }
}
```

**Multi-channel**:
```jsonc
{
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123"]
    },
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "allowFrom": ["alice", "bob"]
    },
    "discord": {
      "enabled": true,
      "botToken": "${DISCORD_BOT_TOKEN}"
    }
  }
}
```

### 4. Gateway Configuration

WebSocket server and remote access.

**Local** (default):
```jsonc
{
  "gateway": {
    "port": 18789,
    "host": "127.0.0.1"
  }
}
```

**Remote** (Tailscale):
```jsonc
{
  "gateway": {
    "port": 18789,
    "bind": "tailnet",
    "auth": {
      "token": "${GATEWAY_AUTH_TOKEN}"
    }
  }
}
```

Start with:
```bash
clawdbot gateway --bind tailnet --token $GATEWAY_AUTH_TOKEN
```

### 5. Tools Configuration

Control tool behavior and permissions.

```jsonc
{
  "tools": {
    "exec": {
      "security": "ask",  // "allow" | "ask" | "deny"
      "applyPatch": true
    },
    "browser": {
      "enabled": true,
      "profilePath": "~/.clawdbot/browser-profile"
    }
  }
}
```

## Skills Management

### Creating a Skill

**Skill structure**:
```
my-skill/
├── SKILL.md          (required: frontmatter + instructions)
├── scripts/          (optional: executable code)
├── references/       (optional: detailed docs)
└── assets/           (optional: templates, files)
```

**SKILL.md format**:

```markdown
---
name: my-skill
description: What the skill does and when to use it. Be specific about triggers.
metadata: {"clawdbot":{"requires":{"bins":["python3"],"env":["MY_API_KEY"]},"primaryEnv":"MY_API_KEY"}}
---

# My Skill

## Quick Start

Instructions for using this skill...

## Resources

Scripts: python3 "$SKILL_ROOT/scripts/process.py"
```

**Metadata for gating**:

```jsonc
{
  "clawdbot": {
    "emoji": "🔧",
    "requires": {
      "bins": ["python3", "pip"],
      "anyBins": ["npm", "pnpm"],
      "env": ["MY_API_KEY"],
      "config": ["browser.enabled"]
    },
    "primaryEnv": "MY_API_KEY",
    "os": ["darwin", "linux"],
    "install": [
      {
        "id": "brew",
        "kind": "brew",
        "formula": "my-tool",
        "bins": ["my-tool"],
        "label": "Install My Tool (brew)"
      }
    ]
  }
}
```

**Key principles**:
- `description` is the primary trigger mechanism
- Metadata enables load-time filtering
- Keep SKILL.md concise; use `references/` for details
- Test scripts by actually running them

### Skill Locations

**Per-agent** (highest precedence):
```
<workspace>/skills/my-skill/SKILL.md
```

**Shared** (all agents):
```
~/.clawdbot/skills/my-skill/SKILL.md
```

**Custom folders**:
```jsonc
{
  "skills": {
    "load": {
      "extraDirs": ["~/Projects/custom-skills/skills"]
    }
  }
}
```

### Configuring Skills

**Enable/disable and provide API keys**:

```jsonc
{
  "skills": {
    "entries": {
      "my-skill": {
        "enabled": true,
        "apiKey": "${MY_API_KEY}",
        "env": {
          "MY_API_KEY": "${MY_API_KEY}",
          "MY_ENDPOINT": "https://api.example.com"
        }
      },
      "disabled-skill": {
        "enabled": false
      }
    }
  }
}
```

**Bundled skills allowlist**:
```jsonc
{
  "skills": {
    "allowBundled": ["gemini", "browser", "peekaboo"]
  }
}
```

### Skills in Sandbox

When agent is sandboxed, skills run inside Docker.

**Requirements**:
- Binaries checked on host at load time
- Binaries must exist in container at runtime
- Install via `setupCommand`:

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "setupCommand": "apt-get update && apt-get install -y python3-pip && pip3 install ruff",
          "env": {
            "GEMINI_API_KEY": "${GEMINI_API_KEY}"
          }
        }
      }
    }
  }
}
```

**Important**: Global `skills.entries.<skill>.env` applies to host runs only. Use `sandbox.docker.env` for container.

## Channel Configuration

### WhatsApp

**Basic**:
```jsonc
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"]
    }
  }
}
```

**With groups**:
```jsonc
{
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123", "+15555550124"],
      "groups": {
        "*": {
          "requireMention": true
        },
        // Specific group (use group JID)
        "120363012345678@g.us": {
          "requireMention": false
        }
      }
    }
  },
  "messages": {
    "groupChat": {
      "mentionPatterns": ["@clawd", "hey clawd"]
    }
  }
}
```

**Pairing**:
```bash
clawdbot channels login
```

### Telegram

```jsonc
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "allowFrom": ["username1", "username2"]
    }
  }
}
```

**Get bot token**: Create bot with [@BotFather](https://t.me/BotFather)

### Discord

```jsonc
{
  "channels": {
    "discord": {
      "enabled": true,
      "botToken": "${DISCORD_BOT_TOKEN}",
      "allowFrom": ["user_id_1", "user_id_2"]
    }
  }
}
```

**Setup**: Create application at [Discord Developer Portal](https://discord.com/developers/applications)

### iMessage (macOS)

```jsonc
{
  "channels": {
    "imessage": {
      "enabled": true,
      "cliPath": "/opt/homebrew/bin/imsg",
      "dbPath": "~/Library/Messages/chat.db"
    }
  }
}
```

**Install**: `brew install steipete/tap/imsg`

## Remote Gateway Setup

### Tailscale

1. **Install Tailscale**: https://tailscale.com/download

2. **Generate token**:
```bash
clawdbot doctor --generate-gateway-token
```

3. **Update config**:
```jsonc
{
  "gateway": {
    "bind": "tailnet",
    "auth": {
      "token": "YOUR_TOKEN_HERE"
    }
  }
}
```

4. **Start gateway**:
```bash
clawdbot gateway --bind tailnet --token $GATEWAY_AUTH_TOKEN
```

5. **Connect from remote**:
```bash
export CLAWDBOT_GATEWAY_URL="ws://gateway-hostname.tailnet.ts.net:18789"
export CLAWDBOT_GATEWAY_TOKEN="your-token"

clawdbot tui
```

### SSH Tunnel

**On remote machine** (run gateway):
```bash
clawdbot gateway
```

**On local machine** (create tunnel):
```bash
ssh -L 18789:localhost:18789 user@remote-host

# In another terminal
clawdbot tui
```

## Multi-Agent Routing

Route different users/channels to specialized agents:

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/main",
      "model": "anthropic/claude-sonnet-4"
    },
    "list": [
      {
        "id": "reviewer",
        "workspace": "~/Clawdbot/reviewer",
        "routes": [
          { "channel": "telegram", "peer": "alice" }
        ],
        "tools": {
          "write": false,
          "exec": { "security": "deny" }
        }
      },
      {
        "id": "analyst",
        "workspace": "~/Clawdbot/analyst",
        "routes": [
          { "channel": "discord", "peer": "123456789012345678" }
        ]
      }
    ]
  }
}
```

**Routing rules**:
- Match by channel + peer
- Each agent has isolated workspace and sessions
- Agent-specific tool policies

## Troubleshooting

### Check Status

```bash
# Gateway reachability and quick summary
clawdbot status

# Show effective configuration
clawdbot configure --show

# Validate config syntax
clawdbot configure --validate

# Health checks and quick fixes
clawdbot doctor

# Deep health probes
clawdbot health --verbose
```

### View Logs

```bash
# Tail gateway logs
clawdbot logs --follow

# View specific number of lines
clawdbot logs --lines 100
```

### Common Issues

**Gateway won't start**:
- Check if port is already in use: `lsof -i :18789`
- Verify config syntax: `clawdbot configure --validate`
- Check logs: `clawdbot logs`

**Skills not loading**:
- Verify skill location: `clawdbot skills list`
- Check metadata requirements (bins, env, config)
- For sandboxed agents, ensure binaries exist in container

**WhatsApp not responding**:
- Check allowFrom list includes your number
- Verify QR code pairing: `clawdbot channels login`
- Check channel status: `clawdbot status`

**Remote connection fails**:
- Verify auth token is set correctly
- Check gateway bind mode: `clawdbot status`
- Test connectivity: `curl http://gateway-host:18789/__health`

## References

### Detailed Documentation

- **[Config Schema](./references/config-schema.md)**: Complete configuration reference with all options
- **[Skills System](./references/skills-system.md)**: In-depth skills documentation (metadata, gating, installation)
- **[Config Examples](./references/config-examples.md)**: Practical examples for common use cases
- **[Complete Documentation Archive](./references/repomix-output.xml)**: Full Clawdbot documentation (370+ files) including channels, automation, gateway, tools, platforms, and troubleshooting guides

### Quick Reference

**Config file**: `~/.clawdbot/clawdbot.json`

**Commands**:
```bash
clawdbot setup              # Initialize workspace
clawdbot gateway            # Start gateway
clawdbot configure --show   # View config
clawdbot status             # Check status
clawdbot doctor             # Health check
clawdbot skills list        # List skills
clawdbot channels login     # Pair WhatsApp
```

**Model format**: `provider/model` (e.g., `anthropic/claude-sonnet-4`)

**Skill precedence**: workspace → ~/.clawdbot/skills → extraDirs → bundled

**Dashboard**: http://127.0.0.1:18789/ (when gateway running)

## Best Practices

1. **Start minimal**: Only configure what you need
2. **Use allowFrom**: Restrict channel access from the start
3. **Separate concerns**: Use config includes for modular setup
4. **Version control**: Track workspace bootstrap files (`AGENTS.md`, etc.)
5. **Environment variables**: Store API keys in env vars, not config
6. **Test skills**: Run scripts manually before deploying
7. **Monitor logs**: Use `clawdbot logs --follow` during development
8. **Backup sessions**: Sessions stored in `~/.clawdbot/agents/<agent>/sessions/`

## Using the Documentation Archive

The complete documentation archive (`references/repomix-output.xml`) contains 370+ markdown files covering:

- **Channels**: WhatsApp, Telegram, Discord, iMessage (BlueBubbles), Signal, Slack, MS Teams, Matrix, and more
- **Automation**: Cron jobs, webhooks, Gmail Pub/Sub integration, polling
- **Gateway**: Remote access, Tailscale, authentication, health checks, sandboxing
- **Tools**: Browser automation, elevated exec, Firecrawl, slash commands, subagents
- **Platforms**: macOS, iOS, Android, Linux, Windows, Docker, Hetzner
- **Providers**: Anthropic, OpenAI, GitHub Copilot, OpenRouter, Deepgram, and more
- **Concepts**: Agent loop, sessions, memory, compaction, model failover, streaming
- **CLI**: Complete command reference for all `clawdbot` commands

**When to read the archive**:
- Setting up specific channels (e.g., BlueBubbles for iMessage, Telegram bots)
- Configuring automation (cron jobs, webhooks, Gmail watch)
- Troubleshooting channel-specific issues
- Understanding gateway protocols and remote access
- Platform-specific setup (macOS menu bar, iOS TestFlight, Android)
- Advanced features (OAuth monitoring, voice wake, location commands)

**How to use it**:
1. The archive is XML-formatted with clear file paths
2. Search for specific topics (e.g., "telegram", "webhook", "sandbox")
3. Each file section includes the full path and line numbers
4. Cross-reference with the directory structure at the top

## Getting Help

- **Documentation**: https://docs.clawd.bot
- **GitHub**: https://github.com/clawdbot/clawdbot
- **Skills Registry**: https://clawdhub.com
