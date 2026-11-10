---
name: strategic-revision
description: "Turn external referee correspondence or internal pre-submission feedback into a provenance-safe, DAG-validated revision master plan with atomic tasks, dependencies, critical path, and execution blocks. Use when feedback exists but must be converted into an approved implementation sequence. Not for drafting the reviewer response itself; use $review-response."
argument-hint: "[--external <reviews-pdf-or-folder> | --internal <review-or-synthesis-path>]"
skill-dependencies: [latex-diff, proofread, review-packet, synthesise-reviews]
---

# Strategic Revision — Feedback to DAG-Validated Master Plan

Convert feedback on the author's own paper into a computationally validated revision plan. The shared analytical core produces atomic tasks, a dependency DAG, execution blocks A--E, a critical path, and bottleneck analysis. Provenance determines which of two modes supplies and stores the surrounding artifacts:

1. **External R&R mode** preserves genuine venue correspondence and prepares response-oriented tracking.
2. **Internal revision mode** consumes AI reviews, review syntheses, or informal collaborator feedback without representing them as venue correspondence.

**Provenance:** DAG validation + critical-path architecture adapted from Jukka Sihvonen's strategic-revision skill (https://github.com/jusi-aalto/strategic-revision). the user's ingestion layer (correspondence scaffolding, LaTeX verbatim, R&R routing, venue strategy, coaching) retained.

## When to Use

- Received reviewer or editor reports from a journal or conference
- Need to turn internal pre-submission reviews into an executable revision sequence
- Have a `review-cluster` or `synthesise-reviews` output that needs dependency mapping and critical-path validation
- Need to extend an existing revision DAG with another review of the same draft

## When NOT to Use

- Writing the actual response letter (use generated response blocks as a starting point, then write manually)
- Reviewing someone else's paper (use `proofread` or `peer-reviewer` agent)
- Combining overlapping internal reports without execution planning — use `synthesise-reviews` first
- Applying fixes directly without first producing and approving a plan

## Modes and Provenance Gate

Select the mode from **who authored the source feedback**, not from whether it sounds like a referee report. Full routing and cross-mode rules: [references/modes.md](references/modes.md).

| Mode | Source provenance | Source location | Plan location | External-only artifacts |
|---|---|---|---|---|
| `external` | Human reviewer/editor acting for a venue | `correspondence/referee-reviews/` and/or `correspondence/editorial/` | `correspondence/referee-reviews/{venue}-round{n}/` | Preserved source, verbatim transcription, rebuttal scaffold, venue strategy, `reviews-in` history event |
| `internal` | AI review/skill/agent, manual external-AI output, or informal supervisor/co-author feedback | AI: `reviews/<scope>/<source>/`; human collaborator: `correspondence/internal/` | `reviews/<scope>/strategic-revision/{YYYY-MM-DD-HHMM}/` | None |

An auto-generated "Reviewer 2" report is **internal mode**. A human venue report pasted by the user is **external mode**. If provenance is unclear, ask before creating files. Never copy AI review text into the venue-correspondence record.

**External mode — reviewer-gap extraction (end of run).** After the plan is built, run `skills/_shared/reviewer-gap-extraction.md` on the venue referee reports: capture any generalizable reviewing pattern the human referees raised that our own review agents don't already cover, as `reviewer-gap` signals for the `feedback-review` skill to propose as agent-contract refinements (Phase 2 of the review-agent calibration loop). Internal mode does NOT emit — those sources are our own agents.

## Inputs

Gather the shared inputs first:

1. **Feedback path(s)** — one or more reports, or a `synthesise-reviews` output
2. **Project path** — auto-detect from the current research project when possible
3. **Paper scope** — e.g., `paper-eacl`; `_project` only for project-level feedback
4. **Coordinating author** — who owns revision decisions

External mode also requires venue slug, revision round (default 1), response deadline, and the original venue-supplied review/decision files. Internal mode records the draft identity and review dates; it does not invent a venue round or response deadline.

### External PDF Auto-Discovery

Search for the reviews PDF in this order. Use the first match; if multiple PDFs found at a location, list them and ask the user to pick.

