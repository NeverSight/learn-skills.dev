---
name: slice-and-spine-review
description: >-
  Run a human-in-the-loop whole-repo coherence review of a Sliced Bread
  codebase: inventory slices, the spine, and seams; fan out subagents to
  digest every file with its tests; walk seams in ranked order with the
  human issuing a disposition per stop; review the spine for orchestration
  drift. Use when the user says "review the seams", "slice and spine
  review", "whole-repo coherence review", "walk the seams", or asks whether
  slices still hang together after individual changes passed review. Do NOT
  use for rule-compliance checking on a bounded change set
  (sliced-bread-review), autonomous audit and issue filing
  (sliced-bread-audit), or depth/crust-shape scoring (sliced-bread-depth) —
  this skill is a guided session over the whole repo, not an automated
  check.
---

# Slice and Spine Review

A human-led whole-repo coherence pass with an agentic prep sidecar. Individual
changes can each pass `sliced-bread-review`, `sliced-bread-depth`, and
`sliced-bread-audit` while the seams between slices and the spine accrete
leaky or duplicated logic no bounded-diff check ever sees. This skill
inventories the repo, fans out digests, then walks every seam with a human in
the loop.

## Invocation

```text
/slice-and-spine-review [scope: slice names | seam ids | full]
```

Default scope is `full`. A named scope (slice names or seam ids) limits
Phase 2's walk and Phase 3's spine visit to the matching seams and use cases,
but Phase 0's inventory and matrix still cover the whole repo so ranking has
full context.

## Terms

- **Slice** — a `domains/*` module in doctrine role, not necessarily a
  literal directory named `domains`.
- **Crust** — a slice's public seam in the language's native form (exported
  identifiers, package `__init__` surface, index module, public class
  surface, or the positional root for languages with no native visibility).
  Full rationale:
  <https://cheeselord.dev/sliced-bread-architecture/reference/sliced-bread/>
  (in-repo: [[architecture/crust-definition]]).
- **Spine** — `app/use_cases` plus the composition root (`app/bootstrap`).
- **Seam** — a crossing edge, one of exactly three kinds: slice-slice (crust
  import or event), spine-slice, adapter-port binding. Distinct from a
  Feathers-style test-substitution seam.

## Phase 0 — Inventory

1. Enumerate slices (crusts), the spine, and every seam crossing them,
   classified into the three edge kinds above.
2. Derive **hot paths** from caller-graph code intelligence (dependency
   closure / call hierarchy from entrypoints through the spine into slices).
   Hot paths feed seam ranking (below), SeamDossiers (Phase 1), and spine
   visit order (Phase 3).
3. Build the **slice link-level matrix**: for every slice pair, one ordinal
   level with its evidence:

   | Level | Meaning             |
   | ----- | ------------------- |
   | L0    | No link             |
   | L1    | Event-linked        |
   | L2    | Crust import        |
   | L3    | Multi-symbol import |
   | L4    | Co-change hot       |

   Every cell records the pinned evidence trio (`imports`, `co_change`,
   `hot_paths`, per `references/formats.md`) regardless of level; a level's
   meaning may cite its distinguishing detection input in prose (e.g. an
   event link for L1, multiple imported symbols for L3) without that input
   becoming a separate evidence field.

   L4 (co-change hot) fires on a high co-change score or hot paths crossing
   the pair with no import requirement — the ordinal ladder does not imply
   L4 requires an import.

   Pin the schema in `references/formats.md`; do not restate field shapes
   here.

