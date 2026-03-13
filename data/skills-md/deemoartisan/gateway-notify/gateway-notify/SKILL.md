---
name: gateway-notify
description: "Set up automatic notifications when OpenClaw gateway restarts. Use when user wants to be notified of gateway startup events via any messaging channel (iMessage, WhatsApp, Telegram, Discord, etc.)."
---

# Gateway Notify

Automatically send notifications when the OpenClaw gateway starts up.

## What It Does

Creates a hook that triggers on `gateway:startup` events and sends a notification message to the user's preferred channel with gateway status information.

## Quick Start

Run the setup script with the user's messaging channel and address:

```bash
scripts/setup_gateway_notify.sh <channel> <address>
```

Examples:
```bash
scripts/setup_gateway_notify.sh imessage user@example.com
scripts/setup_gateway_notify.sh whatsapp +1234567890
scripts/setup_gateway_notify.sh telegram @username
```

The script will:
1. Create the hook directory at `~/.openclaw/hooks/gateway-restart-notify`
2. Generate the handler with the specified channel configuration
3. Enable the hook in OpenClaw config
4. Restart the gateway to activate

## How It Works

The hook uses OpenClaw's internal hook system:
- Listens for `gateway:startup` events
- Collects gateway status (model, time, port)
- Sends notification via the configured channel CLI

## Supported Channels

See [CHANNELS.md](references/CHANNELS.md) for channel-specific CLI commands and address formats.

## Manual Setup

If you need to customize the hook, see [MANUAL.md](references/MANUAL.md) for step-by-step instructions.
