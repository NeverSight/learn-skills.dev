---
name: openclaw-cli
description: Use this skill when the user wants you to talk to OpenClaw. Trigger it for requests like "ask OpenClaw...", "tell OpenClaw...", "message OpenClaw...", or any similar wording.
---

# OpenClaw CLI

Use the `openclaw-cli` CLI for direct OpenClaw calls.

## Install

If `openclaw-cli` is not installed yet, run:

```bash
curl -fsSL https://raw.githubusercontent.com/TimoBechtel/openclaw-cli/main/install.sh | bash
```

## Required environment

```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
```

Optional:

- `OPENCLAW_BASE_URL` (default `http://127.0.0.1:18789`)
- `OPENCLAW_AGENT_ID` (default `main`)
- `OPENCLAW_SESSION_KEY_PREFIX`

## Usage

Start a new conversation (omit `--session-key`):

```bash
openclaw-cli ask "Summarize the latest deployment risks."
```

Continue the same conversation (reuse the returned session key):

```bash
openclaw-cli ask "Continue from previous context." --session-key "<session-key>"
```

Use machine-readable output when needed:

```bash
openclaw-cli ask "Return JSON with top 3 risks." --json
```

## Session handling

- Pass the same `--session-key` on every call to continue a conversation.
- First call: omit `--session-key` (a new one is returned).
- Later calls: pass the returned key.
- To start fresh, omit `--session-key` again.

## Context guidance

- OpenClaw has no memory between sessions.
- When starting fresh or omitting `--session-key`, include the full context OpenClaw needs:
  - the user's question
  - relevant code
  - file paths
  - any other important details
