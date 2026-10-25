---
name: audit-cuj
description: Verify a stored critical user journey by replaying it step by step against the running app, and report the exact step that broke as a cuj report in .ux/audits. Use for "verify my CUJs", "do the journeys still work", "journey regression check", "which step broke".
---

# Audit CUJ — replay a journey and report the step that broke

Replays the critical user journeys stored in the host's `.ux/cujs/` against the running app
and reports the exact step that broke, as an `auditor: cuj` report under `.ux/audits/`.

Adopt the [`cuj-auditor`](../../agents/cuj-auditor.md) persona: you hold **no heuristics**
and offer no opinions about the design. The journey file is the entire rubric. The
[CUJ file contract](../spec-cuj/references/cuj-contract.md) defines it; the
[report contract](../usability-audit/references/report-contract.md) defines your output.

**Evaluation modes:** prefer **live**. In **static** mode you can only trace the route,
handler, or component behind each step and assess whether `expect` is plausible — every such
finding is labelled `potential — unverified`, and **a static run cannot produce a verified
pass**. **hybrid** is live where reachable, static elsewhere, reported per step. Mode is
auto-selected by default; `--mode` forces one. Record the mode you **actually** used, not the
one requested.

> **The failure mode this skill exists to prevent is itself.** For every other auditor an
> empty report means "I looked and found nothing". For you, **`total: 0` is the SUCCESS
> state** — and it is also, byte for byte, what a run that verified nothing produces. The
> report schema cannot tell those apart. Nothing downstream can either. The counts you write
> in step 7 are the only thing standing between a clean pass and a lie.

---

## Inputs

`$ARGUMENTS`:

- **`target`** — a URL or host repo path. Defaults to the current repo, auto-detecting the
  dev server.
- **`--cuj <id|all|critical>`** — which journeys to select. `all` (default), a single `CUJ-003`,
  or `critical` for every journey whose `criticality` is `critical`.
- **`--mode static|live|hybrid`** — force an evaluation mode.

## Workflow

### 1. Snapshot the repo, then select the journeys — and stop if there are none

**Before you write anything**, record what was already dirty:

```
python3 scripts/audit_safety.py <host-repo> --snapshot > /tmp/ux-baseline.json
```

Git can tell you the tree differs from HEAD; it cannot tell you *who* made it differ. You
are most often run on a repo that is dirty **before you start** — "did my refactor break a
journey?" means the refactor is uncommitted, by definition. Without this snapshot, step 8
reports the user's own work as your violation, every run. A check that cries wolf gets muted,
and a muted check is a deleted one.

Then read `.ux/cujs/` in the host repo and apply `--cuj`. Record the **selected set** now: it
is the denominator for every count you report later, and it never shrinks.

**If `.ux/cujs/` is absent or empty, stop and say so** — *"no CUJs authored; run `/ux-spec`"*
— and write no report. This is not pedantry. *"Every journey passed"* is **vacuously true**
against zero journeys, and an empty search domain that reports success is the exact defect
that nearly issued a false pass in the predecessor to this suite. **Zero journeys found is a
stop, never a pass.**

**Exit criteria:** a non-empty selected set, its size recorded — or a clean stop with the
reason.

### 2. Validate every selected journey before walking it

Run the validator and **paste its real output** into your summary — do not describe it:

```
python3 scripts/validate_cuj.py --dir .ux/cujs
```

A malformed journey is **skipped and disclosed**, never half-walked: half-verifying garbage
is worse than refusing, because it produces findings that look real.

Judgement the validator structurally cannot make, because it requires reading English:

- An **unobservable `expect`** ("it works", "the state updates") is an **authoring defect**.
  Report it as one and recommend `/ux-spec`. You cannot invent the ground truth you are
  checking against — doing so grades the app against a target you made up.
- A **precondition nobody can establish** is likewise an authoring defect. See step 4.

