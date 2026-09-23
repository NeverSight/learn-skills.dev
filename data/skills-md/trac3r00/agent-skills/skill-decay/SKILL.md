---
name: skill-decay
description: Find declared-but-unused skills, tools, or plugins by cross-referencing an inventory (SKILL.md files or a name list) against real usage logs, and fail CI when the dead weight grows past a budget.
when_to_use: Your agent/host loads dozens of skills, tools, or plugins that each cost prompt tokens on every turn, and you suspect many are never actually invoked. You want a deterministic, offline signal for what to prune — which capabilities loaded but were called zero times, or haven't been touched in N days — instead of guessing.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [agent-governance, context-engineering, prompt-budget, usage-audit, dead-code, ci]
---

# Skill Decay

Turn "we have 200 skills" into "we *use* 40 of them" — with receipts.

## Overview

Every skill, tool, or plugin an agent declares is loaded, described, and paid
for in the prompt on **every single turn**. The inventory only ever grows:
adding one looks free, removing one requires proof it's dead, and nobody
gathers that proof. So the context window fills with capabilities that haven't
been invoked in months, quietly taxing latency and token cost on requests that
will never touch them.

`skill_decay.py` is that proof. It cross-references a **declared inventory**
against a **usage log** and reports the decay:

- **never** — declared, loaded, invoked **zero** times in the logs.
- **stale** — used once, but not in the last N days (default 30).
- **live** — actually earning its prompt slot.

It exits non-zero when the number of decay candidates blows a budget, so *"the
inventory grew faster than it's used"* fails CI instead of silently bloating
every request. Nothing from the inventory is imported or executed — `SKILL.md`
is read as text, logs are read as text. Pure stdlib.

This is the other half of a context budget: `context-budget` tells you *how
heavy* each file is, `skill-decay` tells you *whether anyone uses it*. A file
that is both heavy and never-used is the first thing to cut.

## When to use

- An agent/plugin host declares dozens+ of skills/tools and per-turn prompt
  cost is climbing, but you can't tell which ones are dead.
- You want CI to fail when the count of never/stale capabilities exceeds a
  budget, forcing a prune-or-justify decision.
- You're deciding what to archive and want a usage table, not a vibe.

Not for: proving a skill is *good* (a rarely-used skill can still be critical —
read `never` as a *review prompt*, confirm it isn't a break-glass tool before
deleting), or measuring token weight (that's `context-budget`).

## The method

1. **Point it at the inventory and the usage.**
   ```bash
   # inventory = a tree of SKILL.md files; usage = your agent logs
   python scripts/skill_decay.py --skills-dir ~/.hermes/skills \
     --logs ~/.hermes/logs --stale-days 30 --max-decay 20
   ```
   Inventory names come from each `SKILL.md` frontmatter `name:` (or the
   containing directory name). If you don't have `SKILL.md` files, pass a flat
   list instead: `--names plan,codex,dogfood,spike`.
2. **Read the three tiers.**
   - *never*: declared, never invoked. The prime prune candidates.
   - *stale*: used once, but not within `--stale-days`. Decaying.
   - *live*: actively used — leave them alone.
   Each row carries the invocation count and days-since-last-use so you can
   rank the cut list by cost-of-keeping.
3. **Wire it into CI.** The tool exits non-zero over the decay budget:
   ```yaml
   # fail the build when >20 skills are dead or decaying
   - run: python scripts/skill_decay.py --skills-dir skills --logs logs --max-decay 20
   ```
   Or be strict with `--fail-on-never` to block *any* never-used skill from
   merging. Now inventory bloat is a red build, not a slow creep.
4. **Prune the top, re-measure.** Archive a confirmed-dead skill, re-run. The
   `decay_candidates` count is the scoreboard.

## How usage is matched

- Each inventory name is matched as a **whole token** (word/path-segment
  boundaries), so `plan` never counts a hit inside `planet` or `planner`.
  Hyphens and underscores are treated as word-internal, so `skill-decay`
  matches exactly and not `skill`.
- Any `YYYY-MM-DD` on a usage line is read as that invocation's timestamp; the
  latest one becomes the item's *last-seen* date, which drives staleness. Logs
  with no dates still produce never/live verdicts — you just lose the stale
  tier (everything used is `live`).
- Usage sources: one or more `--logs` files/dirs (repeatable), or stdin. A
  directory is walked recursively.

## Anti-patterns

- **Deleting a `never` skill on sight.** Zero invocations is a strong signal,
  not a verdict — a break-glass / disaster-recovery skill *should* be rarely
  used. Confirm it isn't intentionally dormant before archiving.
- **Auditing against too short a log window.** If your usage log only covers a
  week, a monthly skill looks dead. Point `--logs` at a window at least as long
  as your longest legitimate usage cadence.
- **Matching substrings.** Naive `grep skillname` over-counts (`plan` inside
  `planet`) and under-cuts real dead weight. This tool matches whole tokens on
  purpose — don't "fix" it back to substring matching.
- **Treating the tool as its own exception.** A decay auditor that itself never
  runs is dead weight. Put it in CI so it runs on every change.

## Example

```
$ python scripts/skill_decay.py --skills-dir skills --logs agent.log --stale-days 30 --max-decay 5
Skill-decay report
==============================
inventory: 42   as-of: 2026-07-07   stale>30d
live: 30   stale: 5   never: 7   decay-candidates: 12

name              calls  last-use     decay
------------------------------------------------
touchdesigner-mcp     0  -            never
godmode               0  -            never
...
p5js                  1  2026-04-02   stale (96d)
plan                171  2026-07-07   live (0d)
FAIL: decay_candidates 12 > max_decay 5
$ echo $?
1
```
