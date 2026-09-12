---
name: accelint-archive-synthesis
description: Periodically lint the full OpenSpec archive for cross-change decision drift, index/spec reconciliation, and structural over-coupling, the gap nothing else in the QRSPI/OpenSpec stack covers, since every other drift check (accelint-onboard-openspec, accelint-architecture-doc, accelint-qrspi-apply Phase 4) only looks forward from a single change's own artifacts. Use this skill when the user wants to "run archive synthesis," "lint the openspec archive," "check for decision drift," "audit the spec archive for contradictions," "find stale specs," "reconcile the specs index," "check capability coupling," or when accelint-qrspi-archive has surfaced its own suggestion that 15+ changes have archived since the last synthesis run. Also use when the user asks whether an old design decision still holds given everything decided since, whether specs/INDEX.md still matches the actual spec.md files on disk, or whether some capability has become an over-coupled refactor candidate. This skill never runs automatically and never blocks another skill — it is always either a human-invoked audit or an offered suggestion the human accepts explicitly.
license: Apache-2.0
compatibility: Requires the OpenSpec CLI, sub-agent support, and a project already onboarded with accelint-qrspi-archive so that openspec/changes/archive/INDEX.md and openspec/specs/INDEX.md exist and are populated. Routing confirmed findings requires the shared findings - interface (Mode 3 Refresh support) in whichever writer skill(s) a given finding targets; without it, this skill still produces its report but degrades to manual guidance for that step.
metadata:
  author: accelint
  version: "1.2.0"
---

# Accelint Archive Synthesis

Read backward across the entire archived-change history to check whether it still agrees with itself, check the running index itself against the live files it claims to summarize, and surface any capability whose accumulated relationships suggest it has outgrown its own boundaries. This is the "lint" operation in Karpathy's LLM Wiki pattern: `ingest` already exists as `accelint-qrspi-archive`, `query` already exists as artifact loading at propose/apply time, but nothing periodically re-reads the whole corpus to check it is still internally consistent. Every existing drift check in this stack, including `accelint-qrspi-apply` Step 5's own hub-doc refresh, is forward-looking and scoped to one change's own proposal and design. This skill is the only one that looks the other direction — and, since `accelint-qrspi-archive` moved to row-level index patching for its own efficiency, the only one that ever re-checks `specs/INDEX.md` against the `spec.md` files it summarizes at all.

That backward-looking scope is also what keeps this skill's footprint small and deliberate. It reads two indexes and, for genuine candidates only, a handful of `design.md` files and, for the reconciliation check, a lightweight top-of-file read of every `spec.md`. It never rewrites a hub doc directly, and every write it does make — on either index — is a single targeted line, gated behind an explicit human confirmation of that specific finding, and never runs on its own initiative. A human always decides which findings get acted on.

## What This Skill Does

**Automates**: a periodic, corpus-wide consistency check across every archived OpenSpec change, surfacing contradictions between past decisions, flagging capabilities that have become structurally over-coupled, and flagging `specs/INDEX.md` rows that have drifted from the `spec.md` files they summarize.
**Scope**: `openspec/changes/archive/INDEX.md`, `openspec/specs/INDEX.md`, and — for the reconciliation check only — a lightweight read of each `spec.md`'s `## Purpose` heading and `related:` frontmatter. This skill never originates a change, never implements a fix, and never edits a hub doc itself.
**Output**: a CRITICAL / WARNING / SUGGESTION report in the same register as `openspec-verify-change`, plus, only after a human confirms a specific finding, a `Status` column update on the relevant archive row, a single-row patch or removal on `specs/INDEX.md`, and/or an independent invocation of the affected writer skill(s) via the shared `findings:` interface — see Step 8 for which finding types get which.
**Does NOT**: run automatically, run as a blocking step inside any other skill's workflow, rewrite any document directly, write any `archive/INDEX.md` column other than `Status`, write to `specs/INDEX.md` beyond a single confirmed row's patch or removal, introduce any severity or status state beyond CRITICAL/WARNING/SUGGESTION and current/superseded, or reconcile a contradiction on its own judgment without a human confirming which side of it stands.

## Prerequisites

- OpenSpec CLI installed and initialized, with `accelint-qrspi-archive` already in regular use — this skill is a consumer of the indexes that skill produces, not a replacement for it.
- `openspec/changes/archive/INDEX.md` and `openspec/specs/INDEX.md` both exist and contain at least one row. See Verification Task B.
- Sub-agent support, for the same reason `accelint-qrspi-archive`'s Steps 2 and 5 require it: opening a candidate change's `design.md`, or a capability's `spec.md` for reconciliation, should return a structured extract to the parent, not the raw file contents. This skill's Step 3 and Step 4 both always delegate those targeted reads to subagents.
- Read access to every capability directory under `openspec/specs/` — plain file reads are sufficient, no OpenSpec CLI shellout needed, the same reasoning `accelint-qrspi-archive` already applies to its own local spec reads. Step 4 is the only step that needs this beyond the two index files.
- For routing to actually land anywhere beyond the report itself, the four writer skills' Mode 3 Refresh path needs to accept a `findings:` list (the same shared interface `accelint-qrspi-apply` Step 5 uses). If a targeted writer skill doesn't yet support this, this skill still produces the finding — it just can't hand it off automatically (see Error Handling).

## Build Order Context

This skill is deliberately the last of four pieces to exist, and each of the other three is a hard dependency, not a nice-to-have:

1. **`accelint-qrspi-archive`** has to already be in regular use. It's what produces both indexes this skill reads and the `related:`/frontmatter fields Steps 3, 4, and 5 depend on — without it, there is no corpus here at all.
2. **`accelint-qrspi-propose`'s Phase 2 extension** (reading `specs/INDEX.md` at propose time) needs to exist so that `specs/INDEX.md` is actually a load-bearing artifact in the workflow, not just a side effect of archiving — otherwise nothing downstream would notice or care if this skill's structural-coupling flags ever pointed at stale data.
3. **The shared `findings:` interface** — the Mode 3 Refresh extension across the four writer skills, paired with `accelint-qrspi-apply` Step 5's matching prompt change — has to land before this skill has anywhere to route a confirmed decision-drift or structural-coupling finding at all. Without it, Step 8 has a report and a human decision but no destination for those two finding types. Index reconciliation findings (Step 4) don't depend on this at all — they never route anywhere, confirmed or not, so that check works the same regardless of whether this interface exists yet.

The practical consequence: if any of these three aren't in place yet, this skill can still run Steps 1 through 7 (scan, detect, report) and produce a valid report, but Step 8 degrades to "tell the human what to do manually" for whichever half of the interface is missing, on decision-drift and structural-coupling findings only. It is never a reason to refuse the run outright.

## The Two Indexes This Skill Reads (Owned Elsewhere)

