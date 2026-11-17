---
name: pre-compact
description: Prepare the session for context compaction - write a handoff file a fresh session can continue from, propose updates to the project's durable docs, apply them on approval or with `auto`. Use before compacting or clearing context, or on "pre-compact".
metadata:
  version: "0.1.5"
  categories: "agents, productivity"
  topics: "context, handoff, compaction, session-state, documentation"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/pre-compact
    emoji: "🧳"
argument-hint: "[auto|a]"
---

I will compact this context soon. The summary can be wrong. Files are the
source of truth. Move everything a fresh session needs from this conversation
into files. Mode: $ARGUMENTS. `auto` or `a` means: apply all proposed updates
without asking.

Write `.agents/compact-handoff/YYMM-DD-HHMM-<short-slug>.md`. Start with the
line `# Handoff <date> <time> <repo>@<branch>`. Then write these sections:

- Position: what we are doing, why, and where we stopped.
- Next steps: in order, with the paths, commands and identifiers needed to run them.
- Decisions: each decision made here, with its reason.
- Findings: what we learned works or fails, verbatim.
- Open questions: numbered, each with your recommended answer.
- Undone instructions: what I asked for that is not done.
- References: files, links, related docs.

Copy numbers, commands and paths exactly. Do not paraphrase them. Never write
secrets, tokens, passwords or API keys into the handoff. Write where they
live instead, for example the env var name or the vault item. Record only
decisions that were made. Keep open questions open.

Then check the docs this project uses to track work: plans, journals, status
sections, task lists. For each item in the handoff, ask: is it recorded there,
and is it current? Do not ask me what the repo can answer.

Also check my global agent instructions (`~/.claude/CLAUDE.md`, `AGENTS.md`,
or the equivalent for this harness) for the marker `<!-- pre-compact -->`. If
the marker is absent, add this item: insert the line below verbatim.

- After compaction, read the handoff file named in the summary (`.agents/compact-handoff/`) before you trust the summary. The summary can be wrong. The handoff file is the source of truth. <!-- pre-compact -->

List what is missing or stale as numbered items. Give the file and the change,
one line each. Then ask: y = apply all, n = apply none, numbers = apply those,
or tell me what to change. Wait for my answer, unless in auto mode. Never
commit. Never push.

Finish with one line: READY, the handoff path, and the files you changed.
