---
name: done
description: Summarize session findings and save to Obsidian vault (user)
---

# Session Summary

Capture everything from the current session (Claude Code or Codex) and save it to the Obsidian vault.

## When to Use

- At the end of any Claude Code session
- When you want to preserve context for future reference
- Before switching tasks or closing a session

## Process

### 1. Gather Session Metadata

Run these commands to collect context:

```bash
# Current date
date +%Y-%m-%d

# Git branch
git branch --show-current 2>/dev/null || echo "no-branch"

# Project name (directory name)
basename "$PWD"

# Short session identifier (timestamp-based)
date +%H%M%S

# Detect agent and get session ID for resume
# Claude Code sets CLAUDECODE=1; Codex sets CODEX_THREAD_ID
if [ -n "$CLAUDECODE" ]; then
  echo "agent=claude-code"
  SESSION_ID=$(tail -100 ~/.claude/history.jsonl 2>/dev/null \
    | python3 -c "import sys,json; ids=[json.loads(l).get('sessionId','') for l in sys.stdin if 'sessionId' in l]; print(ids[-1] if ids else 'unknown')" 2>/dev/null)
  echo "session_id=${SESSION_ID}"
  echo "resume=claude --resume ${SESSION_ID}"
elif [ -n "$CODEX_THREAD_ID" ]; then
  echo "agent=codex"
  echo "session_id=${CODEX_THREAD_ID}"
  echo "resume=codex resume ${CODEX_THREAD_ID}"
  echo "resume_exec=codex exec resume ${CODEX_THREAD_ID} \"<prompt>\""
else
  echo "agent=unknown"
  echo "session_id=unknown"
fi
```

### 2. Summarize the Session

Review the entire conversation and extract:

- **What was discussed**: High-level summary of the session topic
- **Key decisions**: Technical choices made and why
- **Changes made**: Files created, modified, or deleted
- **Questions raised**: Open questions or clarifications needed
- **Follow-ups**: Next steps, TODOs, deferred work

### 3. Write to Obsidian Vault

Save to: `$OBSIDIAN_VAULT/Sessions/`

Before saving, verify and prepare the target directory:

```bash
[ -n "$OBSIDIAN_VAULT" ] || { echo "OBSIDIAN_VAULT is not set"; exit 1; }
mkdir -p "$OBSIDIAN_VAULT/Sessions"
```

> **Requires**: `OBSIDIAN_VAULT` environment variable.
> Set it in `~/.zshrc.local`:
> ```
> # 00-env
> export OBSIDIAN_VAULT="$HOME/Documents/Obsidian Vault"
> ```
>
> If unset, abort and ask the user to configure it.

File name format: `YYYY-MM-DD-<branch>-<time>.md`

Example: `2026-02-18-main-143022.md`

## Output Template

```markdown
---
date: <YYYY-MM-DD>
project: <project-name>
branch: <branch-name>
session_id: <UUID>
agent: <claude-code | codex | unknown>
model: <model-name>
tags:
  - session
  - <agent-name>
---

# Session: <project> / <branch> (<date>)

## Summary

<1-3 sentence overview of what was accomplished>

## Agent

- **Agent**: <claude-code | codex | unknown>
- **Model**: <model name, e.g. claude-sonnet-4-6 or o4-mini>
- **Resume**: `<resume command>`

## What Was Discussed

<Bullet points of topics covered in the session>

## Key Decisions

<Technical choices made, with brief rationale>
- **Decision**: Why

## Changes Made

<Files created, modified, or deleted>
- `path/to/file` — what changed and why

## Questions & Clarifications

<Open questions or things that needed clarification>
- Question or clarification point

## Follow-ups / Next Steps

<Deferred work, TODOs, or things to pick up next session>
- [ ] Next step 1
- [ ] Next step 2

## Notes

<Any other observations, gotchas, or context worth preserving>
```

## Tips

- Be concise but complete — future-you needs enough context to resume quickly
- Include file paths for any code that was changed
- Capture the "why" behind decisions, not just the "what"
- If no git branch exists, use the project/directory name instead
