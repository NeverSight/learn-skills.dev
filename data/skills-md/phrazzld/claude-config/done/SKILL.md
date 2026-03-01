---
name: done
description: |
  Session retrospective and codification. Run at the end of any significant
  session to extract learnings, update documentation, and create artifacts
  that make future sessions smoother.

  Invoke when:
  - Finishing a multi-step implementation
  - After debugging a hard problem
  - End of any session with 3+ tool calls
  - "what did we learn?" / "wrap up" / "done"

  Subsumes /codify-learning (codification is one output, not the only one).
effort: medium
argument-hint: "[--skip-commit] [--focus area]"
---

# /done — Session Retrospective

Structured reflection that produces concrete artifacts. Not a journal entry —
every finding either becomes a codified artifact or gets explicitly justified
as not worth codifying.

## Process

### 1. Gather Evidence

Reconstruct session from multiple sources:

```
# What changed
git diff --stat HEAD~N  (or unstaged if no commits)
git log --oneline -10

# What was attempted (from conversation context)
- Commands that failed and why
- Bugs encountered and root causes
- Patterns discovered
- User corrections received

# Current state
- Task list status
- Any pending/blocked items
```

### 2. Categorize Findings

Sort into five buckets:

| Bucket | Question | Example |
|--------|----------|---------|
| **Went well** | What should we keep doing? | Module separation, lazy imports |
| **Friction** | What slowed us down? | Guessed at API, wrong return types |
| **Bugs introduced** | What broke and why? | Dict access on dataclass |
| **Missing artifacts** | What docs/tools would have prevented friction? | Module API reference |
| **Architecture insights** | What design decisions proved right/wrong? | SQLite for persistence |

### 3. Codification Pass

For EACH friction point and bug, evaluate codification targets in order:

```
Hook      → Can we prevent this automatically? (pre-edit)
Lint rule → Can a lint rule catch this at edit time? → invoke /guardrail
Agent     → Can a reviewer catch this?
Skill     → Is this a reusable workflow?
Memory    → Should auto-memory capture this?
CLAUDE.md → Is this a convention/philosophy?
Docs      → Does a reference doc need updating?
```

**Default: codify. Exception: justify not codifying.**

### 3.5. Retro Append

If this session implemented a GitHub issue, append implementation feedback to
`{repo}/.groom/retro.md` via `/retro append`:

- Issue number
- Predicted effort (from issue's effort label) vs actual effort
- Scope changes (what was added/removed during implementation)
- Blockers encountered
- Reusable pattern for future scoping

This feeds the grooming feedback loop — `/groom` reads retro.md to calibrate
future effort estimates and issue scoping.

### 3.6. Tune Repo

Run `/tune-repo` to refresh `.glance.md` summaries, update CLAUDE.md/AGENTS.md if drift is detected, and seed memory with new gotchas from the session.

### 4. Execute Codification

For each item to codify:

1. Read the target file
2. Check for existing coverage (avoid duplication)
3. Add the learning in the file's native format
4. Verify no conflicts with existing content

Codification targets by type:

| Target | Location | Format |
|--------|----------|--------|
| Hook | `~/.claude/settings.json` + `~/.claude/hooks/` | Python/bash script |
| Agent | `~/.claude/agents/` | YAML agent config |
| Skill update | `~/.claude/skills/*/SKILL.md` | Markdown with frontmatter |
| Auto-memory | `~/.claude/projects/*/memory/*.md` | Markdown notes |
| CLAUDE.md | `~/.claude/CLAUDE.md` Staging section | Concise pattern |
| Project docs | Repo `CLAUDE.md`, `AGENTS.md`, `docs/` | Varies |

### 5. Report

Output structured summary:

```
## Session Retrospective

### Went Well
- [item]: [why it worked]

### Friction Points
- [item]: [what happened] → [codified to: file]

### Bugs Introduced & Fixed
- [bug]: [root cause] → [codified to: file]

### Artifacts Created/Updated
- [file]: [what changed]

### Not Codified (with justification)
- [item]: [specific reason]

### Open Items
- [anything left unfinished or flagged for future]
```

## Integration

| Consumes | Produces |
|----------|----------|
| Session context (conversation) | Updated CLAUDE.md staging |
| `git diff`, `git log` | New/updated skill files |
| Task list state | New/updated hooks |
| Error logs from session | Auto-memory entries |
| | New/updated agents |
| | `.groom/retro.md` entries |

**Hands off to:**
- `/commit` — if codification artifacts should be committed
- `/distill` — if staging section is getting long (graduate to skills/agents)

## Anti-Patterns

- Writing a retrospective without producing artifacts ("reflecting without codifying")
- Codifying things that are already covered (check existing files first)
- Over-codifying obvious patterns that any model would know
- Creating docs nobody will read (prefer hooks/agents that enforce automatically)
- Skipping the "went well" section (positive reinforcement matters for pattern stability)

## Visual Deliverable

After completing the core workflow, generate a visual HTML summary:

1. Read `~/.claude/skills/visualize/prompts/done-retro.md`
2. Read the template(s) referenced in the prompt
3. Read `~/.claude/skills/visualize/references/css-patterns.md`
4. Generate self-contained HTML capturing this session's output
5. Write to `~/.agent/diagrams/retro-{date}.html`
6. Open in browser: `open ~/.agent/diagrams/retro-{date}.html`
7. Tell the user the file path

Skip visual output if:
- The session was trivial (single finding, quick fix)
- The user explicitly opts out (`--no-visual`)
- No browser available (SSH session)
