---
name: linear-webhooks
description: Manage webhooks - create, listen for events, rotate secrets. Use when setting up integrations or event listeners.
allowed-tools: Bash
---

# Webhooks

```bash
# List all webhooks
linear-cli wh list

# Create a webhook
linear-cli wh create https://example.com/hook --events Issue

# Get webhook details
linear-cli wh get WEBHOOK_ID

# Update a webhook
linear-cli wh update WEBHOOK_ID --url https://new-url.com

# Delete a webhook
linear-cli wh delete WEBHOOK_ID --force

# Rotate signing secret
linear-cli wh rotate-secret WEBHOOK_ID

# Listen for events locally (dev/testing)
linear-cli wh listen --port 9000
linear-cli wh listen --port 9000 --secret SIGNING_SECRET
```

## Subcommands

| Command | Purpose |
|---------|---------|
| `list` | List all webhooks |
| `get` | View webhook details |
| `create` | Create webhook |
| `update` | Update webhook |
| `delete` | Delete webhook |
| `rotate-secret` | Rotate signing secret |
| `listen` | Local event listener with HMAC verification |

## Flags

| Flag | Purpose |
|------|---------|
| `--events TYPE` | Event types to subscribe |
| `--port N` | Local listener port |
| `--secret KEY` | HMAC signing secret |
| `--output json` | JSON output |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
