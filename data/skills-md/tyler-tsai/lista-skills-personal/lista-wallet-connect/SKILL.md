---
name: lista-wallet-connect
version: 1.0.0
repository: https://github.com/lista-dao/lista-skills
node: ">=18.0.0"
description: Connect wallets via WalletConnect v2 and execute EVM signing/contract-call operations on Ethereum and BSC.
---

# Wallet Connect Skill

> **Status:** Pre-release (internal only, not in public registry)
> **Agent quick check:** `node dist/cli/cli.bundle.mjs version`
> **Agent rebuild:** `npm install && npm run build`

Wallet connection and transaction bridge skill for EVM (`eip155:1`, `eip155:56`).

## Agent Execution Policy

- Execute CLI/setup commands directly as the agent; do not ask the user to run shell commands.
- If dependencies/build/env are missing, fix them automatically in the workspace.
- Before any signing or on-chain write action, explain the action and get user consent.
- Do not output raw JSON/internal payloads to users by default; present concise human-readable summaries.
- Use command snippets in this document as agent-side execution references only.

## Project Structure

```text
skills/lista-wallet-connect/
├── SKILL.md
├── package.json
├── tsconfig.json
├── references/
│   └── chains.md
└── src/
    ├── cli/                # args/help/meta/router/env
    ├── commands/           # pair/auth/sign/call/...
    │   └── call/           # parse/simulate/constants
    ├── client.ts
    ├── storage.ts
    ├── helpers.ts
    ├── rpc.ts
    ├── types.ts
    └── cli.ts              # CLI entrypoint
```

Notes:

- `src/cli.ts` stays as the entrypoint; argument parsing/help/dispatch are split under `src/cli/*`.
- Raw call logic is modularized under `src/commands/call/*` (`parse`, `simulate`, constants).

## Setup (Agent-Run)

Use prebuilt `dist/` by default for faster startup.

```bash
cd skills/lista-wallet-connect
# ensure Node.js >= 18 (recommended >= 20)
node -v
node dist/cli/cli.bundle.mjs version
```

Only run install/build when `dist/` is missing or version check fails:

```bash
cd skills/lista-wallet-connect
npm install
npm run build
node dist/cli/cli.bundle.mjs version
```

Set WalletConnect project id:

```bash
export WALLETCONNECT_PROJECT_ID=c9e9af475f95d71b87da341e0b1e2237
```

Default project id is already included in `skills/lista-wallet-connect/.env`.  
You can override it by exporting `WALLETCONNECT_PROJECT_ID` in your shell.

## Runtime Contract

- Agent execution entrypoint: `node dist/cli/cli.bundle.mjs <command> ...`
- `stdout`: JSON payloads for automation/agent parsing
- `stderr`: progress/diagnostic logs
- Wallet-request commands emit one `waiting_for_approval` event first, then a terminal status (`paired`/`authenticated`/`signed`/`sent`/`rejected`/`simulation_failed`/`error`).
- Optional debug mode: add `--debug-log-file <path>` to append structured `stdout/stderr` logs (jsonl).
- Keep CLI/runtime JSON and debug logs in raw format (for example `eip155:1`, `eip155:56`) for stable machine parsing and troubleshooting.
- For user-facing answers, the agent should map chain IDs to names (`eip155:1` -> `Ethereum`, `eip155:56` -> `BSC`) in rendered text/tables.
- Treat raw JSON payloads as internal contract data; only show raw output to users on explicit request.

### OpenClaw Streaming Rules (Required)

- Run wallet-request commands (`pair`, `auth`, `sign`, `sign-typed-data`, `call`) as long-running streams.
- Do not stop on `status: "waiting_for_approval"`; this is an interim event only.
- Continue consuming output until a terminal status is received.
- Terminal statuses: `paired`, `authenticated`, `signed`, `sent`, `rejected`, `simulation_failed`, `error`.
- If no terminal status arrives before process timeout, return timeout as an operational error and prompt retry.
- For `pair`, always try image delivery first (`qrPath` attachment, then `qrMarkdown` if supported).
- Only send `uri` (`wc:`) when image rendering/delivery is unsupported or fails.
- Read `deliveryPlan` in the waiting payload as the source of truth for this fallback order.
- For OpenClaw channels, if `openclaw.mediaDirective` exists, emit that `MEDIA:<path>` line as the image-send directive.
- If OpenClaw media send fails, retry with `openclaw.fallbackUri` (`wc:` URI) as text.
- When a waiting event contains `interactionRequired: true`, show a user reminder immediately (once per request) using `userReminder` text, e.g. "Please approve/reject in your wallet app."

## Supported Chains

- `eip155:1` (Ethereum)
- `eip155:56` (BSC)

