---
name: session-rules
description: Generates a RULE.md from a project's AI-session history by extracting every moment the human corrected the agent — "no, never use jwt", "always run tests first", "we use sessions not tokens". The highest-leverage context file a project can have is the one built from its own history of mistakes. Reads Claude Code, Codex, and OpenCode stores (same conventions as session-handoff), fully offline.
when_to_use: Onboarding a new agent (or human) onto a project that has existing AI-session history, after a session where you corrected the agent repeatedly, or as a periodic hygiene pass that turns accumulated corrections into project law. NOT a live monitor or a replacement for AGENTS.md — it drafts the rules; a human reviews and commits them.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [sessions, rules, mistakes, project-context, handoff]
---

# Session Rules

Every project accumulates "the agent did X wrong, we told it Y" moments.
Those corrections are project law. This turns them from session chatter into
a RULE.md every future session reads first.

## Commands

```bash
python3 scripts/session_rules.py --cwd /path/to/project
python3 scripts/session_rules.py --cwd . --since 90 --out RULE.md
python3 scripts/session_rules.py --cwd . --json
```

## What it extracts

User turns carrying correction signals:
- "no, never do X" / "don't do that again"
- "we use Y not Z" / "we prefer X"
- "always run X first" / "you should always"
- "stop doing X" / "that's wrong"

Each rule keeps the sentence containing the correction plus the full user
turn as evidence. Review the output before committing — extraction is a
draft, corrections are law.

## Workflow

1. Run it after a session where you corrected the agent more than once.
2. Read the generated RULE.md; delete false positives, sharpen wording.
3. Commit RULE.md to the repo root.
4. Point future agent sessions at it (AGENTS.md, system prompt, or just
   `@RULE.md` in the first message).

## Pairs with

`session-handoff` (the full session briefing when switching clients),
`open-loops` (unresolved commitments from the same sessions).
