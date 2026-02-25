---
name: standup
description: Generate a standup report from Goldfish memory across all projects
allowed-tools: mcp__goldfish__recall, mcp__goldfish__plan
---

# Standup — Cross-Project Status Report

## What This Does

Generates a concise standup report by recalling checkpoints across all workspaces and reviewing active plans from multiple sources. Covers what happened, what's next, and what's stuck.

## How to Generate a Standup

### Step 1: Recall cross-project activity

```
mcp__goldfish__recall({ workspace: "all", days: 1 })
```

For a Monday standup covering the weekend:
```
mcp__goldfish__recall({ workspace: "all", days: 3 })
```

For a custom range:
```
mcp__goldfish__recall({ workspace: "all", from: "2026-02-10", to: "2026-02-14" })
```

### Step 2: Gather plans from ALL sources

Plans may exist in two locations per project. Check BOTH:

**Source 1: Goldfish plans** — already included in recall output if an active plan exists.

**Source 2: Project plan docs** — scan `docs/plans/*.md` in each project that appeared in the recall results. Read files modified in the last 14 days (skip older ones — they're likely completed). Look at the `**Status:**` field in the header of each file.

### Step 3: Assess plan status from evidence

Do NOT blindly trust the Status field in plan docs. Cross-reference against checkpoints:

- **Status says "Approved" + checkpoints show all tasks done** → effectively complete, note as done
- **Status says "Approved" + checkpoints show partial progress** → in progress, report remaining items
- **Status says "Approved" + no checkpoint activity** → upcoming work, report as planned
- **Status says "Complete"** → trust it, skip or mention briefly as done

For Goldfish plans (from recall), use the plan's status field directly — it's managed by the agent via the plan tool.

### Step 4: Synthesize the report

## Report Format

Structure the standup with these rules:

- **One bullet per accomplishment.** Each on its own line for easy scanning.
- **Lead with impact, not activity.** "Shipped auth refresh tokens" not "Worked on auth."
- **Use past tense** for done items. "Fixed," "Implemented," "Shipped."
- **Blockquote (`>`) for forward-looking items.** Visually separates past from future.
- **Abbreviated month names** in headers. `Feb 14` not `February 14`.
- **Date range in header** when covering multiple days (`Feb 12–14, 2026`).
- **Always state blockers explicitly.** If none, say "Nothing currently blocked."

## Multi-Project Format

When checkpoints span multiple projects, group by project with bullets for accomplishments, blockquotes for next/blocked, and plan references:

```
## Standup — Feb 14, 2026

### goldfish
- Implemented 4 skill files with behavioral language patterns
- Converted tool handlers from JSON to markdown output
> Next: Test skills with live agent sessions
> Plan: v5.1 skills refresh — 2/4 tasks complete (docs/plans/2026-02-16-v5.1-implementation.md)

### api-gateway
- Fixed rate limiter race condition in Redis cluster mode
- Added integration tests for multi-node scenarios
> Next: Deploy to staging, run load tests
> Blocked: Waiting on DevOps for staging Redis cluster
```

## Single-Project Format

When all checkpoints are from a single project, drop the project grouping and use section headers:

```
## Standup — Feb 14, 2026

### Done
- Implemented 4 skill files with behavioral language patterns
- Converted tool handlers from JSON to markdown output

### Up Next
- Test skills with live agent sessions
- v5.1 skills refresh: workspace env var implementation (2/4 tasks complete)

### Blocked
- Nothing currently blocked
```

## Synthesis Rules

- **Be concise.** A standup is 2 minutes, not 20. One line per accomplishment.
- **Group by theme.** Five checkpoints about "auth" become one bullet: "Implemented auth token refresh with rotation."
- **Highlight blockers prominently.** These are the most actionable items in a standup.
- **Skip noise.** Minor refactors, formatting changes, and config tweaks don't need individual mentions unless they were the main work.
- **Use past tense for accomplishments.** "Shipped," "Fixed," "Implemented" — not "Working on" for done items.
- **Surface decisions.** If a checkpoint captured an architectural decision, mention it briefly — the team may need to know.
- **Include plan progress.** When active plans exist, include a brief progress summary (e.g., "3/5 tasks complete") in the Up Next section.

## Handling Edge Cases

### No checkpoints found
Report honestly: "No activity recorded in the requested period." Don't fabricate.

### Single project only
Use the single-project format above (Done / Up Next / Blocked sections).

### Too many checkpoints (20+)
Be more aggressive about grouping. Summarize by theme rather than listing individual items. A standup with 15 bullet points defeats the purpose.

### No plans found
That's fine — just skip the plan progress lines. Not every project has active plans.

### Plans in docs/plans/ but no Goldfish plan
Include them in the forward-looking section. Plans don't need to be in Goldfish to be useful for standup.

## Critical Rules

- **Do NOT ask the user what to include.** Recall gives you everything. Synthesize it yourself.
- **Do NOT fabricate activity.** Only report what checkpoints actually show.
- **Keep it standup-length.** If your report is more than a screenful, you're being too verbose.
- **Include dates** when covering multi-day ranges so the reader knows the timeline.
- **Check BOTH plan sources.** `.memories/plans/` (via recall) AND `docs/plans/` (via file reading). Missing one source means an incomplete forward-looking view.
- **Infer plan status from evidence.** Don't trust stale Status headers — verify against checkpoint activity.