Neither index below is written by this skill in the general case. Both are written and maintained by `accelint-qrspi-archive`; this skill only ever reads them, with two narrow exceptions, both spelled out under Step 8: a `Status` column update on `archive/INDEX.md`, and a single-row patch or removal on `specs/INDEX.md`.

```
openspec/changes/archive/INDEX.md, one row per archived change:

| Change        | Date       | Decision                                               | Specs touched                      | Status  |
|---------------|------------|---------------------------------------------------------|-------------------------------------|---------|
| add-live-sync | 2026-03-02 | polling with 5s interval, no infra budget this quarter   | sync/protocol, ui/status-indicator  | current |

openspec/specs/INDEX.md, one row per capability, rebuilt on every archive:

| Capability    | Purpose                                                | Related              | Last touched by            |
|---------------|----------------------------------------------------------|------------------------|------------------------------|
| sync/protocol | Defines how client and server exchange live state       | ui/status-indicator   | add-live-sync (2026-03-02)  |
```

The `Decision` column is a condensed one-line summary of that change's `design.md` frontmatter (`choice` + `rationale`). This skill's Step 3 works off that summary first, cheaply, and only opens the full `design.md` — for its `alternatives:` field and any nuance the one-liner compresses away — for the specific candidates flagged as plausibly contradictory. This mirrors the same cost-control discipline `accelint-qrspi-archive` uses when it defers opening a change's folder until its own index flags it as relevant.

## The Log This Skill Owns

Neither index above records a synthesis checkpoint — that's expected, since both are owned entirely by `accelint-qrspi-archive` and neither has a reason to know this skill exists. So this skill maintains one small file of its own, `openspec/changes/archive/SYNTHESIS-LOG.md`, purely to answer two questions neither index can: "how many changes have archived since I last ran," and "has a human already looked at this specific decision-drift pair and judged it not real." It's a plain append-only list of one line per completed run, date plus the `archive/INDEX.md` row count checked through, plus an optional `dismissed:` sub-list of decision-drift pairs a human explicitly dismissed that run.

This file is not a column of either index and is never touched by `accelint-qrspi-archive` — it exists solely so **Step 2** and **Step 1, Task A** below can read it, and **Step 3** can filter against its accumulated `dismissed:` history. Step 9 is the only step that ever appends to it, and it only ever appends — a dismissal recorded on one run is never later removed by this skill itself; if a human wants to reconsider a dismissed pair, that's a manual edit to the log file, outside this skill's own write path. The exact line format, including the `dismissed:` sub-list, is shown where Step 9 writes it.

**Only decision-drift dismissals get this treatment — structural coupling dismissals don't, on purpose.** A decision-drift pair is anchored to two specific, immutable archived changes; a human's judgment that a specific pair isn't a real contradiction stays true forever, since the underlying `design.md` files never change. A structural coupling finding is a live snapshot of a `related:` count that moves every time `accelint-qrspi-archive` runs — permanently silencing "sync/protocol is over-coupled" would blind this skill to sync/protocol's count climbing further, which is exactly the trend this signal exists to catch. So structural coupling findings always resurface every run regardless of a prior dismissal; only decision-drift dismissals are ever written to the log.

## Findings Interface (Shared Contract, Not New)

Routing a confirmed finding to a writer skill uses the exact same `findings:` shape `accelint-qrspi-apply` Step 5 already uses — this skill is the interface's second caller, not a new one:

```text
Invoke the accelint-architecture-doc skill.

We found the following during periodic archive synthesis. Treat this as known
context and refresh the affected section(s).

findings:
- [Confirmed finding, rephrased as a plain factual statement, e.g., "add-live-sync
  (2026-03-02) chose polling for sync/protocol citing no infra budget for a
  message broker, but adopt-websocket-gateway (2026-09-14) later adopted a
  message broker for an unrelated capability — worth confirming the original
  budget constraint still holds before sync/protocol's spec is next touched"]
```

The writer skill merges this with its own codebase scan before presenting anything to the human — same Mode 3 Refresh path a manual run would take. Nothing about invoking it here is special-cased for this skill. This interface is used for decision-drift and structural-coupling findings only — index reconciliation findings (Step 4) never route through it, since a stale `specs/INDEX.md` row isn't a hub-doc content gap; see Step 8 for what happens to those instead.

**Rephrasing discipline.** Every line inside `findings:` is a plain factual statement about what the archive shows, never an instruction and never a conclusion the writer skill hasn't reached itself yet. "sync/protocol's stated budget constraint may no longer hold, given a later change's message-broker adoption" is correctly phrased; "update sync/protocol's spec to remove the budget constraint" is not — that second phrasing pre-empts the writer skill's own Mode 3 interview, which is exactly the judgment call this skill's Steps 7/8 split exists to keep with a human, not hand to a downstream skill as a foregone conclusion.

## Relationship to `openspec-verify-change`

This skill borrows `openspec-verify-change`'s CRITICAL/WARNING/SUGGESTION register deliberately, so a report from either reads as a familiar artifact — but the two check fundamentally different things. `openspec-verify-change` runs once, per change, before that change archives: forward-looking, scoped to whether one implementation matches its own `design.md` and `tasks.md`. This skill runs periodically, across the whole archive, after changes have already landed: backward-looking, scoped to whether the archive as a whole still agrees with itself. A change can pass `openspec-verify-change` cleanly the day it archives and still surface in a decision-drift finding two years later, once enough later changes touch related capabilities. The two are complementary, not redundant, and neither substitutes for the other.

## Workflow Overview

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Step             Action                                            Output    │
├───────────────────────────────────────────────────────────────────────────────┤
│  1 Preflight      Read SYNTHESIS-LOG.md, verify dependencies        Go / no-go│
│                   exist, sanity-check the two reasoned-default      + notes   │
│                   thresholds (Tasks A, B, C)                                  │
│  2 Scan indexes   Read archive/INDEX.md + specs/INDEX.md, load      In-memory │
│                   prior dismissed: pairs from the log               model     │
│  3 Decision drift Coarse-scan Decision column for same/related-     Candidate │
│                   capability collisions, skipping already-dismissed findings  │
│                   pairs; SUBAGENT opens design.md for the rest                │
│  4 Reconciliation Confirm every spec.md still exists; read Purpose  Candidate │
│                   + related: from each and diff against its         findings  │
│                   specs/INDEX.md row                                          │
│  5 Structural     Median related-count across specs/INDEX.md,       Candidate │
│    coupling       flag outliers ≥5 and ≥2× median                   findings  │
│  6 Compile report Assemble CRITICAL / WARNING / SUGGESTION          Draft     │
│                   findings, openspec-verify-change register         report    │
│  7 Human review   Present report; human confirms, dismisses, or     Confirmed │
│                   defers each finding                               findings  │
│  8 Route          Update Status, or patch/remove a specs/INDEX.md   Docs +    │
│                   row (confirmed findings only) + invoke affected   Status +  │
│                   writer skill(s) via findings:                     specs row │
│  9 Log + report   Append run checkpoint + any new dismissed:        Summary   │
│                   pairs to SYNTHESIS-LOG.md, summarize                        │
└───────────────────────────────────────────────────────────────────────────────┘

