---
name: riskiest-assumption-test
description: >
  Walks the founder through assumption dump, risk × impact ranking, falsifiable hypothesis
  rewriting, and test-method selection — produces a 1-page Assumption Test Plan with the top-3
  ranked hypotheses, success/kill criteria, and an interactive HTML risk × impact matrix. Use
  after `validation-canvas` and BEFORE `pitch-deck` — pitching on untested assumptions is
  sales theater. Triggers on "test my assumptions", "riskiest assumption", "RAT", "what should
  I validate first", "assumption mapping", "experiment design", "how do I de-risk this",
  "Wizard of Oz test", "fake door test", "concierge MVP", "smoke test", "5-interview rule", or
  when `validation-canvas.md` has populated Stress Tests and the user asks what's next. Job —
  "what have we proven?". Upstream half of validation closure; the downstream half loops
  results back into the canvas. NOT a discussion of testing in general (use `team-composer`);
  NOT a generic experiment platform. Produces a plan, not the experiments.
metadata:
  tier: draft
---

# Riskiest-Assumption Test

Convert the **beliefs** captured in the `validation-canvas` Stress Tests into
**falsifiable hypotheses** with explicit test methods, success criteria, and
kill criteria. Ship a 1-page Assumption Test Plan plus an interactive risk ×
impact matrix.

This skill's job is **experimental**: *what have we proven, and what's the
cheapest experiment that would invalidate the next belief?* It's the bridge
between the canvas (declarative beliefs) and the pitch deck (story you can
defend).

---

## What this skill produces

Every run produces exactly **two files**, both in the resolved RAT root
(see Phase 0 Step 0.0 for path resolution; default is `docs/rat/` for solo
runs, `docs/startup-kit/rat/` when invoked via orchestrator):

1. **`assumption-test-plan.md`** — canonical, editable Markdown with
   sections: `## Assumptions Dump`, `## Ranking Matrix`, `## Top 3
   Hypotheses`, `## Test Plan`, `## Kill Criteria`, `## Results`.
   Headings are load-bearing — `pitch-deck` and `startup-grill` grep them.
   `## Results` is initially empty; the founder fills it in as tests
   complete, which triggers the loop-back protocol.
2. **`test-matrix.html`** — interactive risk × impact matrix. Single
   self-contained HTML file. Each assumption is a draggable card on a 2D
   plane; click to expand the hypothesis, success criteria, kill criteria,
   and chosen test method. Color-coded by category (desirability /
   viability / feasibility). Print-clean for inclusion in board decks.
   Zero network dependencies.

Both files go into the resolved RAT folder. Existing files from prior
sessions are appended-to (Results section), never silently overwritten.

---

## What this skill is NOT

- **Not a canvas builder.** The canvas (Lean + VPC) is `validation-canvas`'s
  job. RAT *reads* the canvas; it does not produce it.
- **Not a pitch deck.** The deck is `pitch-deck`'s job. RAT *gates* the
  deck — pitch-deck refuses to ship if RAT Results are empty for top-3
  hypotheses (heavy gate).
- **Not the experiments themselves.** RAT produces a *plan* — what to test,
  how to test it, what success looks like. The actual landing page,
  concierge service, or Wizard of Oz prototype is built in the founder's
  real product surface (or with `web-artifacts-builder`, etc.).
- **Not a generic A/B-testing framework.** Methods here are early-stage
  validation experiments (concierge, Wizard of Oz, fake door, pre-sale,
  smoke test, 5-interview rule). Optimization-grade A/B testing is
  downstream and out of scope.
- **Not a substitute for talking to customers.** Several test methods
  *require* customer interviews. The skill helps design them; it does not
  do them for the founder.
- **Not a market research firm.** RAT is about *what to test cheaply*, not
  about commissioning a Forrester report.

---

## Skill Boundaries

