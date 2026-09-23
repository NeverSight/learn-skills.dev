---
name: session-handoff
description: Carries work context between AI agent clients. Reads session logs from every installed client's native store (Claude Code JSONL projects, Codex rollout JSONL, OpenCode SQLite, Gemini CLI chats), and produces a portable handoff briefing — what was asked, what was done, files touched, last state — so a session in one client can continue work started in another. Use when switching clients mid-task ("bring everything I worked on in Codex into this Claude session"), resuming after days away, or auditing what any client did recently.
when_to_use: You worked on something in one agent client and want to continue in another, or need a cross-client inventory of recent sessions for a directory. NOT a live sync — it reads completed local logs; nothing is uploaded anywhere.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [sessions, handoff, interop, context, multi-agent]
---

# Session Handoff

One machine, many agent clients, one work history. `session_handoff.py` reads
each client's native session store read-only and turns recent work into a
briefing the current client can consume.

## Commands

```bash
python3 scripts/session_handoff.py list                       # recent sessions, all clients
python3 scripts/session_handoff.py list --cwd $(pwd)          # only sessions about this project
python3 scripts/session_handoff.py show claude:a3f7e0b9       # one session's turns + files
python3 scripts/session_handoff.py handoff --cwd $(pwd)       # markdown briefing to stdout
python3 scripts/session_handoff.py handoff --since 7 --sessions 8 --out HANDOFF.md
```

All commands accept `--json` for machine-readable output.

## Typical flow

You worked in Codex yesterday; today you open Claude Code (or any client) and
ask it to continue:

1. `handoff --cwd <project>` produces the briefing: per session, the user asks,
   the last assistant state, and the files it touched.
2. Paste the briefing (or `--out HANDOFF.md` and reference the file) into the
   current session.
3. The current agent reads it and picks up where the other client stopped.

An agent running this skill should execute step 1 itself and ingest the output
directly instead of asking the user to paste it.

## Session stores read (read-only, local, nothing uploaded)

| Client | Store | Format |
|---|---|---|
| Claude Code | `~/.claude/projects/<slug>/*.jsonl` | JSONL events (user/assistant/tool_use) |
| Codex | `~/.codex/sessions/**/rollout-*.jsonl` | JSONL (session_meta, response_item) |
| OpenCode / OMO | `~/.local/share/opencode/opencode.db` | SQLite (session, message, part) |
| Gemini CLI | `~/.gemini/tmp/<hash>/chats/*.json` | JSON chat logs |

Missing stores are skipped silently. Command/hook noise (slash-command
wrappers, task notifications, skill-load banners) is filtered so the briefing
holds real work, not harness chatter.

## Semantics

- `--cwd` matches sessions whose working directory is the target or inside it
  (never a parent — a session about `~` is not a session about your project).
- `show <provider>:<id-prefix>` resolves any unambiguous id prefix.
- The OpenCode reader also covers OMO/Senpi sessions (same store).
- Older sessions: raise `--since` (days); `list` searches up to a year for
  `show` resolution.