Step 3's design.md reads and Step 4's spec.md reads both always delegate to
a subagent, one per candidate, regardless of how many candidates surface. This
keeps raw design.md and spec.md contents out of the parent's context on every
run, the same discipline accelint-qrspi-archive applies to its own Step 2
and Step 5.
```

## Implementation Steps

Execute these steps in order without stopping between them unless an error occurs:

1. **Preflight — confirm this run has something to check and that its two reasoned-default thresholds still look reasonable, before reading anything else.**

   **Verification Task A — trigger cadence sanity-check.** Read `openspec/changes/archive/SYNTHESIS-LOG.md` (introduced above, under "The Log This Skill Owns") to find the last completed run's date and the archive row count it checked through. If the file doesn't exist yet, this is the first-ever run — skip the cadence math entirely rather than dividing by a history that doesn't exist yet, and note in the report that no prior checkpoint exists. Otherwise, take the `Date` column across every `archive/INDEX.md` row appended since that checkpoint and derive an average time-between-archives. The 15-archived-changes-since-last-run trigger is a reasoned starting point, not a measured one, so if the actual cadence implies 15 changes would mean checking twice a year or checking every few days, surface this as an informational note in the final report — never adjust the threshold automatically. Changing it is a decision for the human reading the report, not this skill. This task never blocks a run: if a human manually invokes this skill the day after the last run, with zero new rows since the checkpoint, proceed anyway — say so plainly ("0 changes since the last run, proceeding at your request"), since freshness is informational, not a gate.

**Verification Task B — dependency check.** Confirm both `openspec/changes/archive/INDEX.md` and `openspec/specs/INDEX.md` exist and contain at least one row each. If either is missing or empty, stop and report that `accelint-qrspi-archive` needs to run first — this skill has nothing to read yet, and guessing at index content would be worse than declining. If the archive has fewer than roughly 10 rows total, proceed only if the human explicitly wants a low-signal run anyway; note plainly in the report that a corpus this small has little for cross-archive synthesis to find, per the same reasoning that put this skill last in the build order.

**Verification Task C — structural coupling threshold sanity-check.** "At least 5 and at least double the index median" is the same kind of reasoned-not-measured default as Task A's trigger count. Compute the actual median `related:` count across every row in `specs/INDEX.md` and note, informationally only, whether the fixed floor of 5 or the 2× multiplier look like they'd flag either far too many capabilities or none at all against this project's real distribution. Same rule as Task A: report the observation, never silently change the threshold.

   If Tasks A and C surface nothing unusual, say so briefly and move on — these are sanity checks, not a mandatory finding every run.

2. **Scan Indexes — build an in-memory model of the archive without opening a single change folder yet.**

Read `archive/INDEX.md` in full: every row's `Change`, `Date`, `Decision` summary, `Specs touched` list, and current `Status`. Read `specs/INDEX.md` in full: every row's `Capability`, `Purpose`, `Related` list, and `Last touched by`/date. Both files stay cheap regardless of how large the archive has grown — that is the entire point of maintaining them — so this phase never needs to look past them.

   Also read every `dismissed:` sub-list across `SYNTHESIS-LOG.md`'s full history (not just the most recent run — a pair dismissed three runs ago still needs to stay suppressed) and build one flat set of dismissed-pair identities, each in the form `<change-A slug>|<change-B slug>|<capability>` with the two slugs alphabetically sorted so the same pair always produces the same identity regardless of which run or which order they were first compared in. If the log doesn't exist yet, this set starts empty — same first-run handling as Task A.

3. **Decision Drift Detection — find archived decisions that no longer cohere with each other, without opening every `design.md` in the corpus to do it.**

**Step 1 — group by shared or related capability.** Using `Specs touched` from `archive/INDEX.md` and `related:` from `specs/INDEX.md`, cluster archived changes that touched the same capability directly, or touched capabilities each other's `related:` lists connect.

**Step 2 — coarse scan.** Before comparing anything, drop any pair already present in Step 2's dismissed-pair set (loaded during the Scan Indexes step) — a human already looked at that exact pair and judged it not real, and that judgment doesn't expire. For everything else, within each cluster, compare `Decision` one-liners for signals of tension. A starter list of opposing-choice pairs worth pattern-matching on (extend it as a project's own vocabulary reveals its own oppositions — this isn't exhaustive):

- polling vs. push/websocket
- synchronous vs. asynchronous
- in-process vs. external service/broker
- monolith vs. microservice/split
- eager vs. lazy (loading, evaluation, initialization)
- centralized vs. distributed
- client-side vs. server-side (validation, rendering, state)

Beyond direct opposing pairs, also flag a stated rationale later contradicted by a rationale in a more recent change touching a related capability, and a capability with several changes clustered nearby in time while its own spec's `Last touched by` date sits conspicuously earlier. This step works entirely off the index text already in memory — no file I/O. A coarse-scan hit is cheap to be wrong about: it costs one subagent call in Step 3, not a bad finding in the final report, so this list is intentionally biased toward over-flagging rather than under-flagging.

**Step 3 — targeted verification.** For each candidate the coarse scan flags, spawn one subagent per candidate pair to open the full `design.md` for each change involved and confirm or dismiss the contradiction using the complete `choice`/`rationale`/`alternatives` fields, not just the index's compressed summary. For example, given these two frontmatter blocks:

```yaml
# openspec/changes/archive/2026-03-02-add-live-sync/design.md
---
change: add-live-sync
specs_touched: [sync/protocol, ui/status-indicator]
decisions:
  - id: D1
    choice: polling with 5s interval
    rationale: no infra budget for a message broker this quarter
    alternatives: [websocket push, long polling]
---
```

```yaml
# openspec/changes/archive/2026-06-18-adopt-notification-gateway/design.md
---
change: adopt-notification-gateway
specs_touched: [notifications/dispatch]
decisions:
  - id: D1
    choice: message broker (RabbitMQ)
    rationale: notification fan-out needed guaranteed delivery and retry
    alternatives: [polling, webhook callbacks]