## Security Rules

1. Never send/sign without explicit user confirmation.
2. Always show chain, destination, calldata/value summary before sending.
3. Use `call` simulation by default; avoid `--no-simulate` unless user insists.
4. Do not disclose session topic or pairing URI to third parties.

## Command Index

- `pair`
- `status`
- `auth`
- `sign`
- `sign-typed-data`
- `call`
- `sessions`
- `list-sessions`
- `whoami`
- `delete-session`
- `health`
- `version`

## Command Details

All command snippets below are for agent execution; do not instruct the user to type them manually.

### 1) `pair`

Purpose: Start WalletConnect pairing flow.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs pair --chains eip155:56
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs pair --chains eip155:56,eip155:1
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs pair --chains eip155:56 --open
```

Behavior:
- First outputs `status: "waiting_for_approval"` with `uri`, `qrPath`, `qrMarkdown`, `deliveryPlan`, `openclaw`, plus guidance fields.
- After user approves, outputs `status: "paired"` with `message`, `topic`, `accounts`, `peerName`, `pairedAt`, and `summary`.

### 2) `status`

Purpose: Check whether a stored session exists.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs status --topic <topic>
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs status --address 0xADDRESS
```

### 3) `auth`

Purpose: Request a consent signature and mark session as authenticated.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs auth --topic <topic>
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs auth --address 0xADDRESS
```

### 4) `sign`

Purpose: Sign an arbitrary message (`personal_sign`).

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs sign --topic <topic> --message "Hello"
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs sign --address 0xADDRESS --message "Hello" --chain eip155:56
```

### 5) `sign-typed-data`

Purpose: Sign EIP-712 typed data (`eth_signTypedData_v4`).

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs sign-typed-data --topic <topic> --data '{"domain":...,"types":...,"message":...}'
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs sign-typed-data --address 0xADDRESS --data @/path/to/typed-data.json --chain eip155:1
```

### 6) `call`

Purpose: Send arbitrary contract transaction (`eth_sendTransaction`) with optional calldata and value.

Key points:
- Simulates via `eth_call` before sending by default.
- On simulation failure, command returns `status: "simulation_failed"` and does not send tx.
- Use `--no-simulate` only when you intentionally want to bypass simulation.
- `--value` accepts hex wei (`0x...`) or native decimal string (for example `0.01`).

Examples:

```bash
# contract call with calldata
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs call --topic <topic> --chain eip155:56 --to 0xCONTRACT --data 0xCALLDATA

# with native value
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs call --topic <topic> --chain eip155:56 --to 0xCONTRACT --data 0xCALLDATA --value 0.01

# custom gas
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs call --topic <topic> --chain eip155:56 --to 0xCONTRACT --data 0xCALLDATA --gas 500000

# force send without simulation (risky)
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs call --topic <topic> --chain eip155:56 --to 0xCONTRACT --data 0xCALLDATA --no-simulate
```

### 7) `sessions`

Purpose: Dump raw saved sessions JSON (internal/debug usage).

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs sessions
```

### 8) `list-sessions`

Purpose: Human-readable session listing.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs list-sessions
```

### 9) `whoami`

Purpose: Show account details for a session, or latest session if omitted.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs whoami --topic <topic>
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs whoami --address 0xADDRESS
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs whoami
```

### 10) `delete-session`

Purpose: Remove a saved session entry.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs delete-session --topic <topic>
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs delete-session --address 0xADDRESS
```

### 11) `health`

Purpose: Ping session(s) for liveness and optionally clean dead sessions.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs health --topic <topic>
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs health --address 0xADDRESS
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs health --all
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs health --all --clean
```

### 12) `version`

Purpose: Print skill version.

```bash
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs version
```

## Common Options

- `--address <0x...>`: resolve and use latest session matching address
- `--topic <topic>`: explicit session topic
- `--chain <eip155:1|eip155:56>`
- `--open` (pair): force open QR image in system viewer
- `--no-simulate` (call): bypass simulation

## Session Persistence

- WalletConnect storage: `~/.agent-wallet/wc-store/`
- Session metadata: `~/.agent-wallet/sessions.json`

## Quick Onboarding Flow

```bash
# 1) pair
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs pair --chains eip155:56,eip155:1 --open

# 2) auth
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs auth --topic <topic>

# 3) verify
node skills/lista-wallet-connect/dist/cli/cli.bundle.mjs whoami --topic <topic>
```

## Integration Notes (with lista-lending)

- `lista-lending` executes transactions by calling this skill's `call` command.
- Keep both skills aligned on chain/RPC configuration.
- For debugging transaction flow issues, inspect `stderr` from both skills.
