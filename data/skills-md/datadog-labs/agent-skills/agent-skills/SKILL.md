---
name: agent-skills
description: Datadog skills for AI agents. Essential monitoring, logging, tracing and observability.
metadata:
  version: "1.0.0"
---

# Datadog Skills

Essential Datadog skills for AI agents.

## Core Skills

| Skill | Description |
|-------|-------------|
| **dd-pup** | Primary CLI - all pup commands, auth, PATH setup |
| **dd-monitors** | Create, manage, mute monitors and alerts |
| **dd-logs** | Search logs, pipelines, archives |
| **dd-apm** | Traces, services, performance analysis |
| **dd-docs** | Search Datadog documentation |

## Install

```bash
# Install core skills
npx skills add datadog-labs/agent-skills \
  --skill dd-pup \
  --skill dd-monitors \
  --skill dd-logs \
  --skill dd-apm \
  --skill dd-docs \
  --full-depth -y
```

## Prerequisites

```bash
# Install pup CLI
go install github.com/DataDog/pup@latest
export PATH="$HOME/go/bin:$PATH"

# Authenticate
pup auth login
```

## Quick Reference

| Task | Command |
|------|---------|
| Search error logs | `pup logs search --query "status:error" --duration 1h` |
| List monitors | `pup monitors list` |
| Mute a monitor | `pup monitors mute --id 123 --duration 1h` |
| Find slow traces | `pup apm traces list --service api --min-duration 500ms` |
| Query metrics | `pup metrics query --query "avg:system.cpu.user{*}"` |
| Check auth | `pup auth status` |
| Refresh token | `pup auth refresh` |

## Auth

```bash
pup auth login          # OAuth2 (recommended)
pup auth status         # Check token
pup auth refresh        # Refresh expired token
```

**⚠️ Token Expiry**: OAuth tokens expire (~1 hour). Run `pup auth refresh` if commands fail with 401/403.

## More Skills

Additional skills available shortly.

```bash
npx skills add datadog-labs/agent-skills --list --full-depth
```
