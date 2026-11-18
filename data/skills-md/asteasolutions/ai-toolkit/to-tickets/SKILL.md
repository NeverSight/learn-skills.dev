---
name: to-tickets
description: Break a plan or conversation into tracer-bullet vertical slices as a work-tree map (_map.md + leaf docs). Local first; mirror to GitHub only when asked. Use when a goal is too big for one change; helm's Plan phase reaches for this on decomposition.
---

# to-tickets

Decompose work into **tracer-bullet** vertical slices. Write helm's work-tree shapes: `_map.md` plus one leaf doc per ticket (see `helm/references/artifacts.md` if present).

## Publish policy

1. **Always write local** under `.scratch/<goal-slug>/` — this is the program counter.
2. **Also mirror to GitHub** only when the user asks for GitHub, or already pointed at an issue URL/id. If `docs/agents/issue-tracker.md` exists, follow its GitHub conventions for that mirror.
3. Never skip the local write. Never ask which tracker after a local-only run.

## Process

### 1. Gather context

Work from the conversation. If the user passes a reference (spec path, issue number/URL), fetch and read it.

### 2. Explore (optional)

If needed, explore the codebase. Prefer any domain vocabulary the repo already has. Look for prefactoring — *make the change easy, then make the easy change*. Prefactoring is its own ticket, done first.

### 3. Draft vertical slices

Each ticket:

- Cuts a narrow but complete path through every layer it touches (schema, logic, interface, tests) — vertical, not horizontal
- Is demoable / verifiable on its own
- Fits in one fresh context as one change

Give each ticket **blocking edges** — tickets that must finish before it starts.

**Wide refactors** (one mechanical change with huge blast radius) are the exception: sequence as expand → migrate batches → contract, not forced tracer bullets.

### 4. Quiz the developer

Present a numbered list: **Title · Blocked by · What it delivers**. Ask granularity, edges, merge/split. Iterate until approved.

### 5. Write local artifacts

1. **`_map.md`** — overarching intent + ordered task list with status and blockers:

```markdown
# <goal title>

## Intent
<overarching what + why>

## Tasks
1. [pending] <task-slug>
2. [pending] <task-slug> — blocked by: 1
```

2. **One leaf doc per ticket** at `.scratch/<goal-slug>/<task-slug>.md` — Intent only at creation (Plan comes later when that leaf is planned):

```markdown
# <ticket title>

## Intent
<what to build — end-to-end behaviour, not a layer checklist>

### Done when
- [ ] <acceptance criterion>
- [ ] <acceptance criterion>
```

No brittle file paths or code. Exception: decision-encoding prototypes may be inlined.

Do not write under `issues/`. Do not modify any parent issue on a tracker.

### 6. GitHub mirror (opt-in)

If publishing to GitHub: create one issue per ticket in dependency order (blockers first). Use native blocking/sub-issue links when available; otherwise put blockers in the body. Apply labels only if the repo already documents them and the user wants them — don't invent a triage vocabulary. Keep local `_map.md` + leaf docs as the resume source of truth.
