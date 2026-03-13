---
name: personal-context-ask-flow
description: Use when running question answering in the Personal Context CLI project, including selective context preview and ask with host-auth relay providers.
---

# Personal Context Ask Flow

## Overview

Use this skill for question workflows only.
It focuses on `context preview` and `ask` with provider control (`auto`, `codex`, `claude`).

## One-Time Install

```bash
pipx install "git+https://github.com/WangLiquan/personal-context-cli.git@v0.1.1-beta"
```

Ask the user for profile password once, then pass it with `--password`.

## Ask Workflow

Do not ask the user for question type or structured parameters.
Ask for the natural-language question only, then run commands directly.

### 1) Preview selected context (optional)

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

### 2) Ask with provider relay

```bash
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Provider Modes

- `auto`: try `codex` first, then `claude`, then host-auth guidance.
- `codex`: force relay to `codex exec`.
- `claude`: force relay to `claude -p`.

## Verification

```bash
cd $PROJECT_ROOT
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