---
```

the subagent reads both `choice`/`rationale` pairs directly and confirms a genuine contradiction candidate: `add-live-sync`'s stated constraint ("no infra budget for a message broker") is now in tension with a later change clearing exactly that obstacle for a different capability. Whether this actually rises to a finding, and at what severity, is settled by the rule below — not by this step alone. Return only a structured verdict (confirmed / dismissed, plus a supporting quote-free summary) to the parent — never the raw `design.md` contents.

**Step 4 — staleness flag.** Separately, flag any capability where `specs/INDEX.md`'s `Last touched by` date is old relative to a cluster of recent, related activity nearby (per Step 1's grouping) — this doesn't require opening any `design.md`, since it's a pure date comparison already available from the index data already loaded in Step 2.

   **Classification rule.** A confirmed contradiction is CRITICAL if the affected capability's `specs/INDEX.md` `Last touched by` date falls *after* the earlier of the two contradicting changes' dates — meaning something was built or touched on top of a decision that may no longer hold. Otherwise it's WARNING: the contradiction is real, but nothing has actively depended on the resolved version since. Both halves of this comparison come straight from the index model Step 2 already built, so the rule needs no new lookup and produces the same classification on a re-run given the same data. Staleness flags (Step 4) are always SUGGESTION-level, since they're a signal to look, not a confirmed contradiction.

4. **Index Reconciliation — check whether `specs/INDEX.md` still matches the actual `spec.md` files it claims to summarize — the one thing nothing else in this pipeline verifies. `accelint-qrspi-archive`'s Step 6 patches only the rows for capabilities the current batch's changes declared in `specs_touched`, and only performs a full corpus-wide scan once, at bootstrap, when the index doesn't exist yet. Every archive after that leaves every untouched row exactly as it was, indefinitely — a `spec.md` hand-edited outside the archive workflow, or a capability directory renamed or deleted directly, has no mechanism anywhere in this stack that would ever notice unless that specific capability happens to be touched by some future change. `accelint-qrspi-archive`'s own SKILL.md names this gap explicitly and names this skill as the natural place to close it, since periodic, corpus-wide checking is exactly this skill's charter.**

**Step 1 — existence check (every row, no content read).** For every row in `specs/INDEX.md`, confirm `openspec/specs/<capability>/spec.md` still exists on disk. This is a file-existence check, not a content read, so it costs nothing meaningful even against a large corpus. A missing file or directory is an immediate CRITICAL finding — every other step in this workflow that touches this row (Step 3's clustering, Step 5's median) is working from a reference that no longer resolves to anything.

**Step 2 — content check (every row whose file exists).** Read just the top of each `spec.md` — its `## Purpose` heading body and `related:` frontmatter list, not the full spec body — and compare against that row's `Purpose` and `Related` columns. A mismatch on either is a WARNING finding: "specs/INDEX.md row for `<capability>` disagrees with its own spec.md — index says `<X>`, file currently says `<Y>`." This is a small, bounded read (frontmatter plus one heading, the same shape of read Step 3's detailed verification already does against `design.md`), not a full-corpus content scan — it stays proportionate to corpus size the same way Step 5's median calculation does, just with a per-row cost instead of a zero cost.

   **What this step does not do.** It never writes anything itself — Step 4 is detection only. It never routes a confirmed finding to a writer skill either, since this isn't a hub-doc content gap — it's the index itself being wrong. What happens after a human confirms a reconciliation finding is Step 8's job, not this one; see Step 8 for the narrow, confirmation-gated write permission this skill has on `specs/INDEX.md` for exactly this case.

5. **Structural Coupling Signal — surface capabilities whose `related:` count suggests they may have outgrown their own boundary — at zero extra cost, since the counts already exist in `specs/INDEX.md` for other reasons.**

Compute the median `related:` list length across every row loaded in Step 2. Flag any capability whose count is both at least 5 and at least double that median as a SUGGESTION-level finding, phrased as a plain fact: for example, "sync/protocol relates to 14 other capabilities, more than double the index median of 6." This is a second reading of data the pipeline was already maintaining, not new bookkeeping, and it never requires opening any `design.md`.

   Worked example: across 22 capability rows, related-counts of `[1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8, 8, 9, 10, 11, 14, 14]` sort to a median of 6 (the 11th and 12th of 22 values, both 6). The floor is `max(5, 2 × 6) = 12`, so only the two rows at 14 clear it — everything from 11 down, including the two rows already at 6, stays unflagged. This is exactly the kind of distribution Verification Task C checks against: if every project's median clustered near 1 or 2 instead, the fixed floor of 5 alone would already flag most of the corpus regardless of the 2× multiplier, which is precisely the mismatch Task C exists to surface.

6. **Compile Report — assemble everything Steps 3, 4, and 5 found into one report, in the same CRITICAL / WARNING / SUGGESTION register `openspec-verify-change` already uses, so it reads as a familiar artifact rather than a new report format to learn.**

```text
## Archive Synthesis Report — <date>

Corpus: <N> archived changes, <M> capabilities, checked back to <last synthesis
checkpoint or "project start">.

### CRITICAL
- [Confirmed decision contradiction with a live, actively-touched capability]
- [Index reconciliation: a specs/INDEX.md row's capability directory or
  spec.md no longer exists]

### WARNING
- [Confirmed decision contradiction on a dormant capability]
- [Index reconciliation: a specs/INDEX.md row's Purpose or related:
  disagrees with its own spec.md]

### SUGGESTION
- [Staleness flag]
- [Structural coupling flag]

### Threshold notes (informational only, Tasks A & C)
- [Any cadence or median mismatch worth a human's attention]
```

   Never present a finding here as already-resolved — every CRITICAL/WARNING item is a candidate for Step 7, not a conclusion.

7. **Human Review — let a human decide what actually happens with each finding — this skill never resolves a contradiction on its own authority.**

Present each finding individually, in severity order. The three options are always Confirm / Dismiss / Defer, but "Confirm" and "Dismiss" don't do the same thing for a decision-drift finding as they do for a structural coupling or index reconciliation finding, and the label has to say so — a person choosing between them shouldn't have to already know this skill's internals to know what they're picking:

```
Finding 1 [CRITICAL]: add-live-sync's stated budget constraint for
sync/protocol may no longer hold, given adopt-notification-gateway's
later message-broker adoption.
  (a) Confirm — I'll ask which change stands, then update Status and
      notify the relevant doc skill(s)
  (b) Dismiss — Recorded permanently; this exact pair won't be
      flagged again
  (c) Defer  — Left as-is; resurfaces next run

Finding 2 [SUGGESTION]: sync/protocol relates to 14 capabilities,
over double the index median of 6.
  (a) Confirm — Routes to ARCHITECTURE.md's Known Technical Debt review
  (b) Dismiss — Not persisted; will still be re-checked and may
      resurface next run if still elevated
  (c) Defer  — Left as-is; resurfaces next run

Finding 3 [CRITICAL]: specs/INDEX.md row for cache/layer points at
openspec/specs/cache/layer/spec.md, which no longer exists.
  (a) Confirm — I'll remove this row from specs/INDEX.md; if this
      was a rename, the new capability gets its own row automatically
  (b) Dismiss — Not persisted; will still be re-checked and may
      resurface next run if still unresolved
  (c) Defer  — Left as-is; resurfaces next run
```

   Only confirmed findings proceed to Step 8, and for a decision-drift finding, "Confirm" is the start of a decision, not the end of one — it only tells this skill the contradiction is real; Step 8 still has to ask which side of it stands before anything gets written (see Step 8 and Error Handling). Defer never writes anything — a deferred finding resurfaces on the next run exactly as before, since nothing about the underlying index data changed to stop Step 3, Step 4, or Step 5 from re-detecting the same pattern. Dismiss behaves differently depending on the finding type, which is exactly why its label above isn't the same across all three: dismissing a **decision-drift finding** persists — Step 9 records that specific pair's identity to `SYNTHESIS-LOG.md`, and Step 3 will skip it on every future run. Dismissing a **structural coupling** or **index reconciliation finding** does not persist — either resurfaces next run like a defer would, because both are live snapshots of current state (a `related:` count, or whether a `spec.md` still matches its index row) rather than fixed historical facts (see "The Log This Skill Owns" for the full reasoning).

   If the human stops reviewing partway through the list — ends the session, or moves on without responding to every finding — treat every unaddressed finding as deferred by default, never as confirmed. Step 9 still logs the run and reports what was confirmed so far; whatever wasn't reached simply resurfaces next time, same as an explicit defer.