1. `to-sort/*.pdf` — most likely landing spot after download
2. `correspondence/referee-reviews/{venue}-round{n}/*.pdf`
3. `correspondence/referee-reviews/*.pdf`
4. Ask the user for the path if nothing found

## Output Locations

### External R&R mode

```
correspondence/referee-reviews/{venue}-round{n}/
├── {venue}-round{n}-reviews.pdf      (copy of input PDF — source NEVER moved; taxonomy name per rules/submission-file-archive.md, 2026-07-03)
├── {venue}-round{n}-reviews.md       (searchable parsed transcription — required pair with PDF)
├── {venue}-round{n}-rebuttal.md      (empty — for response draft)
├── reviews/                          (individual reviewer files)
│   ├── reviewer-1.md
│   └── ...
├── analysis/
│   ├── comment-tracker.md            (atomic comment matrix with R&R + 5-cat classification)
│   ├── review-analysis.md            (strategic overview + venue strategy)
│   └── reviewer-comments-verbatim.tex (LaTeX transcription)
└── plan/
    ├── REVISION_MASTER_PLAN.md       (six-phase Sihvonen plan — atomic tasks, DAG, blocks, risks)
    ├── revision_tasks.json           (DAG input — see references/task-schema.md)
    └── revision_dag_analysis.json    (computational output — parallel batches, critical path, bottlenecks)
```

**Source PDF preservation:** The original PDF is only ever **copied** to `{venue}-round{n}-reviews.pdf`. Never move, rename, or delete the source.

**Principle:** `correspondence/` holds human exchanges; AI-derived review and planning artifacts stay under `reviews/`. Informal human collaborator feedback may remain in `correspondence/internal/`, while the derived internal plan goes under `reviews/{scope}/strategic-revision/`.

**Submission-history stamp:** ingesting a reviews PDF is a submission event — append a `history:` row (`event: reviews-in`, `round: r{n}`, `files:` pointing at `{venue}-round{n}-reviews.pdf`) to the paper's vault submission entry per `rules/submission-file-archive.md` § history. When the revision is later resubmitted, that resubmission appends its own `response-sent` + `submitted` rows (usually via `session-close` sync).

**No-overwrite rule:** If outputs already exist, version them (`comment-tracker-v2.md`, `REVISION_MASTER_PLAN-v2.md`). Always flag before writing.

### Internal revision mode

```
reviews/{scope}/strategic-revision/{YYYY-MM-DD-HHMM}/
├── source-manifest.md                 (source paths, provenance, dates, hashes)
├── analysis/
│   ├── comment-tracker.md             (atomic findings + verification anchors)
│   └── review-analysis.md             (cross-review picture + readiness decision)
├── plan/
│   ├── REVISION_MASTER_PLAN.md
│   ├── revision_tasks.json
│   └── revision_dag_analysis.json
├── bundle/                            (created at successful closeout)
│   ├── strategic-revision.bundle.zip
│   ├── strategic-revision.manifest.json
│   └── strategic-revision.sha256
└── snapshots/                         (token-conservation baselines — see below)
    └── {label}/                       (e.g. pre-revision/, post-block-C/: main.tex + sections/ + .bib)
```

Internal mode links to its source reports in place and does not duplicate them. It creates no rebuttal file, venue-response transcription, submission-history event, or alternative-venue analysis unless the user separately requests one. Use a new timestamped package for a materially changed draft; use fold-in versioning for another review of the same draft.

When the source feedback was produced from a sealed review packet, `source-manifest.md` records that packet's path, archive SHA-256, canonical artifact SHA-256, and verification receipt. At successful closeout, invoke `review-packet` in `gate-closeout` mode so the exact reviews, analysis, adjudication, DAG, snapshots, and completion receipt form one decision-ready packet. A closeout packet is provenance, not a review verdict, and receives no separate `reviews/INDEX.md` row.

**Snapshot location (mandatory, 2026-08-02).** Token-conservation baselines and any other source snapshots taken during a revision live in the plan package's `snapshots/{label}/` — git-tracked, tied to the plan that uses them. NEVER store revision snapshots under `paper-*/backup/`: that directory is the Overleaf backup automation's mirror surface (rsync `--delete`), and on 2026-07-31/2026-08-02 an unprotected mirror pass in `daily-maintenance.sh` gutted dated snapshot dirs stored there (both the P108 round-1 and round-2 baselines, plus two AIES submission-era archives). The automation's filters have been hardened, but the ownership boundary stands: `paper-*/backup/` belongs to the automation; revision provenance belongs to the plan package.

