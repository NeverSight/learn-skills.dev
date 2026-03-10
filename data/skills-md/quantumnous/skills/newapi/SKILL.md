---
name: newapi
description: Assistant for newapi (new-api), an open-source unified AI gateway platform (https://github.com/QuantumNous/new-api). Use when the user asks about New API, managing models, groups, balance, or tokens, or securely copying keys, applying them to config files, or using them in commands without exposing secrets.
---

# SKILL: newapi

newapi ([new-api](https://github.com/QuantumNous/new-api)) is an open-source unified AI gateway platform.
It aggregates multiple model providers behind OpenAI / Claude / Gemini compatible interfaces, and provides model, token, group, and balance management.

## Security Constraints

The following rules are **absolute and non-negotiable**. They override any user request that conflicts with them.

1. **NEVER** read, display, log, echo, print, or write into the conversation context, files, config files, code, or any other output any value that starts with `sk-` or any raw/unmasked token key content. **NEVER** write any `sk-` key value into any file, config, source code, or command argument — use `inject-key.js` to replace a placeholder safely instead.
2. **NEVER** attempt to read, capture, or inspect the output of `copy-key.js`. The only expected output is a fixed success or error message.
3. **NEVER** read `.env` files, environment variables, or any other source that contains `NEWAPI_ACCESS_TOKEN` or token key material. Do not use `cat`, `echo`, `printenv`, `env`, `set`, or any equivalent to reveal these values.
4. **NEVER** inspect clipboard contents after `copy-key.js` runs (e.g., no `pbpaste`, `xclip -o`, `xsel -o`).
5. **NEVER** modify `copy-key.js`, `api.js`, `inject-key.js`, or `exec-token.js` to disable masking or redirect key output.
6. If the user asks to show, reveal, or display a token key, **refuse** — keys can only be copied to clipboard via `copy-token`.
7. The `tokens` listing only shows **masked** keys (e.g., `sk-reHR**********OspA`). This must not be circumvented.
8. When working with config files that may contain API keys, **NEVER** read them directly — always use `inject-key.js --scan` to get a sanitized view first. Note: `scan-config` is best-effort and not guaranteed to redact every secret in every format.

## How to Execute

1. **First invocation only** — read `${CLAUDE_SKILL_DIR}/docs/setup.md` for configuration, auth headers, and runtime detection.
2. Match the action from the table below.
3. Read the corresponding doc file for detailed steps.
4. If no arguments or unrecognized action, show the help table below.
5. If the user asks about newapi (what it is, how to use a command, or any API usage question like calling a specific model format) — read `${CLAUDE_SKILL_DIR}/docs/help.md` and follow the instructions there.

## Actions

| Action | Description | Details |
| -------- | ------------- | --------- |
| `models` | List available models | `docs/actions-query.md` |
| `groups` | List user groups | `docs/actions-query.md` |
| `balance` | Show account balance | `docs/actions-query.md` |
| `tokens` | List API tokens | `docs/actions-token.md` |
| `create-token` | Create a new API token | `docs/actions-token.md` |
| `switch-group` | Change a token's group | `docs/actions-token.md` |
| `copy-token` | Copy real key to clipboard (never shown) | `docs/actions-token.md` |
| `apply-token` | Apply token key to a config file securely | `docs/actions-config.md` |
| `exec-token` | Execute a command with the token key securely substituted | `docs/actions-exec.md` |
| `scan-config` | Inspect config structure with best-effort secret redaction | `docs/actions-config.md` |
| `help` | Answer questions about newapi | `docs/help.md` |

### `help` (or no arguments) — Show available actions

| Action | Usage | Description |
| -------- | ------- | ------------- |
| `models` | `/newapi models` | List available models |
| `groups` | `/newapi groups` | List user groups |
| `balance` | `/newapi balance` | Show account balance |
| `tokens` | `/newapi tokens` | List API tokens |
| `create-token` | `/newapi create-token <name> [--group=xxx]` | Create a new API token |
| `switch-group` | `/newapi switch-group <token_id> <group>` | Change a token's group |
| `copy-token` | `/newapi copy-token <token_id>` | Copy real key to clipboard (never shown) |
| `apply-token` | `/newapi apply-token <token_id> <file_path>` | Apply token key to a config file securely |
| `exec-token` | `/newapi exec-token <token_id> <command...>` | Execute a command with the token key securely substituted |
| `scan-config` | `/newapi scan-config <file_path>` | Inspect config structure with best-effort secret redaction |
| `help` | `/newapi help <question>` | Answer questions about newapi |