| Request | Skill |
|---|---|
| "Help me design an assumption test" | `riskiest-assumption-test` (this skill) |
| "What's my riskiest assumption?" | `riskiest-assumption-test` |
| "Plan a Wizard of Oz / concierge / smoke / fake-door experiment" | `riskiest-assumption-test` |
| "Build a landing page for my fake-door test" | `web-artifacts-builder` (after this skill names the test design) |
| "Discuss validation strategy with a team" | `team-composer` with `@startup_strategist` + `@ux_researcher` |
| "Update my canvas because a test invalidated something" | `validation-canvas` (loop-back, update mode) |
| "Score my pitch deck adversarially" | `startup-grill` |

If the founder asks for both planning AND running ("plan AND run my fake-door
test"), do the planning here, then route to the appropriate builder skill
for the artifact. Don't try to be a build tool inside an experiment-design
skill.

---

## Phase 0: Read prior artifacts (medium gate)

**Goal:** confirm `validation-canvas.md` exists, parse it, and STOP if it's
missing.

### Step 0.0 — Path resolution + manifest awareness (v2.2.0+)

**Resolve the RAT root** once at invocation, in this precedence order
(canonical chain):

1. **Explicit `output_dir` arg** (passed by `startup-launch-kit`) → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var** set → `${STARTUP_KIT_DOCS_ROOT}/rat/`.
3. **Smart default — `docs/startup-kit/` exists** → `docs/startup-kit/rat/`.
   Surface the smart-default notice: *"Writing to `docs/startup-kit/rat/`
   (smart default). Set `STARTUP_KIT_DOCS_ROOT=./docs` to write standalone
   instead."*
4. **Solo fallback** → `docs/rat/`.

**Manifest awareness.** Look for `kit-manifest.json` at
`<resolved-kit-root>/kit-manifest.json` first; fall back to the
working-directory root for backward compat. Use it as a hint, never as a
bypass:

- If the manifest lists `riskiest-assumption-test` as `completed` with a
  recent mtime, surface that fact: *"Manifest says you ran RAT on [date].
  Update mode (re-rank, add results, revise top 3), fresh run, or skip to
  the next step?"* Update mode is the common case — the founder just ran
  experiments and is updating `## Results`.
- The `intake_answers` cache, if populated, informs how to communicate
  push-back rigor in Phase 3 (Hypothesis Rewriting) — repeat founders get
  push-back on glib hypotheses regardless of declared mode.
- Manifest read failures (corrupt JSON, missing fields) are non-fatal — log
  the issue inline and proceed as if no manifest exists.

After this skill ships its artifacts (Phase 5 — render & ship), if a
manifest exists, append/update this skill's entry. Use atomic write (write
`.tmp`, then rename). If the manifest doesn't exist, do **NOT** create it
— that's the `startup-launch-kit` orchestrator's job. See
[`startup-launch-kit/references/manifest-schema.md`](../startup-launch-kit/references/manifest-schema.md)
for the schema.

### Step 0.1 — Check for `validation-canvas.md`

Look for `validation-canvas.md` at `<canvas-root>/validation-canvas.md` —
the canvas root is the sibling of this skill's RAT root (e.g.,
`docs/startup-kit/canvas/` when this skill's root is
`docs/startup-kit/rat/`, or `docs/canvas/` when this skill's root is
`docs/rat/`). Fall back to the legacy path `validation-canvas.md` (cwd
root) for backward compat. If the file is missing at both, **STOP** and
route the founder to `validation-canvas`:

> *"This skill needs `validation-canvas.md` as its starting point — the
> Stress Tests section is the seed for the assumption dump. Run
> `validation-canvas` first; come back here when the canvas exists."*

If the canvas was found at the legacy path, surface a one-line notice
so the founder knows the artifact is at a v1 location: *"Read canvas
from legacy v1 path."*

**Override (rare):** if the founder explicitly says they have a canvas in
their head and want to RAT a one-pager directly, accept a paragraph dump
that names: top customer segment, UVP, top 1–3 problems, and 3+ assumptions
they're not sure of. Skip below the override is unusual — the canvas is the
right starting point.

### Step 0.2 — Parse the canvas

