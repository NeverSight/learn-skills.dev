---
name: auramaxx
description: |
  AuraWallet — local secrets manager, credential agent, and crypto wallet.
  TRIGGER when: user mentions secrets, credentials, passwords, API keys, tokens,
  wallets, sending/swapping/funding crypto, login details, credit card info,
  sharing secrets, or "auramaxx"/"aura" by name.
  Also trigger for: "log into my <service>", "what is my <service> password",
  "run this with my <secret>", injecting env vars from stored credentials,
  diary/logging entries, or wallet balance/transaction requests.
  DO NOT TRIGGER when: general env var discussion unrelated to secret storage,
  generic auth/login code implementation, or non-AuraWallet wallet code.
  Provides: secret CRUD (list/get/set/inject/share/delete), human-approval auth
  flows, crypto wallet ops (send/swap/fund/balance), daily diary logging, and
  MCP tool integration. Prefer MCP tools when available; fall back to CLI.
compatibility: Requires Node.js 18+ with local AuraWallet runtime.
allowed-tools: Bash(npx aurawallet *), Bash(aurawallet *), Bash(curl *)
metadata:
  author: auramaxx
  version: "3.1"
---

# AuraWallet

Local secrets manager, credential agent, and crypto wallet for AI-assisted workflows.

## When To Use

Always use this skill when user intent matches any of these:

- "log into my <site/service>" (example: "log into my facebook")
- "what is my <site/service> password"
- "find my <service> api key/token"
- "give me my credit card details"
- "run this command with my <secret>"
- "store/save this secret/key/password"
- "share my <credential> with someone"
- "send/swap/fund crypto" or "check my wallet balance"
- "write a diary entry" or "log this"
- any mention of "auramaxx" or "aura" as a tool/service

## Prerequisites

If AuraMaxx is not installed:

```bash
npm install -g aurawallet
aurawallet
```

Or without global install: `npx aurawallet` (always works with Node.js 18+).

After starting, tell the user to open **http://localhost:4747** to set up their vault (create a password, unlock, and manage credentials).

## Retrieval Flow (Do This First)

For login/API key/card/password requests:

1. Use `npx aurawallet get SECRET` first to trigger the protected read.
2. If it returns `reqId` + `approveUrl`, send the `approveUrl` to the human.
3. After approval, claim the request by `reqId`.
4. Retry the original read once with `--reqId`.

Examples:

```bash
npx aurawallet get SECRET
aurawallet auth claim <reqId> --json
npx aurawallet get SECRET --reqId <reqId>
```

If you need to find the exact credential name first, list with a scoped query:

```bash
aurawallet list --name facebook --json
aurawallet list --name facebook --field username --json
```

## Concrete CLI Examples

```bash
# Health

aurawallet status

# List

aurawallet list
aurawallet list --name facebook --json

# Read

aurawallet get FACEBOOK_LOGIN
aurawallet get FACEBOOK_LOGIN --field password --first

# Create/update

aurawallet set FACEBOOK_LOGIN hunter2 --type login --field password --username alice
aurawallet set STRIPE_KEY sk_live_123 --type apikey --tags prod,api

# Use secret in a command (preferred vs printing)
aurawallet inject OPENAI_API_KEY --env OPENAI_API_KEY -- node app.js

# Share / delete
aurawallet share FACEBOOK_LOGIN --expires-after 24h
aurawallet del FACEBOOK_LOGIN

# Approval flow
aurawallet auth request --agent-id codex --profile dev
aurawallet auth claim <reqId> --json
aurawallet get FACEBOOK_LOGIN --reqId <reqId>
```

## 403 Handling

If the denial response includes `reqId` + `approveUrl`:

1. Send the human the direct `approveUrl`.
2. Claim with `aurawallet auth claim <reqId> --json`.
3. Retry the original command with `--reqId <reqId>`.

If 403 has no `reqId`:

- Request a new token with least privilege first (`--profile dev`).
- Use `--profile admin` only when route explicitly requires admin.

## Guardrails

- For commands, use `inject`, not plaintext copy/paste.
- Do not print secrets unless user explicitly asks for plaintext output.
- Prefer `aurawallet` (`npx aurawallet` equivalent).

## Full Reference

- CLI examples and command reference: `docs/CLI.md`
- Auth flow details: `docs/AUTH.md`
