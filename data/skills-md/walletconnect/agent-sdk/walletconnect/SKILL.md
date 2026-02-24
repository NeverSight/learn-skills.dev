---
name: walletconnect
description: Manages the walletconnect CLI for wallet connection, session management, and message signing. Use when the user wants to connect a wallet, check session status, sign messages, or disconnect.
---

# WalletConnect CLI

## Goal

Operate the `walletconnect` CLI binary to connect wallets via QR code, inspect sessions, sign messages, and disconnect.

## When to use

- User asks to connect a wallet or scan a QR code
- User asks to check which wallet is connected (`whoami`)
- User asks to sign a message with their wallet
- User asks to disconnect their wallet session
- User mentions `walletconnect` CLI in context of wallet operations

## When not to use

- User wants to stake, unstake, or claim WCT rewards (use `walletconnect-staking` skill)
- User is working on the SDK source code itself (just edit normally)
- User wants to interact with a dApp or smart contract beyond signing

## Prerequisites

- Project ID must be configured (see below) for `connect` and `sign` commands
- Binary is at `packages/cli-sdk/dist/cli.js` (or globally linked as `walletconnect`)
- Build first if needed: `npm run build -w @walletconnect/cli-sdk`

## Project ID configuration

The project ID is resolved in this order: `WALLETCONNECT_PROJECT_ID` env var > `~/.walletconnect-cli/config.json`.

```bash
# Set globally (persists across sessions)
walletconnect config set project-id <id>

# Check current value
walletconnect config get project-id

# Or override per-command via env var
WALLETCONNECT_PROJECT_ID=<id> walletconnect connect
```

## Commands

```bash
# Connect a wallet (displays QR code in terminal)
walletconnect connect

# Connect via browser UI instead of terminal QR
walletconnect connect --browser

# Check current session
walletconnect whoami

# Sign a message
walletconnect sign "Hello, World!"

# Disconnect
walletconnect disconnect

# Manage config
walletconnect config set project-id <value>
walletconnect config get project-id
```

## Default workflow

1. Check project ID is configured: `walletconnect config get project-id`
2. Check if a session exists: `walletconnect whoami`
3. If not connected, connect: `walletconnect connect`
4. Perform the requested operation (sign, check status, etc.)
5. If done, optionally disconnect: `walletconnect disconnect`

## Important notes

- The `connect` and `sign` commands require a project ID — set it with `walletconnect config set project-id <id>` if not configured
- Sessions persist across invocations in `~/.walletconnect-cli/`
- `sign` auto-connects if no session exists
- The `--browser` flag opens a local web page with the QR code instead of rendering in terminal
- Always use a 60s+ timeout for commands that require wallet interaction (QR scan, signing)

## Validation checklist

- [ ] Project ID is configured (`walletconnect config get project-id`)
- [ ] Binary is built and linked (`walletconnect --help` works)
- [ ] Command output is shown to the user
- [ ] Timeouts are sufficient for wallet interaction (60s+)

## Examples

### Check session status
```
User: "Am I connected to a wallet?"
Action: Run `walletconnect whoami`
```

### Sign a message
```
User: "Sign the message 'verify-ownership' with my wallet"
Action: Run `walletconnect sign "verify-ownership"`
Note: Inform user to confirm in their wallet app
```
