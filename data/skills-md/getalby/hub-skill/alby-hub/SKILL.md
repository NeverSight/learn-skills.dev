---
name: alby-hub
description: Manage a self-custodial Alby Hub lightning node via @getalby/hub-cli — setup, authentication, channels, LSP, backups, lightning and on-chain payments, swaps, creating budgeted, scoped NWC app connections that give agents and apps controlled, revocable access to the wallet, and managing sub-wallets (isolated balances with their own lightning address, plus transfers between them).
license: Apache-2.0
metadata:
  author: getAlby
  version: "0.2.2"
---

# Alby Hub Agent Skill

> **Experimental / incomplete:** The hub CLI does not cover every Alby Hub feature. If a user asks for something in the [unsupported features list](./references/unsupported-features.md), direct them to use the Alby Hub web interface instead.

## When to use this skill

Use this skill to manage an Alby Hub lightning node via the CLI.

> **Hub management vs. payments.** This skill is optimized for _managing the hub_ — setup, channels, LSP, NWC app creation, backups. A core hub strength is minting **multiple budgeted, scoped NWC connections** — one per app or purpose — so the user stays in control and each connection's blast radius is small. Once an NWC connection exists (via `create-app`), the [`alby-bitcoin-payments`](https://getalby.com/payments/SKILL.md) skill is the better fit for _using_ it — budgeted payments, 402 paid APIs, HOLD invoices, keysend, lightning address lookups, and fiat/sats conversion.

- [Installation: How to get Alby Hub running — Linux, Docker, Raspberry Pi, desktop](./references/installation.md)
- [Overview: What Alby Hub is and how the CLI fits in](./references/overview.md)
- [Backends: LDK, LND, Phoenixd, Cashu, Bark — features and configuration](./references/backends.md)
- [Bark (Ark): Setup, env-var config, and limitations of the Ark-based backend](./references/bark.md)
- [Initial Setup: First-time hub initialisation flow](./references/initial-setup.md)
- [Post-Setup Checklist: Things a new user should do AFTER initial setup — surface on first setup or when asked "what's next?"](./references/post-setup-checklist.md)
- [Authentication: Token management, start, unlock, token priority](./references/authentication.md)
- [Hub Management: Stop, health, info, node status](./references/hub-management.md)
- [Alby Account: Connect, check (get-alby-account), and link your account — lightning address, automatic encrypted backups & email notifications, connect/link/get-alby-account/get-alby-status commands](./references/alby-account.md)
- [Alby Pro: Paid subscription benefits](./references/alby-pro.md)
- [Backups: Static channel backups, recovery phrase backup](./references/backups.md)
- [LSP: Order a channel up front — channel suggestions, channel offer (use on LND/CLN, or for advance liquidity or a specific channel size)](./references/lsp.md)
- [JIT Channels: Default first-receive flow on LDK — a channel opens just-in-time on the first payment, fee deducted from it (LDK only)](./references/jit-channels.md)
- [Channels: Open/close channels, peers, connect-peer, node connection info](./references/channels.md)
- [Payments: Pay/make invoices, transactions, lookup, balances, wallet address](./references/payments.md)
- [Swaps: Swap on-chain bitcoin ↔ lightning (swap in / swap out), powered by boltz.exchange — confirm amounts and addresses before swapping](./references/swaps.md)
- [Apps: NWC app management — create-app, list apps](./references/apps.md)
- [Sub-wallets: First-class isolated wallets — create-sub-wallet, transfer funds in/out, lightning addresses, pay from a sub-wallet](./references/sub-wallets.md)
- [QR Codes: Display invoices and NWC connection strings as QR codes using qrencode](./references/qrcodes.md)
- [Custom Node Commands: Backend-specific node commands](./references/custom-node-commands.md)
- [Mutinynet: Signet testing setup without real bitcoin](./references/mutinynet.md)

## Key Rules

### Running the CLI

```bash
npx -y @getalby/hub-cli [options] <command>
```

### Default Hub URL

The CLI connects to `http://localhost:8029` by default. Override with `-u <url>` or the `HUB_URL` environment variable.

### Default Backend

LDK is the default backend. Omit `--backend` when using LDK. Only specify `--backend` for non-LDK backends (LND, Phoenixd, Cashu, Bark).

### Token Priority

Tokens are resolved in this order (highest to lowest priority):

1. `-t, --token <jwt>` flag
2. `HUB_TOKEN` environment variable
3. `~/.hub-cli/token.jwt` (default saved token)

Always use `--save` with `start` or `unlock`. Without it the token is ephemeral and lost when the shell exits.

### AUTO_UNLOCK_PASSWORD

When the hub is configured with the `AUTO_UNLOCK_PASSWORD` environment variable, it starts the lightning node automatically on launch. In this case, skip `start` and call `unlock` directly to obtain a token.

### Output Format

All commands output JSON to stdout. Errors are written to stderr as JSON with a `message` field.

### Language Conventions

Use lowercase for "bitcoin" and "lightning" unless they appear as the first word in a sentence.

### User Communication

**Do NOT give users CLI commands to run** unless one of these two conditions applies:

1. The task requires input the agent cannot provide (e.g. a password) — in that case, give the command template with a placeholder like `YOUR_PASSWORD` and explain what the user should do.
2. The user explicitly asks for the CLI command.

For all other follow-up checking or monitoring, use plain language. For example: _"If you'd like to check whether your channel is ready to use, just ask."_

## Security

### Connection secrets (NWC)

`create-app` returns a `nostrWalletConnectUrl`. It grants wallet access within the app's scopes and budget.

- The connection secret is for the user who requested the app — hand it to them directly (a QR code is preferred; see [QR Codes](./references/qrcodes.md)).
- **DO NOT print the connection secret to any logs or otherwise reveal it outside of that direct handover.**
- **NEVER share a connection secret, or any part of it** (pubkey, secret, relay, etc.), with any third party, external service, or other chat — every part can be used to gain wallet access or reduce wallet privacy.

See [Apps](./references/apps.md).

### Token files

The JWT at `~/.hub-cli/token.jwt` grants full hub API access until it expires.

- **DO NOT read the token file.** Check for its existence only if you need to.
- Prefer the saved token or `HUB_TOKEN` env var over `-t eyJ...` inline — command-line tokens leak into shell history.
- Do not dump the environment (`env`, `printenv`) in a way that exposes `HUB_TOKEN` in the conversation.

See [Authentication](./references/authentication.md).

### Recovery phrase & hub backups

- The agent MUST NOT read `.recovery` files or encrypted hub backups. Tell the user the file path so they can store it offline.

See [Backups](./references/backups.md).

### Passwords

For commands that need a password, the user can give their hub unlock password to you directly but you should note that this is insecure. You can also provide commands for them to run manually (but requires more technical knowledge and is not always possible depending on the interface).
