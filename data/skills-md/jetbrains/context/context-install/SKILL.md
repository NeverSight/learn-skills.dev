---
name: context-install
description: Install jbcontext and complete first-time setup — login and configure agent integration. Use when `jbcontext` is not found or the user asks to install jbcontext.
---

# Install and set up jbcontext

Use this skill to install the jbcontext CLI and finish first-time setup (login, agent integration).

## When to use

- `jbcontext` returns `command not found`
- The user says jbcontext is not installed
- The user explicitly asks to install jbcontext

## Do not use for

- Authentication issues → use `jbcontext login`
- Missing project index → use `jbcontext index`
- Agent integration only → use `jbcontext setup-agent --help`

## Install

### macOS / Linux

```bash
curl -fsSL https://download.jetbrains.com/jetbrains-context/release/download-jbcontext.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://download.jetbrains.com/jetbrains-context/release/download-jbcontext.ps1 | iex
```

## Verify installation

```bash
jbcontext --version
```

## Common follow-ups

### `401`

The user is not logged in.

```bash
jbcontext login
```

### `404`

There is no index on the server.

```bash
jbcontext index
```

### Agent setup

If the user also wants jbcontext configured for an agent, use `jbcontext setup-agent`.

Claude non-interactive setup:

```bash
jbcontext setup-agent --agent=CLAUDE --auto --non-interactive
```

Codex non-interactive setup:

```bash
jbcontext setup-agent --agent=CODEX --auto --non-interactive
```

Study help for any other agents and options:
```aiignore
jbcontext setup-agent --help
```