## Protocol — 11 Mode-Aware Phases

The skill runs 11 sequential phases. Detailed step-by-step procedure: [references/phases.md](references/phases.md).

| # | Phase | Output | Source |
|---|-------|--------|--------|
| 1 | **Provenance + Setup** | Mode lock, scaffold, and source manifest/copy | FB |
| 2 | **Read Feedback** | Structured source data in memory | FB |
| 3 | **Source Records** | External reviewer files or internal source manifest | FB |
| 4 | **Verbatim Gate** | External transcription compiled; internal mode records a justified skip | FB |
| 5 | **Atomic Parsing** | Every distinct request as own SourceID (`R1.a3`, `EiC.2b`) | JS |
| 6 | **Classification** | 5-cat (STRUCTURAL/ARGUMENTATIVE/EMPIRICAL/CLARIFICATION/EDITORIAL) + R&R routing (NEW ANALYSIS / CLARIFICATION / DISAGREE / MINOR) | Both |
| 7 | **Dependency Mapping (DAG)** | Upstream Blockers + Collateral Risks tables → `revision_tasks.json` | JS |
| 8 | **Structural DAG Validation** | `dag_validator.py --validate-only` gate check | JS |
| 9 | **Critical Path Sequencing** | Execution Blocks A-E + GO/NO-GO gate after Block A | JS |
| 10 | **Risk & Conflict Resolution + Decisions** | Conflicts, process risks, and mode-appropriate author decisions | Both |
| 11 | **Computational Optimization + Strategy** | Parallel batches, critical path, bottlenecks + external venue strategy or internal readiness decision | Both |

**JS = Sihvonen phases. FB = the user phases. Both = merged.**

### Phase Dependencies

- Phases 1-4 (mode-aware ingestion) must complete before Phase 5 begins
- Phase 8 is a **hard gate**: cycles → return to Phase 7, do not advance to Phase 9
- Phase 11 requires the Phase 9 block assignments before running full DAG analysis
- Phase 10 author decisions run only on Major/Critical findings (skip Minor/Editorial)

## DAG Validation Quick Reference

**Phase 8 (structural gate):**
```bash
cd correspondence/referee-reviews/{venue}-round{n}/plan
uv run --with networkx python dag_validator.py revision_tasks.json --validate-only
```

**Phase 11 (full analysis):**
```bash
uv run --with networkx python dag_validator.py revision_tasks.json
# Produces revision_dag_analysis.json
```

Copy `dag_validator.py` from `skills/strategic-revision/scripts/` into the plan directory before running. Invoke it through `uv run --with networkx` so the project environment is not mutated.

Full validator documentation: [references/dag-validation.md](references/dag-validation.md).
Task JSON schema: [references/task-schema.md](references/task-schema.md).
R&R routing rules: [references/rr-routing.md](references/rr-routing.md).

## Classification: Two Axes

Every atomic task gets **both** classifications recorded in the comment tracker:

**Category (5-cat, Sihvonen):** structural intent of the change
- 🔴 STRUCTURAL — moves, cuts, reorganizations
- 🟠 ARGUMENTATIVE — theory, narrative, logical framing
- 🟡 EMPIRICAL — new regressions, data work, robustness
- 🟢 CLARIFICATION — definitions, justifications, explanations
- 🔵 EDITORIAL — formatting, typos, figures, terminology

**R&R Routing (FB):** workflow routing
- **NEW ANALYSIS** — needs code/data work
- **CLARIFICATION** — textual fix only
- **DISAGREE** — author adjudication; external mode may produce push-back in the later response, internal mode records Reject/Adapt/Defer
- **MINOR** — trivial or editorial

The two axes are orthogonal: a STRUCTURAL task is usually a CLARIFICATION routing; an EMPIRICAL task is usually NEW ANALYSIS; ARGUMENTATIVE with DISAGREE signals a high-stakes author decision and, in external mode only, a potentially rebuttal-heavy revision.