8. **Route Confirmed Findings — hand off confirmed findings to wherever they can actually change something, using the shared `findings:` interface, and, for the narrow set of writes this skill is ever allowed to make, make them.**

**For a confirmed decision contradiction**: confirming doesn't specify which side of the contradiction stands, so ask that directly first — never infer it from recency alone, even though "the later change" is often the reasonable guess (see Error Handling for why a wrong guess here is worse than a wrong guess almost anywhere else in this skill). Once the human names it, update that row's `Status` column in `archive/INDEX.md` to `superseded by <slug> (<date>)`, where `<slug>` and `<date>` identify the change that stands. This is the only write this skill ever makes to that file, and it only happens after both the initial confirmation and this follow-up answer — never automatically, never speculatively, never guessed. Then invoke the writer skill(s) whose hub doc covers the affected capability, using the Findings Interface format above.

**Which writer skill a finding targets** follows the same purpose split `accelint-qrspi-apply` Step 5 already uses to decide between the four hub docs — a decision-drift finding rarely belongs to exactly one, so route to whichever actually covers what the contradiction is about:

- A contradiction over **tech stack, dependencies, or coding/architecture patterns** → `accelint-onboard-openspec` (`openspec/config.yaml`).
- A contradiction over **system structure, components, or data flow** → `accelint-architecture-doc` (`ARCHITECTURE.md`). This is also always the target for structural coupling findings, landing in that skill's existing Known Technical Debt interview slot.
- A contradiction over **agent workflow or behavior** → `accelint-onboard-agents` (`AGENTS.md`).
- A contradiction over **user-facing setup or usage** → `accelint-readme-writer` (`README.md`).

A single finding can legitimately target more than one — invoke each relevant writer skill separately, with the same finding rephrased once per invocation to fit that doc's own focus, exactly as `accelint-qrspi-apply` Step 5 already treats each hub doc as an independent target rather than a single combined update. Each invocation succeeds or fails on its own — one writer skill being unavailable or erroring never blocks or rolls back a separate, successful invocation of another (see Error Handling for the specific case of a routing failure after `Status` has already been written).

**For a confirmed staleness flag or structural coupling flag**: no `Status` update applies — these aren't contradictions between two specific rows, so there is nothing to mark superseded. Route the finding to `accelint-architecture-doc`'s existing Known Technical Debt interview slot via the same `findings:` interface.

   **For a confirmed index reconciliation finding — content mismatch (WARNING)**: unlike a decision-drift finding, this needs no disambiguating question — `spec.md` is the source of truth by construction, so once a human confirms the discrepancy is real, the correct value isn't a judgment call. Patch that single row in `specs/INDEX.md`: locate the line whose first cell exactly matches the capability name — anchored between the leading `| ` and the next `|`, the same precise match `accelint-qrspi-archive`'s own Step 6 uses, so `cache/layer` never matches `cache/layer-v2` — and replace only the `Purpose` and `related:` cells with `spec.md`'s current values. Leave `last_touched_by` exactly as it reads. That field records which *archived change* last touched this capability, and a reconciliation patch isn't an archived change — overwriting it would misattribute a hand-edit fix to a change that never happened. Build the replacement row with `accelint-qrspi-archive`'s own formatting rules: single-space cell separation, no cross-row padding, every other row in the file untouched. Report the before/after diff once written.

   **For a confirmed index reconciliation finding — missing directory or file (CRITICAL)**: also unambiguous once confirmed — the row points at something that no longer exists, so the correct action is removing that row, regardless of whether the capability was renamed or genuinely retired. Locate the line by the same anchored match and delete it; every other row stays untouched. If it turns out this was a rename rather than a removal, this skill doesn't attempt to guess the new name or insert a row for it — Step 4 never verified that new capability's content, so writing a row for it here would be a guess dressed up as a finding. The new capability picks up its own row the ordinary way, the next time `accelint-qrspi-archive` archives a change that touches it.

   **This skill's write permission on `specs/INDEX.md`** is exactly these two operations — patch or delete a single row — and only ever fires after Step 7's explicit human confirmation of that specific discrepancy. It reuses `accelint-qrspi-archive`'s own row-patch mechanics rather than inventing separate logic that could drift from it over time; the two skills write the same file the same way, they just fire from different triggers.

   **For a dismissed decision-drift finding**: no `Status` write, but Step 9 does record the pair's identity to `SYNTHESIS-LOG.md`'s `dismissed:` sub-list, so Step 3 skips it on every future run. This is the one case where a dismissal actually changes what happens next time.

   **For a dismissed structural coupling or index reconciliation finding, or any deferred finding**: no write anywhere. All resurface identically on the next synthesis run — a deferred finding because nothing about the underlying index changed, a dismissed coupling or reconciliation finding because both are live snapshots that deserve re-checking every run regardless of a prior dismissal (see "The Log This Skill Owns").

9. **Log and Report — leave a checkpoint for Task A's cadence math next time, persist any newly dismissed decision-drift pairs, and summarize the run.**

Append one line to `openspec/changes/archive/SYNTHESIS-LOG.md` (created fresh on first run) recording the date and the `archive/INDEX.md` row count this run checked through, followed by an indented `dismissed:` sub-list if any decision-drift finding was dismissed this run (omit the sub-list entirely if none were):

```
2026-07-06 — checked through row 42 — 2 confirmed, 1 dismissed, 1 deferred
  dismissed: [add-live-sync|adopt-notification-gateway|sync/protocol]
```

   This log is a new, standalone file this skill owns entirely — it is not a column of either index, so writing it never conflicts with the single-write-permission rule on `archive/INDEX.md`. It exists purely so Step 1's next run can compute "changes since last run" without guessing, and so Step 3 can skip pairs a human has already ruled out, since neither index records either of those things on its own. Every run only ever appends a new line — an existing `dismissed:` entry is never edited or removed by this skill; a human wanting to reconsider a dismissed pair does so by editing the log file directly, not through this skill.

   Close with a short summary: how many findings of each type, how many confirmed/dismissed/deferred, and which writer skill(s) were invoked as a result.

