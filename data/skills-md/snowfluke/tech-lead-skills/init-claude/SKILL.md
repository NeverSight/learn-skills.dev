---
name: init-claude
description: 'Generate the project CLAUDE.md as a dense, agent-facing operating manual, at the end of the documentation pipeline just before build starts. Distills the technical specs, coding standard, task breakdown, and deployment plan into the rules an agent must hold in context: tech stack, repo layout, architecture laws (file-size cap and split strategy, layering), runtime do/don''t, the verification gate, naming, type-safety, prohibitions, a context-recovery checklist, and a command quick-reference. Use when the user wants to initialize or write CLAUDE.md, an agent operating manual, AGENTS.md, or asks to "init claude".'
---

# Init CLAUDE.md

Write `CLAUDE.md`: the operating manual an agent reads before touching the repo. It is not a doc like the others. The pipeline docs are the source of truth and the place to read in depth; `CLAUDE.md` is the **dense distillation** of the load-bearing rules plus pointers to those docs, written so an agent with limited context still gets the invariants right.

This runs at the **end of the documentation pipeline, just before build**: the technical specs, coding standard, task breakdown, and deployment plan already exist, and this synthesizes them. Three phases: read everything, grill the user on what the docs leave open, then write the manual. Because every agent reads this file before touching the repo, a wrong or guessed invariant here misleads every future build, so resolve the gaps before writing, never invent.

## 1. Read the pipeline docs

`CLAUDE.md` is a synthesis, so read its sources first and pull the real values, never invent them:

- `docs/technical-specs/`: tech stack and versions (`04`), repo layout (`03`), module/service boundaries (`05`), data model and state machines (`06`), env config (`11`).
- `docs/coding-standard/` (or `CODING_STANDARD.md` in an older project): the architecture laws, naming, type-safety, error-handling, and testing rules to restate tersely.
- `docs/task-breakdown/` (or `docs/TASK_BREAKDOWN.md` in an older project): the work model (pre-assigned vs self-pick, scaffold model, reviewer).
- `docs/deployment-plan/` (or `DEPLOYMENT_PLAN.md` in an older project): environments, deploy triggers, the verification/build commands.
- `docs/GLOSSARY.md` (or `GLOSSARY.md` at the root in an older project) and `docs/business/`: domain terms, roles, language policy.
- Any existing `CLAUDE.md` to update in place rather than overwrite.

## 1b. Grill on the gaps

Don't write until the open questions are resolved. Grill the user one at a time (recommending a default and the trade-off for each) on whatever the docs leave ambiguous: the verification command set if not yet fixed, the trailer/commit policy, the file-size cap and split strategy, the layering laws, any prohibition that isn't already pinned in the coding standard. Skip what the docs already answer; never guess an invariant.

## 2. Write CLAUDE.md in the standard structure

Write the sections in [references/layout.md](references/layout.md), in its order. Then append the system prompt block in [references/system-prompt.md](references/system-prompt.md) at the end.

## Writing rules

- Terse and imperative. Agents read this file with little context left, so every line states a rule they need. Restate rules in one sentence and point to the full doc rather than copying it wholesale.
- Real values only: the actual stack versions, command names, paths, roles, and formats from the docs. No placeholders where a real value exists.
- Keep it consistent with the other docs; if `CLAUDE.md` and the coding standard disagree, the standard wins and `CLAUDE.md` must be corrected.
- Write to `CLAUDE.md` at the repo root (or `AGENTS.md` if the project uses that). Update in place if one exists; report what changed.

## Writing conventions (enforced in all output)

- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative tone.
- If a document carries a metadata header (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`), each such line ends with two trailing spaces so Markdown renders them on separate lines.