**Never repair the journey.** `.ux/cujs/` is off limits during an audit — `audit_safety.py`
under the default `audit` profile will flag the write, and rightly. Softening an `expect`
until the app passes is grading your own homework.

**A green validator is not evidence about the app.** It says the journey file is well-formed.
It says nothing about whether the app does what the file describes — that is steps 4–6.

**Exit criteria:** every selected journey is either validated or skipped-with-a-reason, and
the validator's literal output is shown.

### 3. Establish the mode and reach the app

Auto-select: a reachable running app → live; no app and no permission to start one → static.
**Ask the user first** before starting or restarting a dev server, and before navigating a
browser to any URL. If a requested `live` falls back to `static`, report it as `static` with
the reason — never claim evidence you could not gather.

**Auth pre-flight (live/hybrid).** Once the app is reachable, navigate to the selected
journeys' `entry_point`s and check whether a login wall stands between you and them. If one
does, run the **auth handoff** now — see
[`auth-handoff.md`](../usability-audit/references/auth-handoff.md) for the five beats, the
Never list, and the artifact posture.

Do it **here**, before step 4, not lazily when a precondition fails. A journey that needs a
session usually has a *precondition* that needs one too, so a lazy handoff asks the user the
same question twice — once for the precondition and once for the steps — and the second ask
arrives minutes into a run. One interruption, before any journey starts.

Record the outcome; it becomes the report's `Access:` line (report contract §5):

| Outcome | Then |
|---|---|
| No wall at any `entry_point` | Nothing to record *yet* — see below. Proceed. |
| Handoff succeeded | Proceed. Every selected journey inherits the session. |
| Declined | Journeys behind the wall are skipped with cause `precondition unmet — access declined`. |
| No attended browser surface | Same skip, cause `handoff unavailable — no attended browser surface`. **Not** a decline — nobody was asked. |

**The probe only sees the front door.** It navigates to `entry_point`s, so it can only
discover a wall that stands *there*. A journey that starts public and signs the user in
partway through — browse the catalogue, then authenticate at checkout — shows this probe no
wall at all, and the session it would have needed is not established. That case is real and
common; it is handled at L3 below, not here.

**Exit criteria:** mode fixed and recorded, with the reason if it differs from the request;
and, if a wall was met, the handoff outcome recorded.

### 4. Establish each journey's preconditions — the precondition ladder

`preconditions` say what must already be **true**; they are not steps. This is what lets a run
say *"skipped, `precondition unmet`"* honestly instead of reporting a severity-4 catastrophe
for what is really "couldn't run this".

Walk the ladder in order. Stop at the first **rung** that succeeds, and record every rung you
attempted, with its result — an unrecorded attempt makes a skip unauditable.

- **L0 — Observe before establishing.** Navigate to `entry_point` and check whether the
  precondition already holds. Record what you observed **verbatim** — row names, counts,
  visible strings. This is the **baseline**, and it is not bookkeeping: see step 6.
  Establishing state you already had is how a verifier manufactures the very state that
  hides the bug.
- **L1 — Replay a setup journey.** If another journey's `success_criteria` assert the state
  this precondition names, replay that journey in full first. **It establishes the
  precondition only if it `passed its own success_criteria`** — not merely if its steps
  passed. A journey whose steps pass and whose criteria fail has not established anything; it
  has proved the app is broken.
- **L2 — Improvised UI setup.** Ordinary use of the app's own affordances, when no setup
  journey exists. Record it as **improvised** and re-observe the state after a full page
  reload before starting step 1.
- **L2.5 — A named reset.** Clearing localStorage, logging out, starting a fresh session —
  **only when the journey file names the reset**, and **ask first** (SPEC §6). It destroys
  state the user may care about. A reset the journey does not name is not available at any
  price.