## Explicitly Out of Scope

- **No automatic doc rewriting, under any circumstance.** This skill produces a report and, on confirmation, a `findings:` handoff — it never edits a hub doc directly itself.
- **No write to any `archive/INDEX.md` column except `Status`.** Every other column belongs to `accelint-qrspi-archive`, permanently, including on rows this skill's `Status` update touches.
- **No third severity or status state.** Findings stay CRITICAL/WARNING/SUGGESTION; `Status` stays a two-state field, `current` or `superseded by <slug> (<date>)`.
- **No automatic threshold adjustment.** Verification Tasks A and C report mismatches; they never change the 15-change trigger or the 5-and-2×-median coupling floor on their own.
- **No running on its own initiative.** Always either a direct human invocation or an offered suggestion from `accelint-qrspi-archive` that the human separately accepts.
- **No cross-repository synthesis.** This skill operates only on the local project's `openspec/changes/archive/` and `openspec/specs/`. OpenSpec's separate stores feature, for cross-repo spec references, is untouched by anything here — extending synthesis across repositories is a different, larger problem this skill doesn't attempt.
- **No writes to any `design.md`, ever.** Step 3 opens archived `design.md` files strictly to read `choice`/`rationale`/`alternatives` for verification — never to annotate, correct, or append anything back to them. An archived change's own record of its own reasoning stays exactly as it was written, even after a later synthesis run confirms it's now superseded.
- **No writes to `specs/INDEX.md` beyond a single confirmed row's patch or removal.** This mirrors the `archive/INDEX.md` rule exactly: one narrow, confirmation-gated exception, using `accelint-qrspi-archive`'s own row-format logic rather than separate logic that could drift from it. No bulk edits, no full-file rewrites, no speculative inserts for a renamed capability this skill never verified.
- **No writes to any `spec.md`, ever.** Step 4 reads `## Purpose` and `related:` to compare against the index — it never corrects, annotates, or touches the file it's checking.
- **No full-body reads of `spec.md` during reconciliation.** Step 4 reads only the `## Purpose` heading and `related:` frontmatter — the same bounded, top-of-file read Step 5's own source data already assumes, not a full spec review.

## Error Handling

**Either index missing or empty (Task B)**: stop before Step 2; tell the user to run `accelint-qrspi-archive` first.

**`SYNTHESIS-LOG.md` doesn't exist yet**: not an error, and not the same condition as the one above — this is the expected state on this skill's first-ever run. Task A skips its cadence math and proceeds; Step 9 creates the file fresh.

**Corpus smaller than ~10 archived changes**: don't block, but say plainly that a corpus this size has little for cross-archive synthesis to find, and ask before proceeding with a low-signal run.

**A flagged writer skill isn't installed, or doesn't yet support `findings:` in its Mode 3 path**: don't fail the whole run. Still produce and present the finding in the report; for Step 8 routing, tell the user this specific handoff needs to happen manually and summarize what the finding was so they can paste it in themselves.

**No subagent support available**: fall back to opening flagged `design.md` candidates directly in the parent context for Step 3 Step 3. Warn the user explicitly that this run's raw design.md contents will sit in context as a result — a degraded fallback, not the default.

