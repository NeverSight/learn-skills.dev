---
name: swain-retro
description: "Automated retrospectives — captures learnings at EPIC completion and on manual invocation. Reviews recent work, prompts the user with reflection questions, then distills findings into memory files and retro docs. Triggers on: 'retro', 'retrospective', 'what did we learn', 'reflect', or automatically after EPIC completion."
user-invocable: true
license: MIT
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  short-description: Structured retrospectives at natural completion points
  version: 1.0.0
  author: cristos
  source: swain
---
<!-- swain-model-hint: sonnet, effort: medium -->

# Retrospectives

Captures learnings at natural completion points and persists them for future use. This skill is both auto-triggered (EPIC completion hook in swain-design) and manually invocable via `/swain-retro`.

## Invocation modes

| Mode | Trigger | Context source |
|------|---------|---------------|
| **Auto** | EPIC transitions to Complete (called by swain-design) | The completed EPIC and its child artifacts |
| **Manual** | User runs `/swain-retro` or `/swain retro` | Recent work — git log, closed tasks, transitioned artifacts |
| **Scoped** | `/swain-retro EPIC-NNN` or `/swain-retro SPEC-NNN` | Specific artifact and its related work |

## Step 1 — Gather context

Collect evidence of what happened during the work period.

### For EPIC-scoped retros (auto or scoped)

```bash
# Get the EPIC and its children
bash skills/swain-design/scripts/specgraph.sh tree <EPIC-ID>

# Get closed tasks linked to child specs
TK_BIN="$(cd skills/swain-do/bin && pwd)"
export PATH="$TK_BIN:$PATH"
ticket-query '.status == "closed"' 2>/dev/null | grep -l "<EPIC-ID>\|<SPEC-IDs>"
```

Also read:
- The EPIC's lifecycle table (dates, duration)
- Child SPECs' verification tables (what was proven)
- Any ADRs created during the work
- Git log for commits between EPIC activation and completion dates

### For manual (unscoped) retros

```bash
# Recent git activity
git log --oneline --since="1 week ago" --no-merges

# Recently closed tasks
TK_BIN="$(cd skills/swain-do/bin && pwd)"
export PATH="$TK_BIN:$PATH"
ticket-query '.status == "closed"' 2>/dev/null | head -20

# Recently transitioned artifacts
bash skills/swain-design/scripts/specgraph.sh status 2>/dev/null
```

Also check:
- Existing memory files for context on prior patterns
- Previous retro docs in `docs/swain-retro/` for recurring themes

## Step 2 — Present summary and prompt reflection

Present a concise summary of what was accomplished, then ask targeted reflection questions. **Do not auto-generate retro content** — the user drives the reflection.

### Summary format

> **Retro scope:** {EPIC-NNN title / "recent work"}
> **Period:** {start date} — {end date}
> **Artifacts completed:** {list}
> **Tasks closed:** {count}
> **Key commits:** {notable commits}

### Reflection questions

Ask these one at a time, waiting for user response between each:

1. **What went well?** What patterns or approaches worked effectively that we should repeat?
2. **What was surprising?** Anything unexpected — blockers, shortcuts, scope changes?
3. **What would you change?** If you could redo this work, what would you do differently?
4. **What patterns emerged?** Any recurring themes across tasks — tooling friction, design gaps, communication patterns?

Adapt follow-up questions based on user responses. If the user gives brief answers, probe deeper. If they're expansive, move on.

## Step 3 — Distill into memory files

After the reflection conversation, create or update memory files:

### Feedback memories

For behavioral patterns and process learnings that should guide future agent behavior:

```markdown
---
name: retro-{topic}
description: {one-line description of the learning}
type: feedback
---

{The pattern or rule}

**Why:** {User's explanation from the retro}
**How to apply:** {When this guidance kicks in}
```

Write to the project memory directory:
```
~/.claude/projects/<project-slug>/memory/feedback_retro_{topic}.md
```

Update `MEMORY.md` index.

### Project memories

For context about ongoing work patterns, team dynamics, or project-specific learnings:

```markdown
---
name: retro-{topic}
description: {one-line description}
type: project
---

{The fact or observation}

**Why:** {Context from the retro}
**How to apply:** {How this shapes future suggestions}
```

### Rules for memory creation

- Only create memories the user has explicitly validated during the reflection
- Merge with existing memories when the learning extends a prior pattern
- Use absolute dates (from the retro context), not relative
- Maximum 3-5 memory files per retro — distill, don't dump

## Step 4 — Write retro document

Create a dated retro doc capturing the full reflection:

```bash
mkdir -p docs/swain-retro
```

File: `docs/swain-retro/YYYY-MM-DD-{topic-slug}.md`

### Retro doc format

```markdown
# Retro: {title}

**Date:** {YYYY-MM-DD}
**Scope:** {EPIC-NNN title / "recent work"}
**Period:** {start} — {end}

## Summary

{Brief description of what was completed}

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| ... | ... | Complete/Abandoned/... |

## Reflection

### What went well
{User's responses, synthesized}

### What was surprising
{User's responses, synthesized}

### What would change
{User's responses, synthesized}

### Patterns observed
{User's responses, synthesized}

## Learnings captured

| Memory file | Type | Summary |
|------------|------|---------|
| feedback_retro_x.md | feedback | ... |
| project_retro_y.md | project | ... |
```

## Step 5 — Update session bookmark

```bash
BOOKMARK="$(find . .claude .agents -path '*/swain-session/scripts/swain-bookmark.sh' -print -quit 2>/dev/null)"
bash "$BOOKMARK" "Completed retro for {scope} — {N} learnings captured"
```

## Integration with swain-design

When swain-design transitions an EPIC to Complete, it should invoke this skill:

```
After completing EPIC transition → invoke swain-retro with the EPIC ID
```

This is a best-effort hook — if swain-retro is not available or the user declines, the EPIC transition still succeeds. The hook is documented in swain-design's completion rules, not enforced by this skill.

## Referencing prior retros

When running a new retro, scan `docs/swain-retro/` for prior retros. If patterns recur across multiple retros, call them out explicitly — recurring themes are the most valuable learnings.

```bash
ls docs/swain-retro/*.md 2>/dev/null | head -10
```