- **L3 — Ask the user.** For auth-gated or seeded state you may not create. Ask once, naming
  the exact state and the journey it unblocks. Supplied → back to L0. Declined → skip.
  **For an auth-gated precondition this rung has a defined handshake** — the auth handoff
  ([`auth-handoff.md`](../usability-audit/references/auth-handoff.md)): observe the wall,
  ask once, the *user* signs in, re-observe to confirm the session actually holds, then back
  to L0. For **seeded** state that is not auth-gated, the rung is unchanged: ask, and take
  what you are given.

  **Arriving here still walled — which of the two happened?** The answer decides whether you
  ask, and getting it wrong writes a decline into the report that the user never made.

  | What step 3's pre-flight did | Then |
  |---|---|
  | **Ran the handoff, and it was declined or unavailable** | Do **not** ask a second time. Record the rung as attempted, carry that cause forward verbatim, and skip. |
  | **Never met this wall** — it stood past the `entry_point`, so the probe could not see it | The user has not been asked about this wall. Run the handoff **now**, once, naming the step that hit it. |

  A wall the pre-flight never saw is not a decline and not "unavailable", and recording it
  as either blames a user who was never asked — the same failure
  [`auth-handoff.md`](../usability-audit/references/auth-handoff.md) §3 keeps out of the
  headless case. Ask once per *wall*, not once per run.

**The hard stop, below L3.** No host code, fixtures, migrations, seed scripts, direct
DB/API writes, and no `evaluate_script` state injection. This is a correctness rule before it
is a safety one: **injected state is state no user can reach through the UI**, so a journey
verified against it proves nothing about the product. And never **route around** a permission
gate or copy this plugin's tooling into the host repo — blocked and honest beats unblocked
and littering.

#### The no-alibi rule

**Never let a precondition failure alibi the journey it belongs to.** Some journeys can only
reach their own starting state through the very flow they exist to test — CUJ-001's
precondition is *"at least one existing task"*, and add-a-task is what CUJ-001 tests. Such a
precondition is **self-referential**, and under a naive ladder, breaking add-task would turn
CUJ-001 into a *skip* and the severity-4 would silently disappear.

So: **a self-referential precondition is never a skip.** Navigate to a bare `entry_point`,
note the unmet precondition in the Appendix, run the steps, and grade normally — adding
*"(precondition self-referential; graded from a bare entry_point)"* to the justification.

**No skip without an accounted cause.** Every skip names either a finding in *this* report or
a specific authoring defect in the journey file, plus a `Repair:` line saying what would
unblock it. If you can name neither, you have not diagnosed it — run the journey and grade
what happens.

**Exit criteria:** every selected journey is established, self-referential, or skipped with a
named cause and its attempted rungs recorded.

### 5. Replay the steps in order

Walk `steps` in `n` order against the app. For each, record the **verbatim** `expect`, what
you actually observed, and evidence — a screenshot under `.ux/audits/assets/`, a `file:line`,
or repro steps. A step marked pass with no evidence is an assertion, not a verification.

In **live/hybrid** mode, screenshot **every** step you replay — pass or fail — not only the
one that broke: the passing steps are what turn the captures into a visual walk-through
(step 7). Save each with the stable name `cuj-<id>-step-<n>.png` under `.ux/audits/assets/`
(and criteria/other evidence as `cuj-<id>-<slug>.png`, e.g. `cuj-001-after-reload.png`).
Stable names mean a re-run overwrites rather than accumulates — see the report contract's
asset-naming rule.

Run **setup journeys before the journeys that depend on them**. A finding discovered while
running a setup journey outside the selection is still reported — never discard a real
finding for scope reasons — but it does not enter the pass denominator.

Stop a journey at its first failing step: subsequent steps assume state the failure prevented,
so grading them produces noise. List them as **not observed** in the Appendix, never as
passes.

**Exit criteria:** every step has a verdict backed by evidence, or is listed as not observed.

### 6. Evaluate `success_criteria` — separately, after the steps

