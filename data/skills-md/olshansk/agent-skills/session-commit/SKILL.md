---
name: session-commit
description: Capture learnings from the current coding session and update AGENTS.md. Use when the user asks to close the loop, run session-commit, record best practices, or update agent instructions based on recent work.
license: MIT
compatibility: Requires read/write access to files in the current repository. Works best in agentic coding CLIs with shell execution support.
metadata:
  author: olshansk
  version: "1.0.0"
allowed-tools: Read Write Edit Glob Grep Bash LS AskUserQuestion
---

# Session Commit

Analyze the current coding session, propose improvements to `AGENTS.md`, and apply approved changes.

## Available scripts

- `scripts/preflight.sh` - Checks whether required instruction files exist and optionally repairs missing files.

## Workflow

1. Run preflight checks:

```bash
bash scripts/preflight.sh
```

2. If preflight fails and user approves repairs, run:

```bash
bash scripts/preflight.sh --fix
```

3. Read the current `AGENTS.md` and build a mental map of existing sections.
4. Extract only durable learnings from the current session.
5. Propose changes using the format in `references/change-proposal-format.md`.
6. Wait for explicit user approval before applying any edits.
7. Apply approved changes and merge with existing content.

## What to capture

- Coding patterns and conventions established in the session
- Architecture decisions and reasoning that should persist
- Debugging playbooks and recurring gotchas
- Workflow preferences that improve future sessions

## Guardrails

- Do not capture transient implementation details that will age quickly.
- Prefer updating existing sections before creating new headings.
- Use concise bullet points rather than long paragraphs.
- Keep guidance tool-agnostic unless behavior differs by tool.
- If no meaningful learning occurred, report that and stop.

## Pointer file behavior

If `CLAUDE.md`, `CODEX.md`, or `GEMINI.md` are missing or empty, create symlinks that point to `AGENTS.md`.

## Output contract

- Proposal stage: output only proposed changes with explicit add/modify/remove counts.
- Apply stage: update `AGENTS.md` only after explicit approval.
- Completion stage: summarize what changed and where.
