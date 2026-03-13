---
name: acpx
description: Use acpx as a headless ACP CLI for agent-to-agent communication, including prompt/exec/sessions workflows, session scoping, queueing, permissions, and output formats.
metadata:
  short-description: Run and orchestrate persistent ACP agent sessions from CLI
---

# acpx

## When to use this skill

Use this skill when you need to run coding agents through `acpx`, manage persistent ACP sessions, queue prompts, or consume structured output from scripts.

Use it especially for Wave-Driven Development execution after `wave-planner` is approved.

## What acpx is

`acpx` is a headless, scriptable CLI client for ACP (Agent Client Protocol) designed for agent-to-agent automation without PTY scraping.

Core capabilities:
- Persistent multi-turn sessions per repo/cwd
- One-shot execution mode (`exec`)
- Named parallel sessions (`-s/--session`)
- Queue-aware prompt submission with optional fire-and-forget (`--no-wait`)
- Cooperative cancel (`cancel`) for in-flight turns
- Session control (`set-mode`, `set <key> <value>`)
- Session metadata/history inspection (`sessions show`, `sessions history`)
- Local agent process checks (`status`)
- Structured output formats (`text`, `json`, `quiet`)

## Install

```bash
npm i -g acpx
```

Prefer global install over `npx` for stable session reuse.

## Command model

`prompt` is default.

```bash
acpx [global_options] [prompt_text...]
acpx [global_options] prompt [prompt_options] [prompt_text...]
acpx [global_options] exec [prompt_options] [prompt_text...]
acpx [global_options] cancel [-s <name>]
acpx [global_options] set-mode <mode> [-s <name>]
acpx [global_options] set <key> <value> [-s <name>]
acpx [global_options] status [-s <name>]
acpx [global_options] sessions [list | new [--name <name>] | close [name] | show [name] | history [name] [--limit <count>]]
acpx [global_options] config [show | init]

acpx [global_options] <agent> [prompt_options] [prompt_text...]
acpx [global_options] <agent> exec [prompt_options] [prompt_text...]
```

## Built-in agent registry

Friendly names:
- `codex` -> `npx @zed-industries/codex-acp`
- `claude` -> `npx @zed-industries/claude-agent-acp`
- `gemini` -> `gemini`
- `opencode` -> `npx opencode-ai`
- `pi` -> `npx pi-acp`

Rules:
- Default agent is `codex`.
- Unknown positional agent tokens are treated as raw commands.
- `--agent <command>` is explicit raw command mode.
- Do not combine positional agent token with `--agent`.

## Core workflows

### Persistent prompt session

```bash
acpx codex 'inspect failing tests and propose fix plan'
acpx codex 'apply minimal fix and run tests'
```

### One-shot exec

```bash
acpx exec 'summarize this repo'
acpx codex exec 'review changed files'
```

### Sessions

```bash
acpx sessions new --name backend
acpx codex -s backend 'fix API pagination bug'
acpx codex sessions history backend --limit 20
acpx codex sessions close backend
```

### Queueing and no-wait

```bash
acpx codex 'run full test suite and investigate failures'
acpx codex --no-wait 'after tests, summarize root causes and next steps'
```

### Structured output for orchestration

```bash
acpx --format json codex exec 'review changed files' > events.ndjson
```

## Wave-Driven orchestration guidance

When running worker agents in waves:

1. Create one named session per worker (`-s <agent-name>`).
2. Send worker prompt with strict ownership boundaries.
3. Require explicit completion marker in each response.
4. Wait for marker before merge.
5. Merge per wave order.
6. Run integration checks before next wave.

Recommended completion marker:
`WAVE {WAVE_ID} / {AGENT_NAME} DONE`

Recommended worker handoff format:
1. Summary
2. Files changed
3. Patch/diffs
4. How to test (commands + expected results)
5. Risks/TODOs/Dependency Notes

## Global options

- `--agent <command>` raw ACP adapter command
- `--cwd <dir>` session scope directory
- `--approve-all` auto-approve all requests
- `--approve-reads` approve reads/searches, prompt for writes
- `--deny-all` deny all requests
- `--format <fmt>` output: `text`, `json`, `quiet`
- `--timeout <seconds>` max wait
- `--ttl <seconds>` queue owner idle TTL
- `--verbose` debug logs

Permission flags are mutually exclusive.

## Session behavior

Persistent prompt sessions are scoped by:
- `agentCommand`
- absolute `cwd`
- optional `session` name

Tips:
- Use named sessions for parallel streams in one repo.
- Use `--cwd` carefully; changing cwd changes session scope.
- Use `status` and `sessions show/history` to debug state.

## Practical examples

Parallel named streams:

```bash
acpx codex -s backend 'implement contract types for Wave 0'
acpx claude -s docs 'draft migration notes for Wave 0'
```

Repo-scoped review with permissive mode:

```bash
acpx --cwd ~/repos/shop --approve-all codex -s pr-842 \
  'review PR #842 for regressions and propose minimal patch'
```
