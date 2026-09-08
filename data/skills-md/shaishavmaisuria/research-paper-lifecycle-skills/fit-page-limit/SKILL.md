---
name: fit-page-limit
description: >-
  Helps a paper hit its target length: recommends exactly what to compress when
  it is over the page limit, or what to add with substance when it is too
  short. Use when a researcher says "I'm over the page limit", "compress my
  paper", "what should I cut", "trim two pages", "my paper is too long", "help
  me fit NeurIPS's limit", "my paper is too short", "I have space left, what
  should I add", or "where is all my length going". Runs a section-by-section
  length analysis, then gives a prioritized, value-aware plan: which low-value
  sections to condense or move to an appendix, while protecting contributions,
  results, and citations, or which thin sections to develop. Never deletes
  evidence to fit and never pads to fill. Trigger words: page limit, compress,
  trim, cut down, too long, too short, over the limit, fit the limit, what to
  cut, what to add.
---

# Fit Page Limit

Two sides of the same problem: a paper that is **over** the limit and needs
careful cuts, or a paper that is **under** and needs useful substance rather
than filler. This skill maps the draft section by section, then gives the author
a prioritized plan for whichever direction they need.

It coordinates with [`polish-prose`](../polish-prose/SKILL.md) for sentence-level
tightening, [`refactor-structure`](../refactor-structure/SKILL.md) for larger
reorganization, [`polish-tables-figures`](../polish-tables-figures/SKILL.md) for
visual layout, and [`preflight-check`](../preflight-check/SKILL.md) when the
page limit comes from a venue rule. Run it after the draft is roughly complete.

## When to use

- The draft is over the limit and the author needs to know where the bulk is.
- The draft is under the target length and the author wants to use space well.
- The author asks for a length map: "where is all my length going?"

## Inputs

- The `.tex` source.
- The real compiled page count, if available, to calibrate the estimate.
- The target: a venue page limit or a length the author names.
- The venue CFP or profile, if the target comes from a venue.

## Process

1. **Map the length.** Run the analyzer from this skill directory; do not
   eyeball where the pages went.

   ```bash
   python3 scripts/section_budget.py paper.tex --target-pages 10 --current-pages 11
   ```

   It reports per-section words, percentage of the paper, estimated pages, and
   the over/under gap. `--current-pages` calibrates words per page to the
   author's actual compile. Use `--json` for machine-readable output.

2. **Confirm what counts.** Re-verify the venue's limit and exclusions against
   the live CFP before relying on appendix moves or excluded sections. A stale
   page limit can desk-reject the paper.

3. **Pick the right branch.** Use
   [references/resize-tactics.md](references/resize-tactics.md) to turn the
   map into a value-aware resize plan.

### If over: compress value-aware, never blind

Rank sections by **compressibility x low impact**, and cut there first:

- **Redundancy**: the same point repeated in the intro, method, and conclusion.
- **Over-long related work**: condense paragraph-per-paper prose into clusters
  that state only the delta that matters.
- **Verbose method/setup**: tighten with `polish-prose`; cut walkthroughs a
  figure already shows.
- **Move, do not delete**: push proofs, extra results, or implementation detail
  to an appendix only when the venue excludes it.
- **Figures/tables**: resize, merge subfigures, or drop a redundant baseline
  column with `polish-tables-figures`.

Protect contributions, headline results, and every citation. Present estimated
savings per cut and let the author approve before editing. Never delete a
result, claim, or reference to hit a number.

### If under: expand with substance

A short, complete paper can be fine; say so. If there is real room to strengthen
it, suggest substance: a missing ablation, deeper error analysis, limitations
or threats to validity, clearer motivation, a worked example, or a related-work
gap. Flag suggestions that would merely pad. Hand drafting to the writing
skills.

## Output

A length map and prioritized resize plan:

- **Over**: ranked cut list, estimated savings, and protected material.
- **Under**: substantive additions ranked by value.

Write durable outputs to the user's local `paper-workspace/writing/` directory
when a workspace exists. The skill recommends and explains; the author decides
and edits.

## Guardrails

- Never delete results, claims, or citations to fit.
- Never pad to fill.
- Page numbers are estimates; tell the author to compile and check the real
  count.
- Re-verify venue limits and exclusions against the live CFP before advising
  appendix moves.
- Copilot, not pilot: propose the plan; the author approves and edits.

## Memory

Uses the shared `.paper-memory/` convention documented by
[`paper-profile`](../paper-profile/references/paper-memory-convention.md).

- **At start:** read `lessons.md` for recurring overspend patterns, such as
  "related work always runs long".
- **At end:** append `date - fit-page-limit - over/under - where the length went
  - what was cut/added` after deduping.
- Create `.paper-memory/` on demand in the user's paper directory. It is local
  only and should usually be ignored by git.
