---
version: 0.1.0
name: 58pic-account
description: |
  Manage 千图AI / 58pic CLI setup, authentication, API key configuration,
  OAuth login, logout, auth status, current config, credits, balance,
  and recent usage. Use when: "login to 58pic", "configure API key",
  "check my credits", "auth status", "58pic auth", "千图账号", "点数余额".
argument-hint: "[auth|credits|config]"
allowed-tools: Bash
---

# 千图AI (58pic) — Account, Auth & Credits

Set up the CLI, authenticate, and check credit balance.

## CLI Setup

Check the CLI:

```bash
58pic --version
```

If missing:

```bash
npm install -g @58pic/cli
```

Node.js must be 18 or newer:

```bash
node --version
```

## Auth Status

```bash
58pic auth status -f json | jq '{loggedIn, authMethod}'
```

If `loggedIn` is `false`, choose one auth method.

## API Key Auth

Fastest for automation:

```bash
58pic config init --api-key sk_YOUR_KEY
```

Interactive setup:

```bash
58pic config init
```

Get an API key from https://ai.58pic.com/open-platform.

## OAuth Login

Use when the user has no API key:

```bash
58pic auth login
```

After this command opens a browser, wait for the user to confirm authorization is complete before continuing.

## Logout

```bash
58pic auth logout
```

## Show Config

```bash
58pic config show
```

Never print raw secrets or full API keys in chat.

## Credits

Check balance and recent usage:

```bash
58pic credits -f json | jq '{balance: .data.balance, recent: .data.list[:5]}'
```

If balance is insufficient, ask the user to top up at https://ai.58pic.com.

## References

- `references/troubleshooting.md` — auth, token, credits, and CLI issues