## Strategic Coaching (Phase 10)

External mode: for each **Major** or **Critical** referee comment, walk the user through:

1. **Understanding:** reviewer's core concern — methodology, theory, or framing?
2. **Position:** Agree / Partially agree / Disagree (with core rebuttal if Disagree)
3. **Risk:** likelihood of reviewer escalation if pushed back on
4. **Response sketch:** one-sentence strategy (not full response)

Record in the comment tracker with two new columns: **Position** + **Strategy**.

Rules:
- Only Major/Critical get coaching. Minor/Editorial auto-classify as Agree.
- the user can say "skip coaching" to auto-classify all remaining as Agree.
- Maximum 2 rounds of dialogue per comment.
- Do not write the actual response letter — that remains the user's job.

Internal mode uses the same risk analysis but records **Decision** (Adopt / Adapt / Reject / Defer) and **Rationale** rather than simulating agreement with a referee. Internal findings never become response-letter claims.

## Strategy (Phase 11)

### External R&R mode

Populate the Publication Strategy section of `review-analysis.md`:

- **Strategy A (minimal revision):** venues that would accept the paper as-is despite reviewer concerns
- **Strategy B (substantial revision):** equal-or-higher prestige venues worth targeting if authors invest in addressing major concerns
- **Conferences:** check CORE rankings via `.context/resources/venue-rankings.md` (CSV: `.context/resources/venue-rankings/core_2026.csv`)
- **Journals:** check CABS AJG via `.context/resources/venue-rankings.md` (CSV: `.context/resources/venue-rankings/abs_ajg_2024.csv`). For SJR, query Elsevier Serial Title API (`SCOPUS_API_KEY` required). Flag journals below CABS 3 only with strong rationale.
- **Recommendation table:** 3-5 venues ranked with rationale. First option should always be "revise for current venue" if acceptance probability >~30%.
- **Key Decision:** frame the core trade-off (speed vs. impact, minimal vs. substantial effort).

### Internal revision mode

Populate a readiness decision instead of a venue-switching exercise:

- **Decision:** `SUBMIT`, `HOLD`, or `DEFER`
- **Blocking tasks:** the incomplete critical-path tasks that determine the decision
- **Scope boundary:** findings explicitly deferred beyond this submission
- **Re-review gate:** the checks that must pass after the DAG is executed

Do not recommend alternative venues in internal mode unless the user asks for venue strategy.

## Critical Rules

1. **External verbatim means verbatim.** In external mode, never paraphrase reviewer text in `reviewer-comments-verbatim.tex`. Copy exactly. Internal mode does not create that artifact.
2. **Every comment gets a SourceID.** No reviewer concern is lost. If in doubt, give it its own ID.
3. **Atomic tasks only.** If a paragraph contains 3 distinct requests, create 3 rows — never collapse.
4. **No invented requests.** Every task traces to a verbatim quote.
5. **Don't overwrite.** Version outputs if present.
6. **Compile the external LaTeX.** In external mode, `reviewer-comments-verbatim.tex` must build cleanly before Phase 5. Internal mode records the provenance-based skip.
7. **Phase 8 is a hard gate.** Cycles block Phase 9. Fix the DAG, re-run validation.
8. **Phase 11 is mandatory.** Do not skip computational optimization — parallel batches and critical path override manual sequencing where they conflict.
9. **Don't write response letters.** The skill produces plans and trackers; writing the rebuttal is the user's job. To inventory *what actually changed* between the submitted and revised manuscript as raw material for the rebuttal, run `latex-diff` (submitted revision vs working tree) — it reports the change list; it does not write the letter.
10. **GO/NO-GO gate after Block A.** If empirical foundation changes key conclusions, escalate to authors before advancing.
11. **Provenance controls routing.** AI-simulated referee reports remain internal; genuine venue correspondence remains external.
12. **External-only side effects stay external.** Internal mode never creates a rebuttal, venue-history event, or referee-verbatim artifact.
13. **Do not cross-fold modes.** A new source with different provenance gets its own package; cross-reference completed work without moving or relabelling source material.
14. **No silent claim-strength moves.** Revision edits touching claim-bearing text follow the claim-strength ladder (`docs/reference/claim-strength-ladder.md`): any move up or down the epistemic scale — including deleting a hedge, scope caveat, or null result — must be authorized by a task's SourceID, and the executing session states the move in its summary. After a revision block completes, run the token-conservation check on each edited file (`uv run python .scripts/check_token_conservation.py --source <pre-revision> --revision <current>`) and reconcile every advisory row (changed number, dropped/added citation) against the tasks that authorized it.
15. **Close out with a Fulfillment Ledger.** When execution completes (final block done, or fold-in close), fill the tracker's Fulfillment Ledger: every reviewer commitment gets `fulfilled` / `partial` / `not_fulfilled` / `acknowledgment_only`, verified **against the manuscript** — read/grep the `.tex` for the promised change; never mark `fulfilled` on the response letter's or the tracker's say-so (exception: `acknowledgment_only`, whose evidence is the letter). `partial` and `not_fulfilled` require an explicit rationale + residual action. (Ported from ARS v3.19 commitment ledger.)
16. **Prepare successful closeout.** After the fulfillment ledger and final DAG validation pass, generate and verify the strategic review packet. Never overwrite an earlier packet or include genuine venue correspondence in an internal packet without explicit authorization.

