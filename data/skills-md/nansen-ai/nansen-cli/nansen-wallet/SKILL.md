---
name: nansen-wallet
description: Wallet management — create, list, show, export, send, delete. Use when creating wallets, checking balances, or sending tokens.
allowed-tools: Bash
---

# Wallet

## Auth Setup

```bash
# API key (persistent — recommended)
nansen login
# Or non-interactive:
NANSEN_API_KEY=<key> nansen login

# Verify
nansen research profiler labels --address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --chain ethereum
```

## Password Policy (Agents)

> **CRITICAL: Never hold a wallet password only in memory.**

Wallets are encrypted with AES-256-GCM. A lost password means permanently locked funds — there is no recovery mechanism. Passwords must be persisted to `~/.nansen/.env` so they survive session restarts.

- Never echo or display the password in conversation history
- Never hold a password only in session memory — always persist to `~/.nansen/.env` first

### Setup flow (before first wallet operation)

```bash
# 1. Ensure ~/.nansen exists
mkdir -p ~/.nansen

# 2. Check if password is already configured (env var OR file)
source ~/.nansen/.env 2>/dev/null
if [ -z "$NANSEN_WALLET_PASSWORD" ] && ! grep -q 'NANSEN_WALLET_PASSWORD' ~/.nansen/.env 2>/dev/null; then
  # 3. Generate a strong password and persist it
  NANSEN_WALLET_PASSWORD=$(openssl rand -base64 24)
  echo "export NANSEN_WALLET_PASSWORD=\"$NANSEN_WALLET_PASSWORD\"" >> ~/.nansen/.env
  chmod 600 ~/.nansen/.env
fi
```

Key rules:
- **Generate + persist is fine** — the password lives in `~/.nansen/.env`, not in agent memory
- If `~/.nansen/.env` already has a password, **always use the existing one** — never overwrite
- If the file already exists but has no password, **append** (don't overwrite other vars)

### For all wallet commands

Always source the env file before running wallet operations:
```bash
source ~/.nansen/.env && nansen wallet <command>
```

## Create

```bash
# Source password from .env (auto-generated if needed), then create
source ~/.nansen/.env && nansen wallet create
```

## List & Show

```bash
nansen wallet list
nansen wallet show <name>
nansen wallet default <name>
```

## Send

```bash
# Send native token (SOL, ETH)
nansen wallet send --to <addr> --amount 1.5 --chain solana

# Send entire balance
nansen wallet send --to <addr> --chain evm --max

# Dry run (preview, no broadcast)
nansen wallet send --to <addr> --amount 1.0 --chain evm --dry-run
```

## Export & Delete

```bash
nansen wallet export <name>
nansen wallet delete <name>
```

## Flags

| Flag | Purpose |
|------|---------|
| `--to` | Recipient address |
| `--amount` | Amount to send |
| `--chain` | `evm` or `solana` |
| `--max` | Send entire balance |
| `--dry-run` | Preview without broadcasting |

## Environment Variables

| Var | Purpose |
|-----|---------|
| `NANSEN_WALLET_PASSWORD` | **Required for agents.** Wallet encryption password — auto-generated and persisted to `~/.nansen/.env` on first use (see Password Policy) |
| `NANSEN_API_KEY` | API key (also set via `nansen login`) |
| `NANSEN_EVM_RPC` | Custom EVM RPC endpoint |
| `NANSEN_SOLANA_RPC` | Custom Solana RPC endpoint |