**A `design.md` referenced by an index row no longer exists** (moved, renamed, or the archive folder was otherwise disturbed outside this skill's own writes): skip that row for Step 3's targeted verification, note it in the report as unverifiable, and do not treat its absence as itself a finding.

**A row in either index is malformed** (a `Specs touched` or `Related` list that fails to parse, a missing `Date`, or similar): skip that single row for whatever phase needs the missing field, note it plainly in the report as unparseable, and continue with every other row. One bad row is a data-quality note for the human, not a reason to abandon the run.

**A `dismissed:` entry in `SYNTHESIS-LOG.md` references a slug that no longer appears in `archive/INDEX.md`** (the log was hand-edited, or the archive was altered outside this skill's own flow): drop that one identity from the in-memory dismissed-pair set for this run and note it once in the report — it can't suppress anything if one of its two slugs no longer resolves to a real row, and guessing at what it originally meant would be worse than treating it as inert.

**Fewer than 2 rows in `specs/INDEX.md`**: skip Step 5 entirely — a median needs enough rows to mean anything, and this mirrors the same low-corpus reasoning as the archive-size check above.

**Step 3 Step 1 clustering produces an unreasonably large candidate set** (a capability with a very long `related:` list, or a corpus with many changes touching it): don't spawn one subagent per pair unconditionally. Prioritize the most recently archived pairs first, verify those, and note in the report how many older candidates in the same cluster weren't checked this run due to volume — they remain candidates and will resurface next run, same as any other unconfirmed finding. This is a volume cap for cost control, not a correctness shortcut: nothing here is dismissed on the skill's own authority.

**A confirmed finding's routing invocation to a writer skill fails or times out**: this doesn't undo a `Status` update already made for that same finding — the two writes are independent, and `Status` reflects the human's confirmation, not whether the handoff succeeded. Tell the user plainly that the `Status` update landed but the writer-skill handoff didn't, and give them the same `findings:`-formatted text so they can invoke it manually.

**The human answers Step 8's "which change stands" follow-up ambiguously, or doesn't answer at all**: never infer it from recency alone, even though "the later change" is often the reasonable guess. Ask again rather than proceeding — a wrong guess here writes a permanent, human-facing claim into an audit-trail file, which is exactly the kind of write this skill's single-write-permission rule exists to keep deliberate. Leave the finding unresolved (equivalent to deferred) until the answer is unambiguous.

**A human names a slug for `Status`'s `superseded by` value that doesn't actually appear in `archive/INDEX.md`**: stop and ask for the correct slug rather than writing an unverifiable reference — this field's entire value depends on it always resolving to a real row.

**A `spec.md` exists but has no `## Purpose` heading** (`accelint-qrspi-archive`'s own Prerequisites require this heading before it will patch a row for that capability, but a hand-edit could still have removed it after the fact): treat this the same as a content mismatch — a WARNING finding noting the heading is missing entirely, not a CRITICAL one, since the directory and file both still resolve to something real.

**The corpus has far more capabilities than is reasonable to content-check in one run**: prioritize capabilities whose `Last touched by` change is oldest relative to the archive's own history first — those are the rows that have gone longest without any patch at all, and so carry the highest risk of undetected drift. Note in the report how many capabilities' content checks were skipped this run due to volume; the existence check in Step 1 still runs against every row regardless, since that check is nearly free.

**A confirmed reconciliation finding's target row changed between Step 4's detection and Step 8's write** (a rare race — `accelint-qrspi-archive` ran in between, or a human hand-edited the row during the review session): re-check the row immediately before writing. If it already matches `spec.md` (something else already fixed it), skip the write and report it as resolved rather than confirmed-and-patched. If it still needs the same fix, proceed. Never write based on what Step 4 saw if that's no longer what's actually there.

**The `specs/INDEX.md` patch or removal write itself fails**: report it plainly, the same way a failed writer-skill handoff is reported — this finding stays unresolved (equivalent to deferred) and resurfaces next run, since nothing was actually written.

## NEVER Do This

**NEVER run without an explicit human invocation or accepted suggestion** — this skill has no automatic trigger of its own; `accelint-qrspi-archive` only ever suggests, it never forces a run.

**NEVER write any `archive/INDEX.md` column other than `Status`** — every other field is `accelint-qrspi-archive`'s, permanently, on every row this skill ever touches.

**NEVER introduce a third state to `Status`** — it is always `current` or `superseded by <slug> (<date>)`, never anything else.

**NEVER update `Status` without an explicit human confirmation of that specific contradiction** — a candidate surfacing in Step 3 is not the same thing as a human agreeing it's real.

**NEVER rewrite a hub doc directly** — always route a confirmed finding through the relevant writer skill's own Mode 3 Refresh path via the `findings:` interface, exactly like `accelint-qrspi-apply` Step 5 already does.

**NEVER open every `design.md` in the corpus wholesale** — Step 3 only opens the specific candidates the cheap index-only scan in Step 2 flagged, one subagent per candidate.

**NEVER silently adjust the 15-change trigger or the 5-and-2×-median coupling floor** — Tasks A and C only report a mismatch; changing either number is a human's call.

**NEVER treat a missing or moved `design.md` as itself a finding** — it just means that row can't be verified this run; note it and move on.

**NEVER tell a human a dismissed structural coupling finding is permanently suppressed** — only decision-drift dismissals persist to `SYNTHESIS-LOG.md`; a dismissed coupling finding resurfaces next run exactly like a deferred one, since its underlying count is a moving snapshot. Say this plainly rather than implying a guarantee this skill doesn't keep.

**NEVER let this skill itself edit or remove an existing `dismissed:` entry** — Step 9 only ever appends. Reconsidering a previously dismissed pair is a manual edit to `SYNTHESIS-LOG.md`, deliberately outside this skill's own write path.

**NEVER roll back a `Status` update because a routing invocation afterward failed** — the two writes are independent. A confirmed finding's `Status` change reflects the human's confirmation, not whether the writer-skill handoff succeeded; a failed handoff gets reported and handed to the human manually, it never reverses a write that already landed.

**NEVER write to `specs/INDEX.md` except a single confirmed row's patch or removal** — same discipline as the `Status` exception on `archive/INDEX.md`: one narrow, confirmation-gated write, never a bulk edit or full-file rewrite.

**NEVER touch `last_touched_by` when patching a reconciliation finding** — that field records which archived change last touched the capability; a reconciliation patch isn't an archived change, and overwriting it would misattribute a hand-edit fix to a change that never happened.

**NEVER guess a renamed capability's new name or insert a speculative row for it** — a missing-file CRITICAL finding only ever removes the stale row. Step 4 never verified the new capability's content, so writing a row for it would be a guess dressed up as a finding.

**NEVER re-pad or realign existing rows in `specs/INDEX.md` when patching or removing one row** — same rule `accelint-qrspi-archive` follows for its own row-level writes. Cell padding is per-row, not aligned to the table's widest value; touching every row's whitespace to keep columns visually lined up turns a one-line diff back into a full-file rewrite.

**NEVER tell a human a dismissed index reconciliation finding is permanently suppressed** — same rule as structural coupling, and for the same reason: the comparison is against live file state, not a fixed historical fact, so it's re-checked every run regardless of a prior dismissal.

**NEVER treat a missing `## Purpose` heading in an otherwise-existing `spec.md` as a directory-level CRITICAL** — the file and directory both resolve to something real; that's a content-level WARNING, same bucket as a `Purpose`/`related:` mismatch.

## Terminology

This skill uses several terms precisely and doesn't mix them — worth pinning down once rather than re-explaining in every phase:

- **Candidate**: a possible contradiction, drift, or coupling signal the coarse scan (Step 3 Step 2), the existence/content check (Step 4), or the median check (Step 5) has flagged, before any verification has happened. Not yet a finding.
- **Confirmed**: a candidate that Step 3 Step 3's targeted subagent verified against full `design.md` content, a Step 4 discrepancy that simply is what the direct comparison against `spec.md` shows (no separate verification step needed, since it's already a direct read), or a Step 5 structural signal that simply is what the index says it is (same reasoning).
- **Finding**: a confirmed candidate, phrased as a plain fact, ready for Step 5's report and Step 6's human review. Only findings appear in the report — raw candidates that Step 3 dismissed never do.
- **Confirmed (human)**: distinct from the verification-step "confirmed" above — this is the human's Step 6 decision that a given finding warrants action. Context disambiguates which sense is meant; where it doesn't, this document says "human-confirmed" explicitly.
- **Dismissed**: a Step 6 human decision that a finding isn't real or doesn't need action. Persists for decision-drift findings (the pair is logged and never re-flagged); does not persist for structural coupling or index reconciliation findings (both are re-checked every run regardless, since both read a live, moving snapshot of current state rather than a fixed historical fact). See Step 6 and "The Log This Skill Owns" for why they differ.
- **Deferred**: a Step 6 human decision that a finding is real but not ready to act on. Never persists, for any finding type — a deferred finding resurfaces next run exactly as before.
- **`Status` = `current`**: the default state `accelint-qrspi-archive` writes for every row — not an assertion that the row is definitely correct, only that no synthesis run has yet confirmed a contradiction affecting it.
- **`Status` = `superseded by <slug> (<date>)`**: the only other state this field ever holds, written exclusively by this skill's Step 8, exclusively after a human-confirmed decision contradiction. Index reconciliation findings never produce a `Status` write — see Step 8.
- **`specs/INDEX.md` row patch or removal**: this skill's other write permission, exclusively on Step 8, exclusively after a human-confirmed index reconciliation finding. A patch touches only `Purpose` and `related:`; a removal deletes the whole row. Neither ever touches `last_touched_by`, and neither is a `Status`-style state — the row is either present and current, or it's gone.

## Example Usage

**Scenario: suggested run, one confirmed contradiction, one structural flag**

```
[accelint-qrspi-archive, at the end of its own summary output]
ℹ 15 changes have archived since the last synthesis run (2026-01-10).
  Consider running accelint-archive-synthesis.

User: Yes, run archive synthesis.

Skill: Preflight —
✓ Task B: both indexes present, 47 archived changes, 22 capabilities
✓ Task A: actual cadence ~1.1 changes/week; 15-change trigger implies
  checking roughly every 10 weeks — no mismatch worth flagging
✓ Task C: index median related-count is 6; 5-and-2× floor looks reasonable
  against this distribution

Scanning archive/INDEX.md and specs/INDEX.md...

Decision drift —
[spawns subagent: verify sync/protocol candidate]
✓ Confirmed: add-live-sync (2026-03-02) chose polling for sync/protocol,
  citing no infra budget for a message broker. adopt-notification-gateway
  (2026-06-18) later adopted a message broker for an unrelated capability.
  sync/protocol has been touched twice since — CRITICAL.

Index reconciliation —
✓ Existence check: 22/22 capability directories present.
[spawns subagent: content-check cache/layer]
✓ Confirmed: cache/layer's specs/INDEX.md row lists related: [cli-core],
  but cache/layer/spec.md's actual related: frontmatter currently reads
  [cli-core, rule-engine] — added by a hand-edit, no archived change
  touched this capability since — WARNING.

Structural coupling —
✓ sync/protocol relates to 14 other capabilities, more than double the
  index median of 6 — SUGGESTION.

## Archive Synthesis Report — 2026-07-06
Corpus: 47 archived changes, 22 capabilities, checked back to 2026-01-10.

### CRITICAL
Finding 1: add-live-sync's stated budget constraint for sync/protocol may
no longer hold, given adopt-notification-gateway's later message-broker
adoption.
  (a) Confirm — I'll ask which change stands, then update Status and
      notify the relevant doc skill(s)
  (b) Dismiss — Recorded permanently; this exact pair won't be flagged again
  (c) Defer  — Left as-is; resurfaces next run

### WARNING
Finding 2: cache/layer's specs/INDEX.md row disagrees with its own
spec.md — index says related: [cli-core], file currently says
related: [cli-core, rule-engine].
  (a) Confirm — I'll patch this row directly (Purpose + related:
      only, last_touched_by stays as-is)
  (b) Dismiss — Not persisted; will still be re-checked and may
      resurface next run if still unresolved
  (c) Defer  — Left as-is; resurfaces next run

### SUGGESTION
Finding 3: sync/protocol relates to 14 capabilities, over double the
median of 6.
  (a) Confirm — Routes to ARCHITECTURE.md's Known Technical Debt review
  (b) Dismiss — Not persisted; will still be re-checked and may
      resurface next run if still elevated
  (c) Defer  — Left as-is; resurfaces next run

User: Confirm all three findings.

Skill: For Finding 1 — which change should Status reflect as the one
that stands: add-live-sync's original budget constraint, or
adopt-notification-gateway's later message-broker adoption?

User: adopt-notification-gateway — the budget constraint's gone now.

Skill:
✓ archive/INDEX.md: add-live-sync row Status → "superseded by
  adopt-notification-gateway (2026-06-18)"

Invoke the accelint-architecture-doc skill.

We found the following during periodic archive synthesis. Treat this as known
context and refresh the affected section(s).

findings:
- sync/protocol budget constraint may be stale

✓ Finding 2 confirmed.
✓ specs/INDEX.md: cache/layer row patched — related: [cli-core] →
  [cli-core, rule-engine] (Purpose unchanged, last_touched_by left
  exactly as it was — this patch isn't an archived change, so
  attribution doesn't move)
✓ Finding 3 confirmed.

Invoke the accelint-architecture-doc skill.

We found the following during periodic archive synthesis. Treat this as known
context and refresh the affected section(s).

findings:
- sync/protocol structural coupling, routed to Known Technical Debt review

Appending checkpoint to openspec/changes/archive/SYNTHESIS-LOG.md...

✅ Synthesis complete: 3 confirmed, 0 dismissed, 0 deferred.
```

**Scenario: first-ever run, small corpus, nothing to report**

```
User: Run archive synthesis on this repo, I don't think it's ever been done.

Skill: Preflight —
✓ Task B: both indexes present, 6 archived changes, 4 capabilities
ℹ openspec/changes/archive/SYNTHESIS-LOG.md doesn't exist yet — this is the
  first-ever run. Task A's cadence math needs a prior checkpoint, so it's
  skipped this time rather than computed against nothing.
⚠ 6 archived changes is a small corpus — cross-archive synthesis has little
  to work with yet. Continue anyway with a low-signal run?

User: Yes, go ahead.

Skill: Scanning archive/INDEX.md and specs/INDEX.md...

Decision drift — no candidate collisions found across 4 capabilities.
Index reconciliation — 4/4 directories present; all 4 spec.md files match
  their specs/INDEX.md rows.
Structural coupling — only 4 specs/INDEX.md rows; Step 5 needs at least 2
  to compute a median, but a corpus this small has nothing meaningful to
  flag either way.

## Archive Synthesis Report — 2026-07-06
Corpus: 6 archived changes, 4 capabilities, checked back to project start.

No CRITICAL, WARNING, or SUGGESTION findings this run.

Appending checkpoint to openspec/changes/archive/SYNTHESIS-LOG.md
  (file created fresh)...

✅ Synthesis complete: nothing to confirm. Re-run once more changes have
   archived — this corpus is too small yet for the signal to be meaningful.
```

**Scenario: a previously dismissed pair stays suppressed on the next run**

```
[Run 1, three months earlier]
Skill: Finding 1 [WARNING]: legacy-cache-warmer (2025-11-02) chose eager
  cache warming for cache/layer, citing predictable traffic patterns.
  adopt-lazy-init (2026-01-14) later chose lazy initialization for an
  unrelated capability.
  (a) Confirm — I'll ask which change stands, then update Status and
      notify the relevant doc skill(s)
  (b) Dismiss — Recorded permanently; this exact pair won't be
      flagged again
  (c) Defer  — Left as-is; resurfaces next run

User: Dismiss — these two were never actually in tension, different
teams, different constraints.

Skill: ✓ Recorded as dismissed.
Appending checkpoint to openspec/changes/archive/SYNTHESIS-LOG.md...
  dismissed: [adopt-lazy-init|legacy-cache-warmer|cache/layer]

[Run 2, today]
Skill: Preflight —
✓ Task A: reading SYNTHESIS-LOG.md — last run 2026-04-02, checked
  through row 31; 1 dismissed pair on record
✓ Task B: both indexes present, 53 archived changes, 24 capabilities

Scanning archive/INDEX.md and specs/INDEX.md...
Loading dismissed-pair history — 1 entry found.

Decision drift —
- legacy-cache-warmer / adopt-lazy-init / cache/layer: matches a
  dismissed pair on record, skipped without re-verification.
- [new candidates, if any, proceed through Steps 2-4 as normal]

## Archive Synthesis Report — 2026-07-06
Corpus: 53 archived changes, 24 capabilities, checked back to 2026-04-02.
(cache/layer's legacy-cache-warmer/adopt-lazy-init pair previously
dismissed — not re-surfaced this run)

No new CRITICAL or WARNING findings.
```
