---
name: nansen-wallet
description: Wallet management — create, list, show, export, send, delete. Use when creating wallets, checking balances, or sending tokens.
metadata:
  openclaw:
    requires:
      env:
        - NANSEN_API_KEY
      bins:
        - nansen
    primaryEnv: NANSEN_API_KEY
    install:
      - kind: node
        package: nansen-cli
        bins: [nansen]
allowed-tools: Bash(nansen:*)
---

# Wallet

## Auth Setup

```bash
# Save API key (non-interactive)
nansen login --api-key <key>
# Or via env var:
NANSEN_API_KEY=<key> nansen login

# Verify
nansen research profiler labels --address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --chain ethereum
```

## Wallet Creation (Two-Step Agent Flow)

Wallet creation requires a password from the **human user**. The agent must NOT generate or store the password itself.

> **Step 1 (Agent → Human):** Ask the user to provide a wallet password (minimum 12 characters).
>
> **Step 2 (Agent executes):** Run the create command with the password the user gave you.

```bash
NANSEN_WALLET_PASSWORD="<password_from_user>" nansen wallet create
```

After creation, the CLI automatically saves the password:
- **OS keychain** (macOS Keychain, Linux secret-tool, Windows Credential Manager) — secure, preferred
- **~/.nansen/wallets/.credentials file** — insecure fallback when no keychain is available (e.g. containers, CI)

**All future wallet operations retrieve the password automatically** — no env var or human input needed.

If the `.credentials` file fallback is used, the CLI prints a warning on every operation. To migrate to secure storage later, run `nansen wallet secure`.

### Password resolution order (automatic)

1. `NANSEN_WALLET_PASSWORD` env var (if set)
2. OS keychain (saved automatically on wallet create)
3. `~/.nansen/wallets/.credentials` file (insecure fallback, with warning)
4. Structured JSON error with instructions (if none available)

### Critical rules for agents

- **NEVER generate a password yourself** — always ask the human user
- **NEVER store the password** in files, memory, logs, or conversation history
- **NEVER use `--human` flag** — that enables interactive prompts which agents cannot handle
- After wallet creation, you do NOT need the password for future operations — the keychain handles it
- If you get a `PASSWORD_REQUIRED` error, ask the user to provide their password again

## Create

```bash
# Ask the user for a password first, then:
NANSEN_WALLET_PASSWORD="<password_from_user>" nansen wallet create
# Or with a custom name:
NANSEN_WALLET_PASSWORD="<password_from_user>" nansen wallet create --name trading
```

## List & Show

```bash
nansen wallet list
nansen wallet show <name>
nansen wallet default <name>
```

## Send

```bash
# Send native token (SOL, ETH) — password auto-resolved from keychain
nansen wallet send --to <addr> --amount 1.5 --chain solana

# Send entire balance
nansen wallet send --to <addr> --chain evm --max

# Dry run (preview, no broadcast)
nansen wallet send --to <addr> --amount 1.0 --chain evm --dry-run
```

## Export & Delete

```bash
# Password auto-resolved from keychain
nansen wallet export <name>
nansen wallet delete <name>
```

## Forget Password

```bash
# Remove saved password from all stores (keychain + .credentials file)
nansen wallet forget-password
```

## Migrate to Secure Storage

```bash
nansen wallet secure
```

For detailed migration steps (from `~/.nansen/.env`, `.credentials`, or env-var-only setups), see the **nansen-wallet-migration** skill.

## Flags

| Flag | Purpose |
|------|---------|
| `--to` | Recipient address |
| `--amount` | Amount to send |
| `--chain` | `evm` or `solana` |
| `--max` | Send entire balance |
| `--dry-run` | Preview without broadcasting |
| `--human` | Enable interactive prompts (human terminal use only — agents must NOT use this) |
| `--unsafe-no-password` | Skip encryption (keys stored in plaintext — NOT recommended) |

## Environment Variables

| Var | Purpose |
|-----|---------|
| `NANSEN_WALLET_PASSWORD` | Wallet encryption password — only needed for initial `wallet create`. After that, the OS keychain handles it. |
| `NANSEN_API_KEY` | API key (also set via `nansen login --api-key <key>`) |
| `NANSEN_EVM_RPC` | Custom EVM RPC endpoint |
| `NANSEN_SOLANA_RPC` | Custom Solana RPC endpoint |