4. **Rank the seam walk** change-coupling-first: sort seams by `co_change`
   descending (primary key); break ties with a composite of 0-1-normalized
   terms (tunable):

   ```text
   tiebreak = w_f * norm(fan_in) + w_d * depth_verdict_weight
            + w_h * norm(|hot_paths_crossing|)
   norm(x) = x / max(x over all seams)   # 0 when the max is 0
   ```

   - `fan_in` — raw static fan-in count crossing the boundary; normalized to
     [0,1] by the max fan_in across all seams.
   - `depth_verdict_weight` — [0,1], see the verdict table below.
   - `|hot_paths_crossing|` — the length of the SeamDossier's
     `hot_paths_crossing` array (a string[] of hot-path identifiers),
     normalized to [0,1] by the max count across all seams.

   Starting weights `w_f=0.4, w_d=0.35, w_h=0.25`; adjust per repo and
   record the adjustment in the session report.

   `co_change` is continuous, so in practice the composite orders seams with
   equal — typically zero — co-change; the weights matter most for the
   never-co-changed tail.

   `depth_verdict_weight` maps `sliced-bread-depth` verdicts onto [0,1] by
   boundary-trouble signal strength (per that skill's own semantics); a
   seam takes the max of its two sides' slice verdict weights, and a
   non-slice side (spine, adapter/port) contributes 0. Verdicts come from a
   `sliced-bread-depth` run or its latest report; when no depth report is
   available, set `depth_verdict_weight = 0` for all seams and record the
   degradation in the session report, mirroring the shallow-git-history
   degradation rule below:

   | Verdict | Weight |
   | ------- | ------ |
   | extract | 1.0    |
   | narrow  | 0.75   |
   | watch   | 0.5    |
   | intent  | 0.25   |
   | healthy | 0      |

5. `common/` edges get a stop in the walk only when co-change flags them —
   do not stop on every `common/` import by default.
6. **Shallow git history** degrades ranking to fan-in only; say so plainly in
   the session output (Phase 4). Never fail the review for missing history
   depth.

## Phase 1 — Fan-out

Before the human session starts, fan out one subagent per file+test pair
within the invocation's scope: the files (and their tests) of in-scope
slices, plus the spine, plus the far-side slices of every seam touching an
in-scope slice — a seam is only judgeable with both sides' dossiers — or
the whole repo when scope is `full`.
Use the Workflow tool when the harness provides it; fall back to the Agent
tool otherwise.

Each subagent produces a **FileDigest** conforming to the pinned schema in
`references/formats.md`: surface exposed, surface used, behavior assertions
extracted from its tests, and duplication suspects. A file with no tests
carries the `UNTESTED` marker in place of behavior assertions — do not infer
assertions from implementation reading.

Roll FileDigests up:

- **SliceDossier** per slice — crust surface, internal files, assertion map,
  mass.
- **SeamDossier** per seam — derived from the SliceDossier(s) on slice
  sides (a bare identifier + summary for a non-slice side) plus co-change
  and hot-path evidence from Phase 0.

Every dossier stamps the commit it was built from (staleness guard — if the
session spans edits, a dossier older than the current HEAD at its path is
stale and must be rebuilt before its stop, not silently trusted).

All schemas live in `references/formats.md` — cite that path in dossiers and
prompts; do not duplicate the schemas here.

## Phase 2 — Seam-walk

Guided session, one stop per seam in rank order:

1. Present a **stop card**: seam id, edge kind, link level (slice-slice
   seams only), both sides' summaries (SliceDossier summary for a slice
   side; identifier + one-line summary for a spine or adapter/port side),
   co-change and hot-path evidence, candidate findings from the dossiers.
2. The human interrogates freely — the agent answers from dossiers plus live
   code intelligence (search, read, caller graph), not from memory or
   speculation.
3. The human issues exactly one disposition per stop:

   | Disposition  | Meaning                                             |
   | ------------ | --------------------------------------------------- |
   | pull-up      | Duplicated/leaked logic moves up into a shared seam |
   | push-down    | Logic moves down out of the seam into a slice/spine |
   | rethink-seam | The edge kind or direction itself is wrong          |
   | healthy      | No action                                           |

4. Record the verdict (rationale, follow-ups) and move to the next seam in
   rank order.

The human may stop the walk at any point; coverage (seams visited vs.
total) is recorded in the session report regardless of where the walk ends.

## Phase 3 — Spine review

Visit `app/use_cases` hot-paths-first (using Phase 0's hot-path derivation
for visit order), then the composition root:

- **Orchestration-only check** — a use case that contains inline domain
  logic (branching business rules, calculations, invariant checks) rather
  than delegating to slices is a push-down candidate.
- **Composition-root wiring check** — `app/bootstrap` wires adapters to
  ports and use cases; any domain logic or adapter-specific branching found
  there is a push-down candidate into the adapter or the relevant slice.

Spine findings feed the same disposition set as Phase 2 and land in the same
session report.

## Phase 4 — Close-out

1. Write the session report to `.cheese/slice-and-spine/<repo>/<date>.md`:
   stops visited, coverage, verdicts, the link-level matrix, and a note on
   any ranking degradation (shallow history, adjusted weights).
2. Every **consequential** verdict (pull-up, push-down, rethink-seam — not
   healthy) becomes an ADR-backed wiki page under `.hallouminate/wiki/`.
   Resolve the exact namespace (`decisions/` vs `architecture/`) against the
   wiki's own ADR conventions at the first close-out in a repo, and state
   the resolution in the session report so later runs are consistent.
3. Render remaining follow-up work as a handoff menu (`/mold`, `/cook`) —
   do not silently drop unaddressed findings.

## Non-goals

- Not rule-compliance checking on a bounded diff — use `sliced-bread-review`.
- Not autonomous audit or issue filing — use `sliced-bread-audit`.
- Not depth or crust-shape scoring — use `sliced-bread-depth`.