Read the canvas's `## Stress Tests` section first — that's the explicit
seed. Then scan the Lean Canvas blocks for `[Unknown — …]` markers and the
VPC for un-relieved Pains and un-created Gains. Each is an assumption
candidate.

### Step 0.3 — Check for prior `assumption-test-plan.md`

Look at `<rat-root>/assumption-test-plan.md` first; fall back to legacy
`rat/assumption-test-plan.md` (cwd-relative). If present, this is a re-run.
Surface the prior top-3 hypotheses and their Results status. Either the
founder is updating Results (run Phase 5 only) or revising the plan (full
Phase 1–5).

---

## Phase 1: Assumption Dump

**Goal:** surface every implicit belief in the canvas, categorized.

Use Christensen's three-axis framing:

- **Desirability** — *will customers want this?* (Problem fit, UVP fit,
  segment intensity.)
- **Viability** — *will the business model work?* (Pricing, willingness to
  pay, unit economics, channel CAC.)
- **Feasibility** — *can we actually build/deliver this?* (Technical risk,
  partner risk, regulatory risk, team capacity.)

For each assumption:

1. **Quote the canvas line that surfaced it.** ("UVP: 'Save 4 hours a week
   of contract redlining' assumes the segment values that 4 hours at >
   $300/mo.")
2. **Categorize** as desirability / viability / feasibility. (Some
   assumptions span — pick the *primary*.)
3. **Phrase as a belief**, not a fact. ("We *believe* X" — the framing makes
   the test-design phase easier later.)

Output: a flat list of 8–15 assumptions. (Fewer means you're missing some;
more means you're being too granular — collapse closely related ones.)

See `references/hypothesis-rewriting.md` for the belief → hypothesis
conversion patterns used in Phase 3.

---

## Phase 2: Risk × Impact Ranking

**Goal:** pick the top 3 assumptions to test now.

For each assumption, score on two axes:

- **Risk** (likelihood it's wrong): Low / Medium / High.
- **Impact** (consequence if wrong): Low / Medium / High → the higher
  end is "kills the business if invalidated."

Plot mentally on a 3×3 matrix. The **Top 3** come from the high-risk +
high-impact corner. If you have fewer than 3 in that corner, supplement
from high-impact + medium-risk. **Never** test low-impact assumptions first
— even if they're high-risk, the result doesn't move you forward.

See `references/ranking-matrix.md` for scoring rubrics with worked examples
and common scoring traps (e.g., founders systematically under-rate
desirability risk because they've already convinced themselves the
problem is real).

The Top 3 will be the assumptions written into `## Top 3 Hypotheses` in the
output Markdown and rendered as the largest cards in the interactive HTML
matrix.

---

## Phase 3: Hypothesis Rewriting (vague belief → falsifiable claim)

**Goal:** convert each top-3 belief into a falsifiable hypothesis that has
a clear measurable outcome.

The pattern (see `references/hypothesis-rewriting.md` for full guidance and
worked examples):

```
We believe [specific assumption about a specific segment].
We'll know this is true if [specific measurable outcome] within [time bound].
```

**Hard rules:**

- The outcome must be **observable** — not "they like it", but "5 of 10
  interviewees ask if they can buy it now."
- The outcome must be **measurable** — name the unit, named threshold.
- The time bound must be **short** — days or weeks at this stage, not
  quarters. Long time bounds are a sign of an unfalsifiable belief.
- The hypothesis must be **falsifiable** — there must be a plausible
  outcome that would convince the founder they were wrong.

**Anti-patterns to refuse:**

- *"We believe customers will love it."* (Not measurable.)
- *"We believe the market is huge."* (Wrong granularity — that's a market
  question, not an assumption test.)
- *"We believe it'll work eventually."* (Time-unbounded.)
- *"We believe the data will show product-market fit."* (Outcome is too
  abstract.)

If the founder produces an unfalsifiable hypothesis, **push back**. Don't
write a test plan for a vague claim; the resulting test will produce noise.

---

## Phase 4: Test Method Selection

**Goal:** match each top-3 hypothesis to the cheapest test method that can
falsify it.

See `references/test-method-catalog.md` for the full catalog. Quick guide:

| Hypothesis category | Best methods (cheapest first) |
|---|---|
| **Desirability** (do they want it?) | Customer interviews (5-interview rule), landing page + email capture, fake-door test, social-media smoke test |
| **Viability** (will they pay?) | Pre-sale, concierge MVP with explicit pricing, willingness-to-pay survey + interview |
| **Feasibility** (can we deliver?) | Wizard of Oz, technical spike, prototype with stub data, expert interview |

For each top-3 hypothesis, write into the Test Plan:

1. **Method** (named: e.g., "Concierge MVP — manually fulfill the first 5
   orders").
2. **Setup** (what you'll build/arrange — landing page URL, interview
   protocol, etc.).
3. **Sample** (who, how many — "10 ICP-matched founders sourced from X").
4. **Success criteria** (the measurable outcome from the hypothesis,
   restated; e.g., "≥ 4 of 10 sign LOI and pay $500 deposit").
5. **Kill criteria** (the outcome that says you were wrong — usually a
   simple "less than X").
6. **Time bound** (start date, end date — measured in days or weeks).
7. **Cost estimate** (hours of work + dollars; if either is large, look
   for a cheaper method).

**Hard rules:**

- **Method must match category.** Don't run a Wizard of Oz to test
  willingness to pay (you need real money), and don't run a pre-sale to test
  feasibility (you might be able to sell it but not build it).
- **Cheapest first.** The job is to find out fast, not to build the
  product. If the cheapest method is a 30-min interview, do the interview.
- **Fake-door tests need a real "door."** Landing pages with a fake "Buy"
  button only work if you can plausibly support the demand if it
  materializes.

---

## Phase 5: Render & Ship (and update mode)

**Goal:** produce `<rat-root>/assumption-test-plan.md` and
`<rat-root>/test-matrix.html`, save them, and present.

### Step 1 — Produce `assumption-test-plan.md`

Structure (headings are load-bearing — `pitch-deck` and `startup-grill`
grep them):

```markdown
# Assumption Test Plan — [Business Name]

> Generated [YYYY-MM-DD]. Based on `validation-canvas.md` (last updated [date]).

## Assumptions Dump

### Desirability
- [Assumption] — sourced from canvas line: "..."
- ...

### Viability
- ...

### Feasibility
- ...

## Ranking Matrix

| # | Assumption | Risk | Impact | Top 3? |
|---|---|---|---|---|
| 1 | ... | High | High | ✅ |
| 2 | ... | Med | High | ✅ |
| 3 | ... | High | Med | ✅ |
| 4 | ... | Med | Med | — |
...

## Top 3 Hypotheses

### Hypothesis 1: [short label]
- **We believe:** [specific assumption about a specific segment]
- **We'll know this is true if:** [measurable outcome] within [time bound]
- **Category:** Desirability / Viability / Feasibility

### Hypothesis 2: [short label]
- ...

### Hypothesis 3: [short label]
- ...

## Test Plan

### Test 1: [method name] for Hypothesis 1
- **Method:** ...
- **Setup:** ...
- **Sample:** ...
- **Success criteria:** ...
- **Kill criteria:** ...
- **Time bound:** [start] to [end]
- **Cost estimate:** [hours] + [dollars]

### Test 2: ...
### Test 3: ...

## Kill Criteria

(Summary of when each hypothesis is considered killed. Founder reads this
section under pressure; keep it terse.)

| # | Hypothesis | Killed if |
|---|---|---|
| 1 | ... | ... |
| 2 | ... | ... |
| 3 | ... | ... |

## Results

(Initially empty. Founder fills this section as tests complete. Each row
triggers loop-back protocol per `validation-canvas/references/folder-contract.md`.)

| # | Hypothesis | Test ran | Result | Status | Date |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

> When a hypothesis is invalidated, return to `validation-canvas` in update
> mode and revise the affected blocks. Do not advance to `pitch-deck` with
> invalidated core assumptions.
```

### Step 2 — Produce `test-matrix.html`

Read the template pattern in `references/matrix-html-template.md` (see file
for the full single-file Vanilla JS implementation). Key features:

- **Self-contained** — single file, all JS/CSS inline, zero network
  dependencies.
- **Interactive 3×3 risk × impact grid.** Each assumption is a draggable
  card. Founder can re-rank by dragging. Drops snap to grid cells.
- **Click to expand.** Card expands in place to show the hypothesis,
  success criteria, kill criteria, test method, and Results status.
- **Color-coded by category.** Desirability, Viability, Feasibility get
  three distinct accent colors (use brand-kit tokens if present).
- **Top-3 highlight.** The 3 cards selected as Top 3 in Phase 2 get a
  visible badge and a thicker border.
- **Print-clean.** `@media print` collapses to a static grid that prints
  cleanly to PDF for board decks. Drag handles hide; expanded states
  collapse to brief text.

Note: the matrix is **declarative only** — it visualizes the plan. It does
NOT execute the experiments and does NOT write to the Markdown file. Edits
in the HTML are session-local; persistence is the founder's job (re-run
this skill to update the canonical Markdown).

### Step 3 — Save to the resolved RAT folder

- `<rat-root>/assumption-test-plan.md`
- `<rat-root>/test-matrix.html`

Where `<rat-root>` is resolved per Phase 0 Step 0.0
(`docs/startup-kit/rat/` orchestrated, `docs/rat/` solo default, etc.).
Create the folder if absent.

Existing files from prior sessions: append to `## Results`, never silently
overwrite the rest. If the founder is materially revising the plan, ask
explicitly: *"This will rewrite Hypotheses and Test Plan but preserve
Results. Confirm?"*

### Step 4 — Present to the user

Use `present_files` if available. Otherwise emit clickable `computer://`
links. Present the HTML first (visual primary), Markdown second.

End with **three lines**:

1. *"Riskiest assumption right now: [Hypothesis 1 in plain language]."*
2. *"Cheapest way to test it this week: [test method, time bound, cost]."*
3. *"Next step: run the test. When you have results, update `## Results`
   and re-invoke `validation-canvas` if any hypothesis was invalidated. Do
   NOT skip to `pitch-deck` until at least one top-3 hypothesis has a
   confirmed result."*

The third line is the **heavy gate** to `pitch-deck`. Surface it explicitly
so the founder knows pitching is blocked until results land.

---

## Update mode (post-results loop-back)

When the founder re-invokes this skill after running tests:

1. **Read existing `<rat-root>/assumption-test-plan.md`.** Identify which Results
   rows are populated.
2. **Diff with prior state.** What changed?
3. **For each invalidated hypothesis:** Surface the loop-back: *"Hypothesis
   [N] failed (Result: …). The affected canvas block is [block]. Run
   `validation-canvas` in update mode to revise that block, then re-run RAT
   if the revision changes other assumptions."*
4. **For each confirmed hypothesis:** Mark it confirmed. Note that the
   founder is now free to advance to `pitch-deck` for that line of
   reasoning.
5. **Suggest next experiments.** If the top 3 are all resolved, the next 3
   from the ranking matrix become the new top 3.

This is the **loop-back protocol** — invalidated assumptions are a normal
action, not a failure mode. See
[`validation-canvas/references/folder-contract.md`](../validation-canvas/references/folder-contract.md)
for the full pipeline-wide protocol.

---

## Output Files

```
<rat-root>/assumption-test-plan.md   Canonical, editable test plan
<rat-root>/test-matrix.html          Interactive risk × impact matrix
```

Where `<rat-root>` resolves per Phase 0 Step 0.0:

- `docs/startup-kit/rat/` — orchestrated (via `startup-launch-kit`)
- `docs/rat/` — solo default
- `docs/startup-kit/rat/` — solo with `docs/startup-kit/` smart default
- `${STARTUP_KIT_DOCS_ROOT}/rat/` — env-var override

No other files. Do not scatter intermediate analyses across the working
folder.

---

## Quality Checklist

Before presenting to the user, verify each:

**Phase 0 (Gate)**
- [ ] `validation-canvas.md` exists (or override path was used with explicit
      one-pager input)
- [ ] Stress Tests section + `[Unknown — …]` markers were parsed as the
      assumption seed

**Phase 1–4 (Plan)**
- [ ] 8–15 assumptions in the dump (not fewer, not more)
- [ ] Each assumption has a quoted canvas line and a category
- [ ] Top 3 selected from high-impact corner of the matrix (with reasoning if
      a high-risk + low-impact item was excluded)
- [ ] Each top-3 hypothesis is **falsifiable** (measurable outcome, time
      bound, observable signal)
- [ ] Each top-3 hypothesis has a Test Plan row with method, setup, sample,
      success criteria, kill criteria, time bound, cost estimate
- [ ] Method matches hypothesis category (no Wizard of Oz for viability, no
      pre-sale for feasibility)
- [ ] Cheapest method considered first (no $50K research project when 10
      interviews would do)

**Phase 5 (Output)**
- [ ] `assumption-test-plan.md` uses the exact heading structure (so
      `pitch-deck` and `startup-grill` can parse it)
- [ ] `test-matrix.html` is a single file, opens in a browser, drag
      works, click-to-expand works, prints cleanly
- [ ] `## Results` section preserved if existing file was being updated
- [ ] Brand tokens applied if `<kit-root>/brand/DESIGN.md` (or legacy `brand-kit/DESIGN.md`) present; reads `colors.primary` from YAML front matter
- [ ] Files saved to the resolved RAT folder per Phase 0 Step 0.0 (not cwd root)
- [ ] Smart-default notice surfaced if smart-default fired
- [ ] Response ends with the three lines (riskiest assumption + cheapest
      test + heavy-gate-to-pitch-deck note)

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `validation-canvas` (our own) | **Required upstream** (medium gate). This skill STOPs without `validation-canvas.md`. After this skill ships, invalidated hypotheses route back to `validation-canvas` in update mode (loop-back). |
| `pitch-deck` (our own) | Downstream (heavy gate). Pitch-deck STOPs without populated `## Results` for top-3 hypotheses. Override available with `[PRE-VALIDATION DRAFT]` watermark. |
| `startup-grill` (our own) | Last step. Reads `<rat-root>/assumption-test-plan.md` Results to check whether canvas was iterated after testing (yellow-flags pristine pipelines). |
| `brand-workshop` (our own) | Upstream — provides design tokens via `DESIGN.md` ([Google Labs spec](https://github.com/google-labs-code/design.md), version `alpha`; reads `colors.primary` from YAML front matter) at `<kit-root>/brand/DESIGN.md` or legacy `brand-kit/DESIGN.md` for the interactive matrix HTML. Optional. |
| `team-composer` (our own) | Instead of this skill when the founder wants to *discuss* validation strategy without committing to a written plan. After this skill when the test plan needs multi-role pressure-testing. |
| `web-artifacts-builder` (Anthropic) | After this skill names a fake-door / landing-page test, use this to actually build the test surface. |
| `theme-factory` (Anthropic) | When the matrix HTML needs branded styling and no brand artifact (`<kit-root>/brand/DESIGN.md` or legacy `brand-kit/DESIGN.md`) is present. |
| `pdf` (Anthropic) | When merging the test plan into a board packet. |

**Principle:** this skill owns the **test design** — what to test, how to
test it, what success and kill look like. It does not run the tests, does
not build the test surfaces, does not validate the canvas, and does not
produce the pitch. Hand off rather than over-reach.

**Graceful degradation:** if a referenced skill is not installed, this
skill still ships `<rat-root>/assumption-test-plan.md` +
`<rat-root>/test-matrix.html` — downstream integrations are enhancements,
not requirements.
