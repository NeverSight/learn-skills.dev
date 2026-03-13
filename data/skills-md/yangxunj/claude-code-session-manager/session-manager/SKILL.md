---
name: session-manager
description: |
  Session expert management system for Claude Code projects. Enables tracking, routing, activating, and registering conversation sessions as domain experts. Use this skill when:
  (1) Setting up session management for a new project (initialization)
  (2) A user requests a feature change, bug fix, or optimization and you need to check if a session expert already handles that domain (routing)
  (3) A session has accumulated deep domain context and should register itself as an expert (registration)
  (4) An existing session expert needs to update its registration after scope changes (update)
  (5) A session is expired and needs to be activated for resuming (activation)
  (6) The user asks about managing, organizing, or optimizing session documentation
---

# Session Manager

## Overview

This skill provides a complete system for managing Claude Code sessions as reusable domain experts. Instead of starting fresh each time, sessions that have accumulated deep context in specific functional areas are documented and can be resumed when related work arises.

## Workflow Decision Tree

```
User request arrives
│
├─ "Set up session management for this project"
│   └─ Go to → Initialize
│
├─ Feature change / bug fix / optimization request
│   └─ Go to → Route
│
├─ "Register this session as an expert"
│   └─ Go to → Register
│
├─ "Update this session's registration"
│   └─ Go to → Update
│
├─ "Activate / resume an old session"
│   └─ Go to → Activate
│
└─ "Optimize session documentation structure"
    └─ Go to → Maintain
```

## Initialize

Set up session management for a project that doesn't have it yet.

**Steps:**

1. Copy `assets/template-index.md` to the project (recommended: `doc/reference/claude-sessions.md`)
2. Copy `assets/template-details.md` to the project (recommended: `doc/reference/claude-sessions-details.md`)
3. Copy `scripts/claude-session.py` to the project (recommended: `scripts/claude-session.py`)
4. Add the CLAUDE.md integration snippet from `assets/template-claude-md-snippet.md` to the project's CLAUDE.md
5. Customize the page tree structure in the index file to match the project's architecture
6. Commit all files

**Important:** The script requires Python 3.6+. On Windows, if Unicode errors occur, prefix with `PYTHONUTF8=1`.

## Route

When a user requests any change, check if a session expert should handle it.

**Steps:**

1. Read the project's session index file (e.g., `doc/reference/claude-sessions.md`)
2. Scan the index table tags, page tree, and file path index
3. If a matching session is found:
   - Run `python scripts/claude-session.py list` to check its status
   - If `[----]` (expired): run `python scripts/claude-session.py activate <session-id>`
   - Recommend: `claude --resume <session-id>`
   - Explain why that session is better suited
   - Do NOT do the work yourself unless the user explicitly asks
4. If no match: handle the request yourself

**Why this matters:** A session expert has the complete conversation history — design decisions, pitfalls encountered, user preferences, architectural context. A new session reading the same code cannot reconstruct this implicit knowledge.

## Register

When a session has accumulated significant domain context, register it as an expert.

**Prerequisites:** The session must have genuine, independent domain context that no existing session covers.

**How to trigger:** Tell the session to read the index file and follow its built-in registration guide. For example:

```
Read `doc/reference/claude-sessions.md` — follow "Scenario A: New Session Registration" in the Registration & Update Guide. Your Session ID is: <session-id>
```

To find the session ID: `python scripts/claude-session.py list` — rank #1 is the current session.

The index file's built-in guide will instruct the session to:
1. Self-evaluate overlap against existing sessions (>60% overlap = do not register)
2. If assessment passes, write to 4 places: index table, page tree, file path index, details file
3. Commit to git

## Update

When an existing session expert's scope has changed after further development, update its registration.

**How to trigger:**

```
Read `doc/reference/claude-sessions.md` — follow "Scenario B: Update Existing Registration" in the Registration & Update Guide. Your Session ID is: <session-id>
```

The session will compare its current context against its registered info and update all four records accordingly.

## Activate

Resume a session that has fallen out of Claude Code's ~10 most recent.

```bash
# Check which sessions are resumable
python scripts/claude-session.py list

# Activate an expired session
python scripts/claude-session.py activate <session-id>

# Resume it
claude --resume <session-id>
```

The script supports partial ID matching (e.g., `activate 3f5273` instead of the full UUID).

## Maintain

Guidelines for keeping session documentation healthy:

- **Tags**: 5-8 functional domain keywords per session, no implementation details
- **Core abilities**: Describe "what the session understands", not "what it changed"
- **File paths**: Paths only, no parenthetical annotations
- **Overlap check**: Before registering, verify >60% overlap threshold against existing sessions
- **Status updates**: Mark sessions as `outdated` when their code has significantly changed, or `superseded:S0XX` when replaced

## Resources

### scripts/

- `claude-session.py` — Session management CLI tool (list sessions, activate expired ones). Copy to the target project's `scripts/` directory.

### assets/

- `template-index.md` — Template for the session index file (index table + page tree + file path index + built-in registration & update guide)
- `template-details.md` — Template for the session details file (per-session functional domain descriptions)
- `template-claude-md-snippet.md` — CLAUDE.md integration snippet (routing workflow + tool usage instructions)
