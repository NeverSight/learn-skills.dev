---
name: pwk-status
description: "Show all active pipeline topics and their phase/progress. Use when the user asks 'where are we', 'status', 'what's in flight', or when resuming and unsure which design to continue. Read-only discovery. Not a pipeline phase."
---

# Status

Report on in-flight pipelines in this working tree (a worktree has its own `docs/plans/`, so run status in each). Read-only: this skill **does not unlock the guard**, so it runs fine inside the design read-only phase — invoke the next phase's skill yourself if you want source edits (the guard follows the skill).

Any command or tool recipe in this skill is an example, not the requirement — when your host grants a better tool for an operation (a sandboxed batch executor — e.g. `codemode` on pi ≥ 1.0.0 — a structured file API), use the better tool and treat the recipe as a fallback; the only exact exceptions are this kit's `scripts/` helpers and plain `git` invocations, whose deterministic output is the point.

## Process

0. **Verify the root** — run `pwd` (or your shell's equivalent) and `git rev-parse --show-toplevel`; mismatch → report both paths and stop; never `cd` (a worktree root counts).
1. **Discover** — List `docs/plans` recursively, excluding docs/plans/completed/, for `*-design.md`, `*-progress.md`, and `overview.md` (topic docs live in `docs/plans/<date>-<topic>/` folders — archived work is not in flight) — this working tree only; take each topic’s `Feature phase:` line header-only (`grep -m1 '^Feature phase:' <file>`). Use whatever recurses in your harness; one example: `find docs/plans -name '<suffix>' -not -path '*/completed/*'`. With a sandboxed batch executor (e.g. `codemode` on pi ≥ 1.0.0) the listing and every phase extraction are one call, returning only the summary lines (adapt the paths to the verified root when your cwd differs):

   ```javascript
   const designs = (await tools.bash({ command: "find docs/plans -name '*-design.md' -not -path '*/completed/*' | sort", timeout: 15 })).output.trim();
   const files = designs ? designs.split('\n') : [];
   const shellq = (s) => "'" + s.replace(/'/g, "'\\''") + "'";
   const heads = await Promise.all(files.map(d =>
     tools.bash({ command: "grep -m1 '^Feature phase:' " + shellq(d.replace('-design.md', '-progress.md')), timeout: 15 }).then(r => r.output.trim() || 'design')));
   return text(files.map((d, i) => d + ' — ' + heads[i]).join('\n') || 'no in-flight topics');
   ```

2. **State per topic/part — map the header.** The body (execution summary, review reports, code digest) carries nothing status needs, and neither do design docs. A header reading `Setup: pending` renders the topic as **`awaiting setup`** — the setup checkpoint was never approved (the slot is only ever written when the design doc has a `## Setup` section, so the header alone decides — no design-doc read) — ahead of any phase-derived state below. Map the line to the displayed state:
   - `done` → **`done`** — terminal, never shown as in-flight; every row is resolved (`✅` passed, `❌` failed, `⏭` skipped — resolved, not necessarily passed). Append the tally as `N/N` when wanted — the Requirements-table row count, scoped to that table because the Execution summary rows share the same `| <n> |` row shape and a bare grep would double it (e.g. `sed -n '/^## Requirements/,/^## Execution summary/p' <file> | grep -c '^| [0-9]'`). Counting `❌`/`⏭` rows over that same scoped range (`sed -n '/^## Requirements/,/^## Execution summary/p' <file> | grep -c '^| [0-9].*❌'` / `sed -n '/^## Requirements/,/^## Execution summary/p' <file> | grep -c '^| [0-9].*⏭'` — the same scoping, so Execution-summary rows and prose mentions of the glyphs do not inflate the count) renders the counts, e.g. `done (1 ❌ · 1 ⏭)`, noting finalizing will require `--force-failed` while `❌` rows stand
   - `implementing (k/N)` → `execute k/N` (the tally rides on the line itself — no extra read)
   - `e2e-written` → `execute 0/N` (the E2E is written and the run continues into implementation — never shown as a paused state; N comes from the same Requirements-table-scoped row count as `done` — so no tally renders without a defined source)
   - `reviewing` → `review`
   - `ship-paused` → `ship-paused` — next: `/skill:pwk-executing-tasks` (approve the ship checkpoint); only `done` routes to finalizing.
   - no progress file, only `*-design.md` → `design` — next: `/skill:pwk-executing-tasks`
   - roster-only (named in the overview, no artifacts) → `not started`
   - no parseable `Feature phase` line → `execute` (with tally if parseable).
3. **Group by umbrella** — for each `overview.md`, read its **`## Parts (build order)`** roster (the heading and the `N. <part> — <scope>` item shape are lint-pinned) and roll the parts up by state (the overview carries no status): done, in-flight (design, execute, review, ship-paused, awaiting setup), not-started. A part at the feature-E2E notice (`e2e-written`) rolls up as execute — a routing moment, not a bucket of its own. Print one roll-up line — `<topic> (umbrella): n done · n in-flight · n not-started` — and when every part is `done` append `— all parts done, ready for /skill:pwk-finalizing`; a `done` single-leaf topic gets the same hint. Once the topic finalizes its folder — overview included — is disposed, so it no longer appears here. Topics without an overview print flat.
4. Print a compact table, grouped under any umbrellas, e.g.:

   ```text
   payments-revamp (umbrella): 1 done · 2 in-flight · 1 not-started
     payments-core      done      3/3
     payments-ui        execute   1/2
     payments-review    review    —
     payments-webhooks  not started
   auth                ship-paused   — ready for /skill:pwk-executing-tasks
   ```

   If nothing, suggest `/skill:pwk-brainstorming`.

Keep it short — this is orientation, not analysis. No writes; the `<topic>` slug is the identity.