Criteria are evaluated **after** the journey completes, once, and they are not the last step's
`expect`. A journey can pass every step and still fail here: the row appears, the user
believes they succeeded, and it is gone after a reload. That class is invisible if you skip
this, and it grades **3, not 2** (step 7).

**An absence criterion needs a non-empty baseline.** A criterion like *"'Buy milk' is absent
from the active list after a reload"* is **vacuously true** when 'Buy milk' was never there —
which is exactly what a broken app produces. **Score an absence as a pass only if your L0
baseline recorded the thing present.** If it did not, the criterion is unverifiable: skip the
journey rather than credit it. Otherwise the app supplies the evidence for its own
verification, and a broken app passes *because* it is broken.

**Exit criteria:** each journey's criteria are scored against their verbatim text, with the
baseline that makes the score falsifiable.

### 7. Grade, then write one report per run

Grade each failure in two stages, naming **both** in the justification: classify (4 blocked /
3 workaround-or-criteria-fail / 2 observable mismatch / 1 cosmetic / 0 match), then **clamp**
by the journey's own `criticality` — `critical`/`high` uncapped, `medium` max 3, `low` max 2.
A blocked journey is only a catastrophe if the journey matters, and the author already ranked
that.

A **match is severity 0, and severity 0 is never a finding** — passing steps are enumerated in
the Appendix. And **a skip is not a finding** either: it carries no severity at all.

**On a cascade, do not open a second finding.** When CUJ-002 was skipped because CUJ-001 broke,
the bug is already reported against CUJ-001 — CUJ-002 reports
`skipped — precondition unmet; blocked by CUJ-001 step 2 (see F1)` and the finding count does
not move. One bug, one finding. Instead, the blocker's finding carries the blast radius:
`Also blocks: CUJ-002 "Complete a task" (high)`. Visibility rises; the count does not inflate.

Write **one report per run, not per CUJ** — `.ux/audits/cuj-<YYYYMMDD>-<HHMMSS>.md` — so
`index.md` rows stay 1:1 with runs. Append the index row.

**Lead the executive summary with the counts:**

```
P/N journeys passed, S skipped, M of T steps verified.
```

**`N` is the journeys you selected in step 1, never the journeys you managed to run.** A
skipped journey stays in the **denominator** permanently — that is what makes a muted check
visible. If everything skipped, say so in the first sentence: *"0/N journeys passed — every
journey was skipped; nothing was verified."*

Set `frameworks` to what the run **actually proved**, never to what it attempted:

- `cuj-contract` — always.
- `task-completion` — **only if the run actually completed, or actually failed to complete,
  the journey.** Live/hybrid only. A static run may not claim it.
- `success-criteria` — only if step 6 actually ran.

An all-skipped run therefore emits `frameworks: [cuj-contract]` alone — the same honest shape
as a static run, and the machine-readable signal that this `total: 0` is **not** a pass.

The Appendix carries: mode; frameworks applied; the CUJ manifest (ids verified, steps
verified, steps not observed); per skipped journey its unmet precondition verbatim, the rungs
attempted with results, the cause, and its `Repair:` line; per passed journey the L0 baseline
and which rung established it; setup journeys run outside the selection; and
**Coverage / not inspected**. Silent gaps are prohibited.

**In live/hybrid mode, assemble the step captures into a `## Walkthrough` section** (report
contract §5), after `## Findings` and before `## Appendix`. One `### Step <n> — <action>` per
step in `n` order, each embedding its screenshot inline —
`![CUJ-<id> step <n>](./assets/cuj-<id>-step-<n>.png)` — with a one-line expected-vs-observed.
This is the visual walk-through of the journey; a bare path is not enough, the embed must
render. Omit the section entirely in static mode (nothing was captured).

**Exit criteria:** the report validates —

```
python3 scripts/validate_report.py .ux/audits/cuj-<timestamp>.md
```

Then render its self-contained HTML companion — the per-step captures become an interactive
walk-through flipbook, and a `total: 0` verified pass renders as a green pass banner (never an
empty "no findings"):