## Fold-in mode — second-review extension of an existing DAG

When a paper that already has a `strategic-revision` package receives a **second same-mode review** of the same draft, extend the existing DAG instead of starting over.

**Trigger:** "fold in this review", "process this second review", `strategic-revision --fold-in <path>`, or recognising the situation from context (existing `plan/revision_tasks*.json` + new same-mode review file). Cross-mode feedback starts or extends its own provenance package and may only be cross-referenced.

**What it produces** (preserving v1; never overwriting):

- `plan/revision_tasks-v{N}.json` + `plan/revision_dag_analysis-v{N}.json` — incremented version
- v{N} addendum appended to `plan/REVISION_MASTER_PLAN.md` and `analysis/comment-tracker.md` (the same files, not new ones)
- A cross-review picture: where the reviews overlap, what each catches that the other misses, and whether either is a superset (usually neither is — the union is the real picture)
- New review gets its own `reviews/<source-N>.md` and its own row in `reviews/INDEX.md`; v1's row is untouched

**Why this matters:** re-running the full skill loses the v1 verification trail (which findings were checked, which converted to DISAGREE, which got Coaching positions). Fold-in preserves that trail. The DAG itself is the durable artifact; reviews are inputs that grow it.

Full step-by-step (including the OVERLAP / MERGE / NEW disposition axis, versioning convention, and the cross-review picture template): [`references/fold-in-protocol.md`](references/fold-in-protocol.md).

## Templates

Located in `templates/referee-comments/`:
- `comment-tracker.md` — atomic matrix with R&R columns
- `review-analysis.md` — strategic overview template
- `reviewer-comments-verbatim.tex` — LaTeX transcription template

## Cross-References

- `latex-diff` — diff the submitted vs revised manuscript (git revision or backup vs working tree) to build the "summary of changes" and confirm every committed revision has a rebuttal line. Read-only; raw material for the letter, not the letter itself.
- `proofread` — proofread the response letter before submission
- `bib-validate` — run after revision to check bibliography
- `pre-submission-report` — full quality check before resubmission
- `paper-critic` agent — self-review of the revised paper
- `synthesise-reviews` — merge internal review agent reports (different use case — not referee comments)
- `review-packet` — records the reviewed manuscript identity and prepares a successfully completed strategic-revision run for closeout review
- `references/phases.md` — detailed 11-phase protocol
- `references/rr-routing.md` — R&R routing signal words
- `references/dag-validation.md` — DAG validator usage + Phase 6 details
- `references/task-schema.md` — `revision_tasks.json` JSON schema
- `references/modes.md` — mode selection, routing, side-effect, and cross-mode provenance contract
- `references/fold-in-protocol.md` — second-review extension protocol (preserves v1 trail; appends v{N} addendums)
- `scripts/dag_validator.py` — NetworkX-based DAG validator (copy to plan dir before running)
