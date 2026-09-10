---
name: check-wayfinder-maps
description: Survey every wayfinder map on a repo's tracker and report which ones are ready for implementation, which still have decisions open, and what the next move is on each.
argument-hint: "The repo (owner/name), if not the current one"
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [planning, wayfinder, github, survey]
---

# Check Wayfinder Maps

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step. Reading a single map needs no permission — that is `/read-the-map`, and it is callable.

A read-only survey across **all** wayfinder maps on one repo. `/wayfinder` works one map at a time and never steps back to ask *"where is the whole effort?"* — this skill answers that in one table — what's decided, what's ready to build, what's still fog, what's blocking what — and hands back a copyable prompt per map to act on it.

**Reading a map is `/read-the-map`'s job; this skill reads many.** Every map here goes through that skill's checklist and comes out with its verdict — the definitions live there, not here. What this skill owns is everything the plural makes possible: ordering by readiness, the bottleneck, the gap nobody noticed.

**This skill never writes.** No claims, no comments, no closes, no map edits. It reads the tracker and reports. If the survey surfaces work worth doing, hand it to `/wayfinder`, `/decisions-to-specs`, or `/specs-to-tickets` — don't do it here.

## Process

### 1. Establish the repo — use what you have, ask rather than search

Resolve the repo from what is **already in front of you**, in this order:

1. The argument, if given (`owner/name`).
2. The current working directory's git remote — `gh` infers this automatically inside a clone.
3. Unambiguous existing context — the session has been working in one repo, or the user named one earlier and nothing since suggests otherwise.

If none of those settles it, or two of them disagree, **ask the user which repo, immediately** — one question, as the first thing you do.

The line is between *knowing* and *hunting*. Context already in hand is free and usually right; use it. What's out of bounds is going to look: scanning the filesystem for candidates, walking directories for `.git`, listing the org's repos to pick a likely one. A search that lands on the wrong repo costs far more than a question, and it makes the user wait for the wrong answer.

**Done when:** you have exactly one repo, reached without a search.

### 2. Learn how this tracker expresses wayfinding

Follow `/read-the-map`'s **Tracker conventions**. It is a per-repo lookup, so do it once here, not once per map.

**Done when:** you know how to list a map's children and read their blocking state.

### 3. Run `/read-the-map`'s checklist against every open map — in bulk

List every **open** map, then cover **every item on that checklist for every one of them**: the map body whole, its children's state and blocking, the build backlog, the frontier, a verdict, a next move.

**Satisfy the items however is cheapest.** One query for all maps' children beats a pass per map; one query for the repo's open non-wayfinder issues covers every map's backlog at once. Bulk is an efficiency, not a shortcut — a map whose body you skipped because a batch query didn't return it has not been read.

The one item that stays per-map is the map body: read each one whole. That is the bulk of the work here and it is the necessary cost — readiness isn't visible from titles or ticket counts.

**Done when:** every open map carries a verdict and a one-line next move, and none was reached by inference from its ticket counts.

### 4. Report: the table, then a prompt per map, then what it adds up to

Three parts, in that order. Refer to every map and ticket **by name**, linked — never a bare `#42`.

#### The table

**Map number first.** It is the column that identifies the row, and it is what every prompt below repeats — a reader matching a block to its row should not have to read across a title to do it.

```markdown
| # | Map | Open decision tickets | Ready for implementation | Next move |
|---|---|---|---|---|
| [157](url) | <map title> | <count + named open tickets, or "0 — all closed"> | **<verdict>** | <one line> |
```

Order the table by readiness — buildable maps first, deferred stubs last — so the top of the table is the takeable work.

#### One prompt per map, below the table

The `Next move` column says what to do; these are what to **type** to do it. One block per row, in the table's order, each under a one-line label naming the map — the blocks are bare prompts and otherwise indistinguishable once stacked:

**157 — Presentation timing**
```
/wayfinder 157 /decisions-to-specs in repo mtngtools/mtng-dotnet-mono
Work in a worktree.
```

`/whats-next` owns the prompt shape — the `/wayfinder <map#> <next thing> in repo <owner/name>` line, which moves carry the worktree reminder, and how labels read. Follow it; do not invent a second format here.

- **One block per map, never two.** Weighing doors on a single map is `/whats-next`'s job. This skill's answer for a map is the one move its verdict already named.
- **Separately copyable.** Its own fenced block, the prompt and nothing else inside it, no prose fused onto the end. A reader clicks copy once and pastes into a fresh session unchanged.
- **A map with nowhere to go gets no block** — `Done`, blocked, or deliberately deferred. Say that on the label line rather than handing over a prompt that should not be run.

#### What that adds up to

Three or four short paragraphs, no bullets-for-their-own-sake, calling out

- how many maps are through their decisions, and which offer the cheapest work
- every genuinely open decision ticket across all maps (usually a very short list) and whether any two are the same underlying question
- **the bottleneck** — the map the most other maps wait on
- **the quiet gap** — a map spun out of another map's charting and then never followed up. These hide well: zero open tickets, so they look finished, but their body is one line

**Done when:** the user can pick their next session off the table without opening a single issue, and start it by copying one block.

## Cost

`/read-the-map` allows zooming into a ticket body; at one map that is cheap, and across ten it is the difference between a survey and an afternoon. **Spend it rarely** — only where a map's `Notes` point at a ticket as needing revision and you can't tell why. Everything else the checklist asks for is list-level, and list-level data comes in bulk.

## Where this sits in the flow

Outside the flow, looking down at it. `/wayfinder` → `/decisions-to-specs` → `/specs-to-tickets` → `/implement` all operate on **one** map; **`/check-wayfinder-maps`** reads across all of them and tells you which one to enter, and by which door. Once you are on one, `/read-the-map` and `/whats-next` take over — the same checklist, one map deep.

Run it when returning to an effort after time away, when several maps are live at once and it's unclear which is takeable, or before planning a stretch of work.