```
python3 scripts/render_report_html.py .ux/audits/cuj-<timestamp>.md
python3 scripts/render_report_html.py --index .ux/audits/index.md
```

The `.html` is a derived view of the Markdown, written under `.ux/audits/` — the footprint
check below is unaffected. (Also available on demand via `/ux-review`.)

### 8. Confirm your footprint

```
python3 scripts/audit_safety.py <host-repo> --baseline /tmp/ux-baseline.json
```

The **default `audit` profile**, deliberately. You are an auditor: `.ux/audits/` is the only
place you write. `.ux/cujs/` and `SPEC.md` are **violations** for this skill even though
`/ux-spec` may write them — that asymmetry is the mechanical form of "never repair the journey
you are grading". Show the real output.

Pass step 1's baseline so this measures **your** footprint rather than the state of the repo
you walked into. The baseline forgives pre-existing dirt only while its bytes are unchanged —
so if you touched a file that was already modified, this still catches you, which is the point.

It is also what keeps the **positive** half honest across runs. Exit 0 requires that your own
writes under `.ux/audits/` were observed, and in a repo that ignores that directory (SPEC
§11.6) every previous run's report is still sitting there — without the baseline they would
answer "were writes observed?" on your behalf forever. With it, only bytes that differ from
run start count as yours.

If you never took the snapshot, say so and report the check as **run without a baseline**,
naming the pre-existing changes it flagged. Do not quietly present the user's own uncommitted
work as your violation, and do not quietly dismiss a real one as "probably theirs".

**Exit criteria:** all changes since the baseline confined to `.ux/audits/`.

## Boundaries

- **Never edit, refactor, or "fix" host application code.** Findings only. You report the
  broken step; repairing it is the user's call.
- **Never write to `.ux/cujs/` or the host's `SPEC.md`.** Report authoring defects; recommend
  `/ux-spec`.
- **Ask first** before starting a dev server, navigating a browser, performing a
  journey-named state reset, installing anything, or reaching auth-gated screens (the
  handshake for the last one is [`auth-handoff.md`](../usability-audit/references/auth-handoff.md)).
- **Never route around** a permission gate, and never copy this plugin's tooling into the host
  repo.
- **Once a session is live**, never read or store session material (cookies, `localStorage`,
  tokens), never read back a filled credential field, never leave the audited scope, never
  record the account identity, and never log the user out — a logout is a state reset no
  journey named. Full list: [`auth-handoff.md`](../usability-audit/references/auth-handoff.md) §7.
- **Never fabricate.** A step you did not observe is not a step that passed.
- **No opinions.** Ugly, slow, or inaccessible are real problems belonging to the other three
  auditors. You have no standard to judge them by.

## Exit criteria (done when)

- The selected set was recorded, and an empty `.ux/cujs/` stopped the run instead of passing it.
- Every selected journey validated, or was skipped and disclosed.
- Every journey's preconditions were established via a recorded rung, graded as
  self-referential, or skipped with a named cause.
- Every step has a verdict backed by evidence; unobserved steps are listed as not observed.
- `success_criteria` were scored separately, and every absence criterion has a baseline.
- Every finding names its journey and step, and its justification names both severity stages.
- One report per run under `.ux/audits/`, validating against the report contract, with an
  index row appended.
- In live/hybrid mode, each replayed step was screenshot with its stable name and the
  captures were assembled into a `## Walkthrough` section (omitted in static mode).
- The executive summary leads with `P/N journeys passed, S skipped, M of T steps verified`,
  where `N` is the journeys selected.
- `frameworks` claims only what the run proved.
- `audit_safety.py` exits 0 on **both** halves: nothing changed outside `.ux/audits/`,
  **and** the writes this run made inside it were observed and listed. (`git status` alone is
  not the check — once `.ux/audits/` is gitignored it shows nothing, which a run that wrote
  nothing satisfies identically.)
